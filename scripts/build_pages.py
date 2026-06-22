# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build the worldenergydata-wiki static GitHub Pages site.

Same deterministic, stdlib-only pattern as the worldenergydata exemplar:
render the source Markdown to static HTML, no server, no API key. The wiki's
distinguishing feature is rendered as visible per-page badges: every page
carries its source authority, public-domain/CC-BY license, and last
license-check date, derived from YAML frontmatter.

Run:  python3 scripts/build_pages.py   (writes public/, gitignored)
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"

DOMAINS = ["bsee", "noaa", "usgs", "mms"]


# ---------------------------------------------------------------------------
# Minimal YAML frontmatter parser (stdlib only) — handles `key: value`,
# quoted values, and simple `key:\n  - item` lists. Sufficient for these pages.
# ---------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body_start = text.find("\n", end + 1)
    body = text[body_start + 1:] if body_start != -1 else ""
    meta: dict = {}
    cur_key = None
    for line in raw.splitlines():
        if re.match(r"^\s+-\s+", line):  # list item
            if cur_key:
                meta.setdefault(cur_key, [])
                if isinstance(meta[cur_key], list):
                    meta[cur_key].append(line.strip()[2:].strip().strip('"'))
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m:
            cur_key, val = m.group(1), m.group(2).strip()
            if val == "":
                meta[cur_key] = []
            else:
                meta[cur_key] = val.strip('"').strip("[]") if not val.startswith("[") else \
                    [v.strip().strip('"') for v in val.strip("[]").split(",")]
    return meta, body


# ---------------------------------------------------------------------------
# Markdown -> HTML (headings, tables, lists, hr, bold, links, inline code).
# ---------------------------------------------------------------------------
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_CODE = re.compile(r"`([^`]+)`")


def _md_link_rewrite(url: str) -> str:
    # wiki/<domain>/index.md -> <domain>.html ; ./index.md style -> index
    m = re.search(r"wiki/([a-z]+)/index\.md", url)
    if m:
        return f"{m.group(1)}.html"
    return url


def _inline(text: str) -> str:
    text = _CODE.sub(lambda m: f"<code>{html.escape(m.group(1))}</code>", text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _LINK.sub(lambda m: f'<a href="{_md_link_rewrite(m.group(2))}">{m.group(1)}</a>', text)
    return text


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i, n = 0, len(lines)
    para: list[str] = []

    def flush():
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para.clear()

    while i < n:
        s = lines[i].strip()
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            flush()
            block = [lines[i], lines[i + 1]]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in block]
            head, _al, *body = cells
            t = ["<div class='table-wrap'><table><thead><tr>"]
            t += [f"<th>{_inline(c)}</th>" for c in head] + ["</tr></thead><tbody>"]
            for row in body:
                t.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in row) + "</tr>")
            out.append("".join(t) + "</tbody></table></div>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush(); lvl = len(m.group(1))
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if s in ("---", "***", "___"):
            flush(); out.append("<hr>"); i += 1; continue
        if re.match(r"^[-*]\s+", s):
            flush(); items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip())); i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(it)}</li>" for it in items) + "</ul>")
            continue
        if not s:
            flush(); i += 1; continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)


STYLE = """:root{--fg:#1a2230;--muted:#5b6675;--bg:#f7f8fa;--card:#fff;--line:#e2e6ec;--brand:#1763c7;--gov:#0a6b46}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
header.site,footer.site{padding:14px 22px;background:var(--card);border-bottom:1px solid var(--line)}
footer.site{border-top:1px solid var(--line);border-bottom:0;color:var(--muted);font-size:14px;margin-top:48px}
header.site{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.home{color:var(--brand);text-decoration:none;font-weight:700}
nav.domains{display:flex;gap:10px;flex-wrap:wrap}
nav.domains a{font-size:14px;color:var(--muted);text-decoration:none;text-transform:uppercase;letter-spacing:.03em}
nav.domains a:hover{color:var(--brand)}
main{max-width:880px;margin:0 auto;padding:28px 22px}
h1{font-size:28px}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 18px}
.badge{font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px;background:#eef1f5;color:var(--muted);border:1px solid var(--line)}
.badge.gov{background:#e7f7ef;color:var(--gov);border-color:#bce8d3}
.prov{background:#eef4fc;border-left:4px solid var(--brand);padding:10px 14px;border-radius:0 6px 6px 0;font-size:14px;margin:0 0 18px}
.table-wrap{overflow-x:auto;margin:1em 0}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card)}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left}
th{background:#f0f3f7}
a{color:var(--brand)}
code{background:#eef1f5;padding:1px 5px;border-radius:4px}
hr{border:0;border-top:1px solid var(--line);margin:1.4em 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:22px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;text-decoration:none;color:inherit;transition:.15s;display:block}
.card:hover{border-color:var(--brand);box-shadow:0 4px 16px rgba(23,99,199,.1);transform:translateY(-2px)}
.card h3{margin:.1em 0 .3em;color:var(--brand);text-transform:uppercase}
.card p{color:var(--muted);font-size:13px;margin:0}
"""

