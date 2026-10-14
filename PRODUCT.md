# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML, CSS and JavaScript with MapLibre GL JS for the map (chosen by the user).
No build step. Data comes from QGIS as GeoJSON, produced by the scripts in `scripts/`.
QGIS and qgis2web remain the data preparation and exploration tools.

## Users

Primary: recruiters and hiring managers in geomatics, GIS, water management and local
government who open the author's portfolio or application link and judge, in a few
minutes, whether the author can deliver professional web cartography.

Secondary: anyone interested in the Durance and the SMAVD who reaches the published page.

## Product Purpose

A published StoryMap telling 50 years of the Syndicat mixte d'aménagement de la vallée
de la Durance (SMAVD, 1976-2026) through scroll-driven maps. It is the author's
portfolio piece for job applications: success means a reader finishes the story,
understands the river and the institution, and comes away convinced of the author's
skills in data preparation (QGIS), cartographic semiology and web mapping.

## Positioning

A real, data-backed story on a real river, built end to end by one person: public
geodata pulled and processed with reproducible PyQGIS scripts, then told with a custom
scroll-driven MapLibre map instead of a template tool (StoryMaps, qgis2web alone).

## Operating Context

- Read on desktop by recruiters, often from a link in an application or portfolio;
  must also hold up on a phone.
- Published as a static site (the author also has a portfolio project), so no server code.
- Inspired by a real internship offer at the SMAVD (Mallemort), but made independently.

## Capabilities and Constraints

- Data: IGN Géoplateforme (BD TOPO, ADMIN EXPRESS, aerial photos 1950-1965 and current),
  INPN Natura 2000, Vigicrues. Licence Ouverte Etalab 2.0, credited on the page.
- Chapters follow `docs/story-board.md`; dated facts and sources in `docs/frise_chronologique.csv`.
- Undecided: final hosting address; the sixth chapter ("Et demain ?") content.

## Brand Commitments

- Independent project: not an official SMAVD publication. No SMAVD logo or brand identity,
  and the page states that it is an independent work based on public sources.
- Published facts must be sourced. Unverified items from the working timeline are either
  verified, phrased with explicit caution, or left out of the published version.

## Evidence on Hand

- Real geodata in `donnees/referentiel.gpkg` and `donnees/smavd_50ans.gpkg`.
- Sourced history: Bouches-du-Rhône departmental deliberations, BANATIC, smavd.org.
- No photos, archive scans, interviews or testimonials yet: do not fabricate any.

## Product Principles

1. Every claim on the page is sourced or clearly framed as uncertain.
2. The map carries the story: each chapter changes what the map shows, not decoration.
3. Show the craft: the method (QGIS, scripts, semiology) is visible to a recruiter.
4. Fast and readable on a recruiter's laptop and on a phone.

## Accessibility & Inclusion

French-language page; text must stand on its own without the map (each chapter's
message readable as text), keyboard navigable, and respect reduced-motion preferences.
