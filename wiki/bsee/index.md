---
title: "BSEE — Bureau of Safety and Environmental Enforcement"
tags: [bsee, regulator, offshore, oil-gas, public-domain]
added: 2026-05-20
last_updated: 2026-05-20
domain: bsee
source_authority: "Bureau of Safety and Environmental Enforcement (US DOI)"
visibility: public-federal-data
license: public-domain
contribution_status: us_federal_only
last_license_check: 2026-05-20
sources:
  - https://www.data.bsee.gov/
  - https://www.bsee.gov/disclaimer
---

# BSEE — Bureau of Safety and Environmental Enforcement

US Department of the Interior agency responsible for safety and environmental enforcement on the US Outer Continental Shelf, including the Gulf of Mexico, Pacific, and Arctic regions. Created in 2011 from the dissolution of the Minerals Management Service (MMS).

## Data corpus scope

BSEE publishes production data, well records, lease block summaries, incident reports, and inspection results. The full catalog at `worldenergydata/data/modules/bsee/` is ≈2.6 GB and includes:

- Production data (current + paleowells; oil, gas, condensate by lease block)
- Well records (drilling permits, completion reports, plug-and-abandonment)
- Lease block summaries (acreage, water depth, operator history)
- Incident reports (loss of well control, spills, equipment failures)
- Inspection reports (compliance findings, civil penalties)

The library wrapper is `worldenergydata.bsee.api` — `ProductionQuery`, `WellsQuery`, `CompaniesQuery`.

## Public-domain status

Verified 2026-05-20: data.bsee.gov terms of use states "Data on this website is in the public domain" (17 USC §105). Stamp `last_license_check` on every derived page; quarterly audit per [#429](https://github.com/vamseeachanta/worldenergydata/issues/429).

## Pages

(none yet — scaffolded 2026-05-20; first derived pages spawn via `worldenergydata` library work)

## Cross-references

- Library: [`vamseeachanta/worldenergydata`](https://github.com/vamseeachanta/worldenergydata) → `src/worldenergydata/bsee/`
- Raw data: `/mnt/ace/0_mrv/` and `/mnt/ace/data/` (off-repo canonical)
- MMS predecessor: [`wiki/mms/index.md`](../mms/index.md)
- Adjacent regulator (Norway): worldenergydata sodir module (not yet promoted to wiki)
