"""Offline fixtures for page disclosures and reproducible reports."""
import importlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_pages


@pytest.fixture
def checker():
    return importlib.import_module("check_pages")


@pytest.fixture
def expected():
    return {
        "visibility": ["public-federal-data"],
        "license": ["public-domain"],
        "last_license_check": ["2026-05-20"],
        "source_authority": ["Federal agency & survey"],
    }


@pytest.fixture
def disclosed_html():
    return """<html><head><meta name="site-commit" content="fixture-commit"></head>
<body><div class="badges">
<span class="badge">public-federal-data</span>
<span class="badge">public-domain</span>
<span class="badge">license checked 2026-05-20</span>
<span class="badge">Federal agency &amp; survey</span></div>
<p class="prov"><strong>Provenance.</strong> Federal agency &amp; survey.</p>
<aside class="data-limits"><strong>Data limits.</strong> Coverage is incomplete.</aside>
</body></html>"""


def test_complete_disclosures(checker, expected, disclosed_html):
    result = checker.inspect_page(disclosed_html, expected)
    assert all(result["badges"].values())
    assert result["provenance"] and result["data_limits"]
    assert result["site_commit"] == "fixture-commit"
    assert result["site_build_time"] is None


@pytest.mark.parametrize("field", ["visibility", "license", "last_license_check", "source_authority"])
def test_wrong_badge_value(checker, expected, disclosed_html, field):
    expected[field] = ["different value"]
    assert not checker.inspect_page(disclosed_html, expected)["badges"][field]


def test_body_text_does_not_count_as_badge(checker, expected):
    document = "<p>public-domain public-federal-data license checked 2026-05-20 Federal agency &amp; survey</p>"
    assert not any(checker.inspect_page(document, expected)["badges"].values())


@pytest.mark.parametrize("markup", [
    '<aside class="data-limits">Data limits.</aside>',
    '<script><aside class="data-limits">Data limits. Missing records.</aside></script>',
    '<aside class="data-limits" hidden>Data limits. Missing records.</aside>',
    '<aside class="data-limits" style="display:none">Data limits. Missing records.</aside>',
])
def test_empty_or_hidden_note_is_missing(checker, expected, markup):
    assert not checker.inspect_page(markup, expected)["data_limits"]


def test_missing_frontmatter_is_not_success(checker, disclosed_html):
    expected = {field: [] for field in ("visibility", "license", "last_license_check", "source_authority")}
    assert not any(checker.inspect_page(disclosed_html, expected)["badges"].values())


def test_site_build_time_is_explicit(checker, expected, disclosed_html):
    document = disclosed_html.replace('name="site-commit"', 'name="build-time"')
    assert checker.inspect_page(document, expected)["site_build_time"] == "fixture-commit"


def test_inventory_matches_builder(checker, tmp_path):
    build_pages.build(tmp_path)
    assert set(checker.page_expectations()) == {p.name for p in tmp_path.glob("*.html")}


def test_builder_has_all_disclosures(checker, tmp_path):
    build_pages.build(tmp_path)
    for page, expected in checker.page_expectations().items():
        result = checker.inspect_page((tmp_path / page).read_text(), expected)
        assert all(result["badges"].values()), page
        assert result["provenance"] and result["data_limits"], page


def test_builder_pages_are_self_contained(tmp_path):
    build_pages.build(tmp_path)
    for page in tmp_path.glob("*.html"):
        assert '<link rel="stylesheet"' not in page.read_text()
        assert '<style>' in page.read_text()


def test_builder_is_byte_identical(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    build_pages.build(first)
    build_pages.build(second)
    assert {p.name: p.read_bytes() for p in first.glob("*.html")} == {
        p.name: p.read_bytes() for p in second.glob("*.html")
    }


def test_http_failure_retains_evidence(checker, expected, disclosed_html, monkeypatch, tmp_path):
    monkeypatch.setattr(checker, "page_expectations", lambda: {"fixture.html": expected})
    monkeypatch.setattr(checker.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(checker, "fetch_page", lambda url: (404, disclosed_html.encode(), {}, None))
    record = checker.check_site("https://example.org/", "fixture-base", tmp_path)
    row = record["pages"][0]
    assert row["http_status"] == 404
    assert not row["passed"]
    assert row["retrieved_at"].endswith("Z")
    assert checker.sha256((tmp_path / "fixture.html").read_bytes()) == row["response_sha256"]
    assert json.loads((tmp_path / "fixture.html.json").read_text())["url"] == row["url"]


def test_transport_failure_is_not_http_success(checker, expected, monkeypatch, tmp_path):
    monkeypatch.setattr(checker, "page_expectations", lambda: {"fixture.html": expected})
    monkeypatch.setattr(checker, "fetch_page", lambda url: (None, b"", {}, "TimeoutError"))
    record = checker.check_site("https://example.org/", "fixture-base", tmp_path)
    assert record["pages"][0]["http_status"] is None
    assert record["pages"][0]["error"] == "TimeoutError"
    assert not record["pages"][0]["passed"]


def test_report_revision_matches_data(checker):
    record = {"revision": "1", "pages": [], "source_commit": "fixture-base"}
    revisions = [{"revision": "1", "date": "2026-10-14", "change": "Record page disclosures and their limits."}]
    report = checker.render_report(record, revisions)
    assert report.index("## Summary") < report.index("## Revision history") < report.index("## Results")
    assert "| 1 | 2026-10-14 | Record page disclosures and their limits. |" in report
    assert report == checker.render_report(record, revisions)


def test_report_rejects_revision_mismatch(checker):
    with pytest.raises(ValueError, match="revision"):
        checker.render_report({"revision": "2", "pages": []}, [{"revision": "1"}])


def test_visibility_badge_from_frontmatter():
    assert 'public-federal-data' in build_pages.badges({"visibility": "public-federal-data"})


def test_data_limits_in_existing_builder(monkeypatch, tmp_path):
    monkeypatch.setattr(build_pages, "PUBLIC", tmp_path)
    build_pages.build()
    for page in tmp_path.glob("*.html"):
        assert 'Data limits.' in page.read_text(), page.name
