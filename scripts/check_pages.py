"""Record live page disclosures; render the saved check without network access.

Live checks retain responses and retrieval receipts in an external evidence folder.
A successful recording can contain gaps: inspect each row's passed flag. Repeat
with --require-pass after deployment to require all published pages to pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen

import build_pages

FIELDS = ("visibility", "license", "last_license_check", "source_authority")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def page_expectations() -> dict[str, dict[str, list[str]]]:
    inventory = build_pages.published_pages()
    metadata = {
        page: build_pages.split_frontmatter(source.read_text(encoding="utf-8"))[0]
        for page, source in inventory.items() if source is not None
    }
    expectations = {
        page: {field: [str(meta[field])] if meta.get(field) else [] for field in FIELDS}
        for page, meta in metadata.items()
    }
    expectations["index.html"] = {
        field: sorted({str(meta[field]) for meta in metadata.values() if meta.get(field)})
        if metadata and all(meta.get(field) for meta in metadata.values()) else []
        for field in FIELDS
    }
    return {page: expectations[page] for page in inventory}


class Disclosures(HTMLParser):
    """Extract visible text from disclosure elements, not incidental body text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.badges = []
        self.provenance = []
        self.notes = []
        self.site_commit = None
        self.site_build_time = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            if attrs.get("name") == "site-commit":
                self.site_commit = attrs.get("content")
            if attrs.get("name") == "build-time":
                self.site_build_time = attrs.get("content")
        style = re.sub(r"\s+", "", attrs.get("style", "").lower())
        hidden = (tag in {"script", "style", "template"} or "hidden" in attrs
                  or attrs.get("aria-hidden") == "true" or "display:none" in style
                  or "visibility:hidden" in style or any(frame["hidden"] for frame in self.stack))
        classes = attrs.get("class", "").split()
        kind = ("badge" if "badge" in classes else "prov" if "prov" in classes
                else "data-limits" if "data-limits" in classes else None)
        if tag not in {"meta", "link", "br", "hr", "img", "input", "source", "wbr"}:
            self.stack.append({"tag": tag, "hidden": hidden, "kind": kind, "text": []})

    def handle_data(self, data):
        if not any(frame["hidden"] for frame in self.stack):
            for frame in self.stack:
                if frame["kind"]:
                    frame["text"].append(data)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                closed, self.stack = self.stack[index:], self.stack[:index]
                for frame in closed:
                    if frame["hidden"]:
                        continue
                    text = " ".join("".join(frame["text"]).split())
                    target = {"badge": self.badges, "prov": self.provenance,
                              "data-limits": self.notes}.get(frame["kind"])
                    if target is not None:
                        target.append(text)
                break


def inspect_page(document: str, expected: dict[str, list[str]]) -> dict:
    parser = Disclosures()
    parser.feed(document)
    badges = {
        field: bool(values) and all(
            ("license checked " + value if field == "last_license_check" else value)
            in parser.badges for value in values
        ) for field, values in expected.items()
    }
    authorities = expected.get("source_authority", [])
    provenance = bool(authorities) and all(any(
        "Provenance." in block and authority in block for block in parser.provenance
    ) for authority in authorities)
    return {
        "badges": badges,
        "provenance": provenance,
        "data_limits": any(note.startswith("Data limits.") and note[len("Data limits."):].strip()
                           for note in parser.notes),
        "site_commit": parser.site_commit,
        "site_build_time": parser.site_build_time,
    }


def fetch_page(url: str) -> tuple[int | None, bytes, dict, str | None]:
    try:
        with urlopen(url, timeout=60) as response:
            return response.status, response.read(), dict(response.headers), None
    except HTTPError as error:
        return error.code, error.read(), dict(error.headers), None
    except (URLError, TimeoutError, OSError) as error:
        # Exception messages can contain local identifiers; retain the type only.
        return None, b"", {}, type(error).__name__


def check_site(site: str, source_commit: str, evidence: Path) -> dict:
    if urlsplit(site).scheme != "https":
        raise ValueError("The site must use HTTPS")
    evidence.mkdir(parents=True, exist_ok=True)
    record = {"source_commit": source_commit, "site": site, "pages": []}
    for index, (page, expected) in enumerate(page_expectations().items()):
        if index:
            time.sleep(1)
        url = urljoin(site.rstrip("/") + "/", page)
        started = utc_now()
        status, body, headers, error = fetch_page(url)
        retrieved = utc_now()
        result = inspect_page(body.decode("utf-8", errors="replace"), expected)
        row = {
            "page": page, "url": url, "request_started_at": started,
            "retrieved_at": retrieved, "http_status": status, "error": error,
            "response_sha256": sha256(body), "response_bytes": len(body),
            "http_last_modified": headers.get("Last-Modified"), "expected": expected,
            **result,
        }
        row["passed"] = (status == 200 and error is None and all(row["badges"].values())
                         and row["provenance"] and row["data_limits"])
        (evidence / page).write_bytes(body)
        (evidence / (page + ".json")).write_text(json_text(row), encoding="utf-8")
        record["pages"].append(row)
    return record


