# worldenergydata-wiki

Contract: https://github.com/vamseeachanta/workspace-hub/blob/main/AGENTS.md (the hub repo may not be cloned beside this one; read it at that URL). Minimum rules apply regardless: branch → PR → merge; never push to or rewrite main; never bypass hooks; tests before implementation; no secrets in code.

PUBLIC wiki of derived knowledge from US federal public-domain energy data (BSEE / NOAA / USGS / MMS).
- Only public-domain federal material, except (a) supporting SPE/OTC/JPT source pages per MIGRATION_MANIFEST.md (DOI-only, fair-use quotes ≤ 50 words) and (b) mixed-contributor datasets (`contribution_status: mixed_private_contributors`, e.g. NDBC ship-of-opportunity, wind-farm SCADA): the redacted summary stays public here, the full data stays out of this repo (README.md, MIGRATION_MANIFEST.md). Routing per https://github.com/vamseeachanta/workspace-hub/blob/main/.claude/rules/codes-standards-data-routing.md §6.
- Page frontmatter: follow the full schema in [README.md § Page-shape contract](README.md#page-shape-contract).
- Companion library: worldenergydata. Routing: README.md, MIGRATION_MANIFEST.md, wiki/.
