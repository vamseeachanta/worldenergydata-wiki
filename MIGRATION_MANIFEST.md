---
title: "Migration manifest — post-2026-05-20 llm-wiki privacy flip"
added: 2026-05-20
last_updated: 2026-05-20
domain: cross-domain
---

# Migration manifest — public-data corpus routing

Post the 2026-05-20 `vamseeachanta/llm-wiki` privacy flip, this manifest records what moves where, what stays, and the policy each artifact follows.

## Scope of migration

**This repo is NEW (2026-05-20)**, scaffolded to be the public sibling for BSEE / NOAA / USGS / MMS derived knowledge. As a NEW repo, this is not a content-relocation migration but a forward-routing baseline.

## What MOVES (decision-pending — forward-routing baseline)

The default policy is forward-routing only (no migration of existing pages). However, the private llm-wiki holds at least two substantive BSEE/regulator-derived pages dated before this routing decision:

- `vamseeachanta/llm-wiki:wikis/asset-management/wiki/sources/bsee-2024-deepwater-dynamic-pipeline-riser-life-extension.md` — substantive (100+ line) BSEE-derived analysis on deepwater dynamic-pipeline-riser life extension.
- `vamseeachanta/llm-wiki:wikis/marine-engineering/wiki/sources/hwcg-2026-bsee-boem-deepwater-containment-tour.md` — derivative BSEE/BOEM containment-tour source page.

**Migration disposition (deferred to per-page decision):** these pre-date the 2026-05-20 routing decision and were authored under the old "public llm-wiki" assumption. Two options for each:

1. **Migrate to `worldenergydata-wiki`** — public-domain BSEE substrate, no vendor-licensed admixture, no client identifiers → fits the new public sibling.
2. **Stay in private llm-wiki with rationale** — if the page mixes BSEE substrate with vendor-licensed standards interpretation or client-deliverable context, the conservative private routing applies (per Option C escape hatch in the decision doc).

Per-page disposition recorded as a follow-on issue (not this migration). No content is moved in the immediate scaffold step.

## What STAYS at its current location

| Artifact | Location | Why it stays |
|---|---|---|
| Raw federal data files | `/mnt/ace/0_mrv/`, `/mnt/ace/data/` (and similar `/mnt/ace/` paths) | Off-repo canonical store; not duplicated into git |
| `worldenergydata` Python library | `vamseeachanta/worldenergydata` (PUBLIC, MIT) | Library is the data-fetch + processing surface; this wiki holds the derived knowledge |
| GTM client reports | `worldenergydata/reports/gtm/` (6 reports) | Already public; clients cite library paths directly; no re-homing |
| BSEE catalog YAML | `worldenergydata/data/catalog.yaml` v2.1.0 | Canonical catalog stays with the library |
| BSEE binary stores | `worldenergydata/data/modules/bsee/` (2.6 GB) | Library-internal storage; not wiki content |
| Papkov BSEE citation source-page | `vamseeachanta/llm-wiki:wikis/drilling-engineering/wiki/sources/papkov-bsee-citation.md` | Pre-flip metadata-only page; URL-only; cross-domain content (drilling-engineering not BSEE-specific); not migrating |

## What LANDS HERE going forward

| Artifact class | Lands at | Notes |
|---|---|---|
| New BSEE-derived analyses | `wiki/bsee/<topic>.md` | Use the page-shape contract from README.md |
| New NOAA-derived methodology / dataset summaries | `wiki/noaa/<topic>.md` | NOAA mixed-contributor datasets (e.g., NDBC ship-of-opportunity) carry `contribution_status: mixed_private_contributors` — route summary public, full data stays at `/mnt/ace/` |
| New USGS-derived material | `wiki/usgs/<topic>.md` | Geological surveys, oil-and-gas reserve assessments, mineral economics |
| New MMS legacy material | `wiki/mms/<topic>.md` | Pre-2010 MMS publications under 17 USC §105 |
| New academic papers cited as supporting context (SPE, OTC, JPT) | `wiki/<domain>/sources/<paper>.md` | DOI-only references; verbatim quoting under fair-use ≤ 50 words per source |

## What ROUTES PRIVATE instead

| Artifact class | Lands at | Why private |
|---|---|---|
| Vendor-licensed standards (OCIMF, API, DNV, ABS, IACS, etc.) | `vamseeachanta/llm-wiki:wikis/<domain>/wiki/standards/` | Vendor copyright; settled by routing rule §1-5 |
| Client-project content (per private deny-list) | private client-scoped wikis | Client confidentiality — specific project identifiers held off-repo |
| Derived analyses with mixed public/vendor substrate | `vamseeachanta/llm-wiki` | Conservative routing when public-domain status is not 100% clear |

## Decision-revision triggers

This routing decision is revisited if:

1. **A federal data source changes its TOU** to introduce restrictions (e.g., BSEE adds a non-redistribution clause). Mitigation: per-source `last_license_check` frontmatter + quarterly audit.
2. **The maintenance burden of two repos** becomes real — e.g., cross-link discipline keeps breaking. Mitigation: revisit at the 6-month mark (2026-11-20). If the burden is real, options are (a) absorb this wiki into `worldenergydata/wiki/`, or (b) collapse to private and accept the GTM-citation friction.
3. **Client-deliverable patterns** demand a per-deliverable visibility choice that this routing doesn't support. Mitigation: file a sibling routing-decision issue, don't unilaterally amend §6.

## Related

- Routing rule: [workspace-hub:.claude/rules/codes-standards-data-routing.md §6](https://github.com/vamseeachanta/workspace-hub/blob/main/.claude/rules/codes-standards-data-routing.md)
- Decision doc: [workspace-hub:docs/governance/2026-05-20-public-data-corpus-routing-decision.md](https://github.com/vamseeachanta/workspace-hub/blob/main/docs/governance/2026-05-20-public-data-corpus-routing-decision.md)
- Plan: [workspace-hub:docs/plans/2026-05-20-issue-429-worldenergydata-public-data-routing.md](https://github.com/vamseeachanta/workspace-hub/blob/main/docs/plans/2026-05-20-issue-429-worldenergydata-public-data-routing.md)
- Origin issue: [vamseeachanta/worldenergydata#429](https://github.com/vamseeachanta/worldenergydata/issues/429)
- Umbrella: [vamseeachanta/workspace-hub#2774](https://github.com/vamseeachanta/workspace-hub/issues/2774)