def local_build_results(directory: Path) -> list[dict]:
    results = []
    for page, expected in page_expectations().items():
        body = (directory / page).read_bytes()
        result = inspect_page(body.decode("utf-8"), expected)
        if not (all(result["badges"].values()) and result["provenance"] and result["data_limits"]):
            raise ValueError("Local disclosure gap: " + page)
        results.append({"page": page, "sha256": sha256(body), "bytes": len(body), **result})
    return results


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_report(record: dict, revisions: list[dict]) -> str:
    if not revisions or str(revisions[-1]["revision"]) != str(record["revision"]):
        raise ValueError("Newest revision must match the report revision")
    rows = record["pages"]
    count = len(rows)
    out = ["# Published page disclosure check", "", "## Summary", "",
           f"Revision {record['revision']}. {count} published pages checked; "
           f"{sum(row['passed'] for row in rows)} passed all live disclosure checks.", "",
           "## Revision history", "", "| Revision | Date | What changed and why |",
           "|---|---|---|"]
    out += [f"| {row['revision']} | {row['date']} | {row['change']} |" for row in revisions]
    out += ["", "## Results", "", f"Source metadata read at `{record['source_commit']}`.", "",
            "The inventory is the page list used by the site builder, including its home page.", "",
            "| Page | HTTP | Visibility | License | Check date | Authority | Provenance | Data limits | Retrieved UTC |",
            "|---|---|---|---|---|---|---|---|---|"]
    def yes(value):
        return "present" if value else "missing"
    for row in rows:
        values = [row["page"], str(row["http_status"] or "unavailable")]
        values += [yes(row["badges"][field]) for field in FIELDS]
        values += [yes(row["provenance"]), yes(row["data_limits"]), row["retrieved_at"]]
        out.append("| " + " | ".join(values) + " |")
    out += ["", "| Disclosure | Present | Missing |", "|---|---|---|"]
    for field in FIELDS + ("provenance", "data_limits"):
        present = sum(row["badges"][field] if field in FIELDS else row[field] for row in rows)
        out.append(f"| {field} | {present} | {count - present} |")
    out += ["", "## Local source correction", "",
            "The builder now renders visibility, license, check date and authority badges, "
            "provenance and a data-limits note on every published page. The home page uses "
            "domain frontmatter rather than inventing an aggregate license-check date. "
            "CSS is embedded so each generated page is self-contained.", "",
            "| Page | Bytes | SHA-256 |", "|---|---|---|"]
    for row in record.get("local_build", []):
        out.append(f"| {row['page']} | {row['bytes']} | `{row['sha256']}` |")
    out += ["", "## Known limits", "",
            "Live results describe the retrieved deployment, before the source correction. "
            "Repeat the check after merge and the Pages rebuild; local rendering does not "
            "prove that the corrected pages have deployed (Refs #2).", "",
            "Site commit and build time are recorded only when explicitly stated in page metadata. "
            "An HTTP Last-Modified header is retained separately and is not a build time. "
            "No new source-license audit, data validation or quarterly audit was performed. "
            "The check detects structural disclosure elements and simple hidden attributes; "
            "it does not evaluate CSS layout or legal validity.", "",
            "## Reproduction", "",
            "Run `python scripts/check_pages.py --site <public-site-url> --source-commit <metadata-commit> "
            "--evidence-dir <evidence-folder> --record <record.json> --report <report.md> "
            "--revisions reports/pages/revisions.json --local-build <built-pages-folder>`.", "",
            "After deployment, add `--require-pass`. For offline regeneration use "
            "`--from-record reports/pages/checks.json --report <report.md> "
            "--revisions reports/pages/revisions.json` instead of the live retrieval arguments.", ""]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--site")
    mode.add_argument("--from-record", type=Path)
    parser.add_argument("--source-commit")
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--revisions", type=Path, required=True)
    parser.add_argument("--local-build", type=Path)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()
    revisions = json.loads(args.revisions.read_text(encoding="utf-8"))
    if args.site:
        if not (args.source_commit and args.evidence_dir and args.record):
            parser.error("Live retrieval requires source commit, evidence folder and record")
        record = check_site(args.site, args.source_commit, args.evidence_dir)
        record["revision"] = revisions[-1]["revision"]
    else:
        record = json.loads(args.from_record.read_text(encoding="utf-8"))
    if args.local_build:
        record["local_build"] = local_build_results(args.local_build)
    report = render_report(record, revisions)
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json_text(record), encoding="utf-8")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    passed = sum(row["passed"] for row in record["pages"])
    print(f"Recorded {len(record['pages'])} pages; {passed} passed live checks")
    return int(args.require_pass and passed != len(record["pages"]))


if __name__ == "__main__":
    raise SystemExit(main())