NAV = '<nav class="domains">' + "".join(
    f'<a href="{d}.html">{d}</a>' for d in DOMAINS) + '</nav>'


def shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · worldenergydata-wiki</title>
<link rel="stylesheet" href="assets/style.css"></head>
<body><header class="site"><a class="home" href="index.html">worldenergydata-wiki</a>{NAV}</header>
<main>{body}</main>
<footer class="site">
<p>Public-domain US federal energy data (17 USC §105). Wiki prose CC-BY-4.0; code MIT. Public-domain status preserved through derivation.</p>
<p>Companion library: <a href="https://github.com/vamseeachanta/worldenergydata">vamseeachanta/worldenergydata</a> · <a href="https://github.com/vamseeachanta/worldenergydata-wiki">source</a></p>
</footer></body></html>"""


def badges(meta: dict) -> str:
    out = []
    lic = meta.get("license", "")
    if lic:
        out.append(f'<span class="badge gov">{html.escape(str(lic))}</span>')
    if meta.get("source_authority"):
        out.append(f'<span class="badge">{html.escape(str(meta["source_authority"]))}</span>')
    if meta.get("last_license_check"):
        out.append(f'<span class="badge">license checked {html.escape(str(meta["last_license_check"]))}</span>')
    return f'<div class="badges">{"".join(out)}</div>' if out else ""


def provenance(meta: dict) -> str:
    srcs = meta.get("sources") or []
    if isinstance(srcs, str):
        srcs = [srcs]
    links = " · ".join(f'<a href="{html.escape(s)}">{html.escape(s)}</a>' for s in srcs)
    auth = html.escape(str(meta.get("source_authority", "US federal public-domain source")))
    return f'<p class="prov"><strong>Provenance.</strong> {auth}. {("Sources: " + links) if links else ""}</p>'


def build():
    PUBLIC.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "style.css").write_text(STYLE, encoding="utf-8")

    built = []
    for d in DOMAINS:
        src = WIKI / d / "index.md"
        if not src.exists():
            continue
        meta, body = split_frontmatter(src.read_text(encoding="utf-8"))
        title = meta.get("title", d.upper())
        page_body = badges(meta) + provenance(meta) + f'<div class="content">{md_to_html(body)}</div>'
        (PUBLIC / f"{d}.html").write_text(shell(str(title), page_body), encoding="utf-8")
        built.append(d)

    # Landing
    cards = "".join(
        f'<a class="card" href="{d}.html"><h3>{d}</h3><p>Public-domain federal data knowledge surface.</p></a>'
        for d in built
    )
    landing = shell("Public-domain US federal energy data wiki", f"""
<h1>worldenergydata-wiki</h1>
<p>Derived knowledge pages for US federal energy data corpora — BSEE, NOAA, USGS, MMS.
Every page is built from public-domain federal sources and stamped with its source
authority, license, and last license-check date. No API key, no server.</p>
<p class="prov"><strong>Why public.</strong> The underlying data are US federal public-domain
works (17 USC §105); gating them behind auth would invert that status. Vendor-licensed
engineering standards live in the private companion wiki instead — the wiki tier matches the
license tier of its source.</p>
<div class="cards">{cards}</div>
<h2>How this site works</h2>
<p>A stdlib-only generator renders the <code>wiki/</code> Markdown to static HTML, carrying
each page's YAML-frontmatter provenance (source authority, license, last check) as visible
badges. Built output is regenerated in CI — what ships always matches source.</p>
""")
    (PUBLIC / "index.html").write_text(landing, encoding="utf-8")

    pages = sorted(p.name for p in PUBLIC.glob("*.html"))
    print(f"Built {len(pages)} pages: {', '.join(pages)}")


if __name__ == "__main__":
    build()
