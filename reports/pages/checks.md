# Published page disclosure check

## Summary

Revision 1. 5 published pages checked; 0 passed all live disclosure checks.

## Revision history

| Revision | Date | What changed and why |
|---|---|---|
| 1 | 2026-10-14 | Record live disclosures and source corrections so deployment gaps can be checked after rebuilding. |

## Results

Source metadata read at `8f4890259fcf9e754b1c91faf12127128d239fe3`.

The inventory is the page list used by the site builder, including its home page.

| Page | HTTP | Visibility | License | Check date | Authority | Provenance | Data limits | Retrieved UTC |
|---|---|---|---|---|---|---|---|---|
| index.html | 200 | missing | missing | missing | missing | missing | missing | 2026-10-14T21:27:12Z |
| bsee.html | 200 | missing | present | present | present | present | missing | 2026-10-14T21:27:13Z |
| noaa.html | 200 | missing | present | present | present | present | missing | 2026-10-14T21:27:14Z |
| usgs.html | 200 | missing | present | present | present | present | missing | 2026-10-14T21:27:16Z |
| mms.html | 200 | missing | present | present | present | present | missing | 2026-10-14T21:27:17Z |

| Disclosure | Present | Missing |
|---|---|---|
| visibility | 0 | 5 |
| license | 4 | 1 |
| last_license_check | 4 | 1 |
| source_authority | 4 | 1 |
| provenance | 4 | 1 |
| data_limits | 0 | 5 |

## Local source correction

The builder now renders visibility, license, check date and authority badges, provenance and a data-limits note on every published page. The home page uses domain frontmatter rather than inventing an aggregate license-check date. CSS is embedded so each generated page is self-contained.

| Page | Bytes | SHA-256 |
|---|---|---|
| index.html | 6746 | `579fea915a562384cf2f4395dc0e2ce1953b24055f6a02a82eae401acf3adf3d` |
| bsee.html | 5921 | `9dec5b0406fc63248b90f41c9d3196827c831f19b8a4f341f5a77ef0ba25a41f` |
| noaa.html | 5827 | `8fce9468e98e82662d7e160306f6ca35735c75dc81708f427b310c2040c4ad32` |
| usgs.html | 5774 | `5dae49c249dcb7ef89a72ebc5045fcb973d24f015a0fbf4cf872f2cf9e051f84` |
| mms.html | 6190 | `8586f7364a44d74e83a714c51f6f20b777d63e397ec33ba8b556d2c0892cb86e` |

## Known limits

Live results describe the retrieved deployment, before the source correction. Repeat the check after merge and the Pages rebuild; local rendering does not prove that the corrected pages have deployed (Refs #2).

Site commit and build time are recorded only when explicitly stated in page metadata. An HTTP Last-Modified header is retained separately and is not a build time. No new source-license audit, data validation or quarterly audit was performed. The check detects structural disclosure elements and simple hidden attributes; it does not evaluate CSS layout or legal validity.

## Reproduction

Run `python scripts/check_pages.py --site <public-site-url> --source-commit <metadata-commit> --evidence-dir <evidence-folder> --record <record.json> --report <report.md> --revisions reports/pages/revisions.json --local-build <built-pages-folder>`.

After deployment, add `--require-pass`. For offline regeneration use `--from-record reports/pages/checks.json --report <report.md> --revisions reports/pages/revisions.json` instead of the live retrieval arguments.
