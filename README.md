# worldenergydata-wiki

Public-domain US federal energy data wiki — derived knowledge pages for BSEE / NOAA / USGS / MMS data corpora.

**Companion repo**: [`vamseeachanta/worldenergydata`](https://github.com/vamseeachanta/worldenergydata) — the Python library that fetches and processes these data sources. This wiki holds the derived knowledge surface (concept pages, methodology notes, dataset-summary pages, cross-references); the library holds the raw data + scrapers.

## License

- **Prose / wiki content**: CC-BY-4.0 ([LICENSE](LICENSE))
- **Any code (scripts, CI, tooling)**: MIT ([LICENSE-CODE](LICENSE-CODE))

The underlying data sources are US federal public-domain works (17 USC §105). Their public-domain status is preserved through derivation.

## Why this exists

`vamseeachanta/llm-wiki` flipped public→private on 2026-05-20 to close the licensing window for vendor-licensed engineering standards (OCIMF, API, DNV, ABS, IACS, ASCE, ASME, etc.). The private posture is correct for those publishers — they're sold by Witherby / Techstreet / IHS Markit and are not freely redistributable.

But it would invert the public-domain status of US federal data to gate BSEE/NOAA/USGS/MMS derived content behind auth. This sibling wiki is the public surface for that material: the wiki tier matches the public-domain status of the underlying data.

Routing rule: [workspace-hub:.claude/rules/codes-standards-data-routing.md §6](https://github.com/vamseeachanta/workspace-hub/blob/main/.claude/rules/codes-standards-data-routing.md).

## Domain coverage

| Domain | Source authority | Status |
|---|---|---|
| [BSEE](wiki/bsee/index.md) | Bureau of Safety and Environmental Enforcement (US DOI) | scaffolded |
| [NOAA](wiki/noaa/index.md) | National Oceanic and Atmospheric Administration (US DOC) | scaffolded |
| [USGS](wiki/usgs/index.md) | US Geological Survey (US DOI) | scaffolded |
| [MMS](wiki/mms/index.md) | Minerals Management Service (US DOI legacy, dissolved 2010 → BSEE / BOEM / ONRR) | scaffolded |

## Page-shape contract

All wiki pages use YAML frontmatter with these fields:

```yaml
---
title: "Page title"
tags: [domain, topic, concept-class]
added: YYYY-MM-DD
last_updated: YYYY-MM-DD
domain: bsee | noaa | usgs | mms
source_authority: "Full agency name"
visibility: public-federal-data
license: public-domain
contribution_status: us_federal_only | mixed_private_contributors
last_license_check: YYYY-MM-DD
sources:
  - https://...   # public URL
  - /mnt/ace/...  # off-repo canonical (raw)
---
```

- `visibility: public-federal-data` distinguishes pages here from `visibility: private-llm-wiki` in the private vendor-licensed wiki.
- `contribution_status: mixed_private_contributors` flags datasets like NDBC ship-of-opportunity reports or wind-farm SCADA contributions; mixed entries route private with a redacted public summary on this side.
- `last_license_check` supports the quarterly license-drift audit per [#429](https://github.com/vamseeachanta/worldenergydata/issues/429).

## Cross-wiki references

- **Public→private** (this repo to llm-wiki): reference by prose only, NOT as Markdown links (would 404 for external readers). Example: "For vendor-licensed standards interpretation see the private llm-wiki under `wikis/marine-engineering/wiki/standards/`."
- **Private→public** (llm-wiki to this repo): use full URLs — they resolve for everyone.

## Contributing

Public-domain status verification is required before any new data source lands. Confirm via the source's terms of use OR by 17 USC §105 inheritance, and stamp `last_license_check` on the page.

See [MIGRATION_MANIFEST.md](MIGRATION_MANIFEST.md) for the post-2026-05-20 migration policy.

## Related

- Issue: [vamseeachanta/worldenergydata#429](https://github.com/vamseeachanta/worldenergydata/issues/429) — the routing-decision issue that created this repo
- Plan: [workspace-hub:docs/plans/2026-05-20-issue-429-worldenergydata-public-data-routing.md](https://github.com/vamseeachanta/workspace-hub/blob/main/docs/plans/2026-05-20-issue-429-worldenergydata-public-data-routing.md)
- Routing rule: [workspace-hub:.claude/rules/codes-standards-data-routing.md §6](https://github.com/vamseeachanta/workspace-hub/blob/main/.claude/rules/codes-standards-data-routing.md)
- Decision doc: [workspace-hub:docs/governance/2026-05-20-public-data-corpus-routing-decision.md](https://github.com/vamseeachanta/workspace-hub/blob/main/docs/governance/2026-05-20-public-data-corpus-routing-decision.md)
