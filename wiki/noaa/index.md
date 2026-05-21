---
title: "NOAA — National Oceanic and Atmospheric Administration"
tags: [noaa, metocean, wave, wind, current, public-domain]
added: 2026-05-20
last_updated: 2026-05-20
domain: noaa
source_authority: "National Oceanic and Atmospheric Administration (US DOC)"
visibility: public-federal-data
license: public-domain
contribution_status: us_federal_only
last_license_check: 2026-05-20
sources:
  - https://www.noaa.gov/
  - https://www.noaa.gov/disclaimer
---

# NOAA — National Oceanic and Atmospheric Administration

US Department of Commerce agency providing oceanographic, meteorological, and climate data. For offshore energy work, the relevant corpora are wave (WaveWatch III, NDBC buoy data), wind (HRRR, GFS forecasts; NDBC), and current (NCOM, RTOFS).

## Data corpus scope

- **Wave**: NDBC buoy stations (significant wave height, peak period, wind speed); WaveWatch III hindcasts and forecasts
- **Wind**: NDBC station wind speed/direction; HRRR / GFS gridded forecasts; CFSR / ERA5 reanalysis
- **Current**: National Ocean Service tidal currents; NCOM (Navy Coastal Ocean Model); RTOFS (Real-Time Ocean Forecast System)

The library wrapper is `worldenergydata.metocean.cli_fetch`.

## Contribution-status carve-out

NDBC includes ship-of-opportunity reports and some private-sector wind-farm SCADA contributions. Per-page `contribution_status: mixed_private_contributors` flags those datasets — when in doubt, route the summary public and keep full data at `/mnt/ace/`.

## Public-domain status

Verified 2026-05-20: noaa.gov/disclaimer states "information presented on these pages is considered public information and may be distributed or copied" (17 USC §105). `last_license_check: 2026-05-20`; quarterly audit per [#429](https://github.com/vamseeachanta/worldenergydata/issues/429).

## Pages

(none yet — scaffolded 2026-05-20)

## Cross-references

- Library: [`vamseeachanta/worldenergydata`](https://github.com/vamseeachanta/worldenergydata) → `src/worldenergydata/metocean/`
- Raw data: `/mnt/ace/data/` (off-repo)
- Methodology context (vendor-licensed): see private llm-wiki naval-architecture methodology pages by prose reference only
