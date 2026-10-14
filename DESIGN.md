---
name: 50 ans au fil de la Durance
description: Récit cartographique en dossier d'archives, avec un plan annexé qui change à chaque pièce
colors:
  chemise: "#16968c"
  chemise-ombre: "#0e6c65"
  chemise-lumiere: "#44b4a9"
  chemise-pale: "#7cc7bd"
  chemise-encre: "#04211f"
  feuille: "#fdfdfb"
  filet: "#d6dcdd"
  encre: "#1b1d1f"
  encre-douce: "#4a5257"
  tampon: "#5a3d9a"
  ruban: "#a8281e"
  dymo: "#151515"
  dymo-texte: "#f2f2ee"
  plan: "#eef0ec"
  eau: "#1f5f99"
  lit: "#a7cde9"
  lac: "#5d9bd0"
  affluent: "#7eaed6"
  canal: "#d26a1e"
  nature: "#3a8a50"
  limite: "#7d8589"
typography:
  display:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, 4.6vw, 4.6rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 72"
  headline:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.9rem, 2.6vw, 2.5rem)"
    fontWeight: 780
    lineHeight: 1.02
    letterSpacing: "-0.01em"
    fontVariation: "'wdth' 78"
  title:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 750
    lineHeight: 1.2
    fontVariation: "'wdth' 85"
  body:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.62
    fontVariation: "'wdth' 100"
  label-dymo:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "0.16em"
    fontVariation: "'wdth' 112"
  label-tampon:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "0.1em"
    fontVariation: "'wdth' 78"
  label-lieu:
    fontFamily: "Archivo, Segoe UI, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 650
    lineHeight: 1
    letterSpacing: "0.09em"
    fontVariation: "'wdth' 85"
  machine:
    fontFamily: "Courier Prime, Courier New, monospace"
    fontSize: "12.5px"
    fontWeight: 400
    lineHeight: 1.4
  machine-mesure:
    fontFamily: "Courier Prime, Courier New, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  feuille: "0"
  ruban: "3px"
  tampon: "4px"
  onglet: "6px"
  poignee: "50%"
spacing:
  marge: "clamp(16px, 4vw, 64px)"
  colonne: "clamp(340px, 34vw, 500px)"
  feuille: "40px"
  feuille-mobile: "22px"
  case: "9px 12px"
  case-cartouche: "8px 12px"
components:
  bouton-dymo:
    backgroundColor: "{colors.dymo}"
    textColor: "{colors.dymo-texte}"
    typography: "{typography.label-dymo}"
    rounded: "{rounded.ruban}"
    padding: "0.7em 1.1em 0.66em"
  bouton-recentrer:
    backgroundColor: "{colors.dymo}"
    textColor: "{colors.dymo-texte}"
    rounded: "{rounded.ruban}"
    padding: "7px 12px"
  tampon:
    textColor: "{colors.tampon}"
    typography: "{typography.label-tampon}"
    rounded: "{rounded.tampon}"
    padding: "0.28em 0.7em 0.22em"
  intercalaire:
    backgroundColor: "{colors.chemise-lumiere}"
    textColor: "{colors.chemise-encre}"
    rounded: "{rounded.onglet}"
    width: "64px"
  intercalaire-pair:
    backgroundColor: "{colors.chemise-pale}"
    textColor: "{colors.chemise-encre}"
  intercalaire-courant:
    backgroundColor: "{colors.feuille}"
    textColor: "{colors.tampon}"
  piece:
    backgroundColor: "{colors.feuille}"
    textColor: "{colors.encre}"
    typography: "{typography.body}"
    rounded: "{rounded.feuille}"
    padding: "{spacing.feuille}"
  piece-pied:
    textColor: "{colors.encre}"
    typography: "{typography.machine}"
    padding: "{spacing.case}"
  cartouche:
    backgroundColor: "{colors.feuille}"
    textColor: "{colors.encre}"
    rounded: "{rounded.feuille}"
    width: "320px"
  etiquette-titre:
    backgroundColor: "{colors.feuille}"
    textColor: "{colors.encre}"
    typography: "{typography.display}"
    padding: "clamp(22px, 2.4vw, 34px)"
---

# Design System: 50 ans au fil de la Durance

## Overview

**Creative North Star: "Le dossier et son plan annexé"**

The page is a fifty-year administrative archive dossier opened on the reader's desk. A flat turquoise pressboard chemise owns whole regions of the screen (the cover, the spine, the back with its bordereau); inside it, white typed sheets carry one numbered pièce each, and behind every sheet lies the live map, drawn like a technical plan with a title-block cartouche. Every institutional mark is one of three flat physical media: violet rubber-stamp ink with a double border for dates, black Dymo tape for actions and the spine label, and a typewriter face for anything measured, referenced or read off the plan.

Density is that of a working file, not a brochure: one sheet in a narrow column, generous paper margins, and a ruled label grid at the foot of each sheet. The map follows one-idea-per-plate semiology: a single thematic subject at full strength, everything else receding, with the same colours as the author's QGIS projects. The world is entirely flat. There is no grain, ink texture, emboss or punched holes; depth comes only from sheets lying on the folder and the folder lifting off the plan.

The page is written in French and set with French typographic spacing: a narrow no-break space (U+202F) before `:` `;` `?` `!`, no-break spaces inside « guillemets », after `n°` and as thousands separators (3 000 ha, 2 000 m³/s).

**Key Characteristics:**
- Turquoise pressboard chemise as a full-bleed surface, never as an accent stripe.
- White sheets (pièces, title sticker, bordereau, cartouche) with square corners.
- Three flat inks only: violet stamp, black Dymo, typewriter black.
- Archivo across a width axis: condensed for headings and stamps, expanded for Dymo tape, normal for reading.
- Courier Prime reserved for cotes, dates, measures, references and live readouts.
- A map drawn as a plan, colour-matched to the QGIS projects, with a cartouche title block.
- Motion that is physical and archival: a cover on a hinge, a river drawing itself downstream, a year retyped digit by digit.

## Colors

A cool archive palette: one saturated turquoise board, near-white paper, near-black inks and a single violet stamp ink, with a separate map semiology of water blues and thematic hues.

### Primary
- **Chemise Turquoise** (chemise): the pressboard folder. Fills the whole cover, the back of the dossier (`dos`) and the page body behind the sheets. It is the theme colour (`<meta name="theme-color">`).
- **Chemise Ombre** (chemise-ombre): the folder's darker fold; used for the scrollbar thumb and as the tone of the folder's own shadows.
- **Chemise Lumière** (chemise-lumiere) and **Chemise Pâle** (chemise-pale): the intercalaire year tabs, alternating odd and even so the tab stack reads as separate cards.
- **Encre de Chemise** (chemise-encre): dark teal ink printed directly on the folder (the window caption, tab numerals).

### Secondary
- **Violet Tampon** (tampon): rubber-stamp ink. Date stamps, the cover stamp, the "Dossier clos" stamp, plan numbers in the cartouche, ordered-list markers in the method, the current tab's numeral, link underlines and hover, focus rings, text selection. On the map it is the institutional colour: the founding perimeter, riverside communes, intercommunalités and the syndicate's headquarters marker.

### Tertiary
- **Ruban Rouge** (ruban): levées and digues on the map; on the page, only for fields still to be completed before publication, with a dashed underline.

### Map semiology (shared with the QGIS projects)
- **Plan** (plan): the paper ground of the map and the halo around place labels.
- **Eau** (eau): the Durance trace, the single strongest line on every plate; also the italic water-name labels.
- **Lit** (lit), **Lac** (lac), **Affluent** (affluent): wetted bed, Serre-Ponçon reservoir, tributaries and the Rhône, all lighter than the main trace.
- **Canal** (canal): the EDF canal, dashed.
- **Nature** (nature): Natura 2000 sites; filled for the Habitats directive, dashed outline for the Birds directive.
- **Limite** (limite): dashed departmental boundaries.
- Dams are filled `encre` dots with a white ring; Vigicrues stations are white dots with an `encre` ring.

### Neutral
- **Feuille** (feuille): every sheet, the cartouche, the current tab, tooltips.
- **Encre** (encre): text ink and every rule of the cartouche and label grid.
- **Encre Douce** (encre-douce): secondary text (subtitles, sources line, readout, notes).
- **Filet** (filet): light hairlines inside a sheet (cote rule, dashed measure rule, source list rules).
- **Dymo** (dymo) and **Dymo Texte** (dymo-texte): the black tape and its off-white embossed lettering.

### Named Rules
**The One Board Rule.** Turquoise is a surface, never a highlight. It owns whole regions (cover, back, body, tabs); it never appears as text colour, button fill or border accent on a white sheet.

**The Single Stamp Ink Rule.** Violet is the only accent ink on the page. Anything stamped, numbered by the archive, linked or focused is violet; no second accent hue is introduced on the sheets.

**The Plan Semiology Rule.** Map colours come from the shared QGIS palette and keep their meaning on every plate and in every legend swatch. A thematic layer is shown at its full opacity only on the pièce it belongs to; the rest recede or vanish.

## Typography

**Display Font:** Archivo (variable, width 62–125%), with Segoe UI, system-ui
**Body Font:** Archivo at normal width (100%)
**Label/Mono Font:** Courier Prime (400, 700), with Courier New

**Character:** One grotesque stretched across its width axis plays three roles: condensed and heavy for headings and stamps, expanded and spaced for Dymo tape, normal for reading. Courier Prime is the dossier's typewriter.

### Hierarchy
- **Display** (800, width 72%, clamp(2.5rem, 4.6vw, 4.6rem), line-height 0.94): the cover title sticker; the bordereau heading uses the same voice at clamp(2.2rem, 4vw, 3.4rem), line-height 1. Balanced wrapping.
- **Headline** (780, width 78%, clamp(1.9rem, 2.6vw, 2.5rem), line-height 1.02): each pièce's title; leaves 120px on the right for its date stamp on desktop.
- **Title** (750, width 85%, 16px): the cartouche plan title (13.5px on phones).
- **Body** (400, 17px, line-height 1.62; 16px on phones): pièce text, max 62ch; cover subtitle max 40ch.
- **Dymo label** (800, width 112%, uppercase, letter-spacing 0.16em; the spine uses 0.26em): primary action, spine tape, map "Recentrer le plan" tape.
- **Stamp** (800, width 78%, 1rem, uppercase, letter-spacing 0.1em): dates and closing marks.
- **Place label** (650, width 85%, 11px, uppercase, letter-spacing 0.09em): towns on the map, with a `plan`-coloured halo. Water names switch to italic 500, 13px, sentence case, in `eau`.
- **Typed** (Courier Prime 400, 11.5–15px): the label grid, cote line, window caption, measures ("Sur le plan : …" at 14px), cartouche readout and scale value, licence, signature, bordereau register heads (700, 13px, uppercase, 0.08em). Bold 700 marks the pièce number and the year cells.

### Named Rules
**The Typewriter Rule.** Courier Prime types only what an archivist would type: cotes, dates, numbers, references, sources, measured values and the live readout. Narrative prose and pièce headings are never set in it.

**The Width Axis Rule.** Hierarchy is carried by width as much as size: condensed (72–85%) for headings and stamps, 100% for reading, 112% for tape. Don't introduce a second sans family for any of these roles.

## Layout

The map is fixed full-screen behind everything (`plan` ground). On desktop the dossier is a single column on the left, `colonne` wide plus the `marge`, with 30svh of lead-in, 78svh between sheets so the map has the screen to itself between pièces, and 40svh of tail. Only one pièce is "active"; inactive sheets sit at 0.82 opacity. The cartouche is pinned bottom-right, clear of the tab rail; the intercalaire tabs are pinned to the right edge, vertically centred, protruding 12px less than the current tab.

The cover is 100svh (min 600px): a die-cut window (46vw from the left, 9svh from the top, 76svh tall, 5vw from the right edge) shows the live map; the text block (title sticker and Dymo button) sits in the remaining left column, the Dymo spine label reads bottom-to-top on the left edge. The back (`dos`) is a full-height turquoise region centring the bordereau sheet (max 1040px, two columns 1.15fr / 1fr).

Camera framing is computed from the free area: map padding excludes the dossier column, the tab rail and the cartouche, so every plate's subject lands in the visible part of the map.

**Phones (max-width 820px):** the map is pinned to the top 48svh with a 1.5px `encre` bottom rule and the pièces scroll beneath it; tabs become a horizontal strip hanging from the top edge; the cartouche goes compact across the top (title and year cells on one row, legend wrapping on a second, north arrow, scale, readout and sources hidden); sheets use 22px padding with 36svh gaps, are always fully opaque, and the date stamp moves to the top-right corner above the heading. The cover window shrinks to a 30svh band and the spine label is hidden. The label grid collapses to two columns with Réf. and Sources on full-width rows; the bordereau becomes one column. Map drag-pan is disabled on phones so the page scrolls.

## Elevation & Depth

Flat materials, physical stacking. Surfaces carry no texture or gradient; depth only says "this sheet lies on that folder". Sheets cast one soft paper shadow; tapes and tabs cast a small contact shadow; the cover gains a shadow as it lifts.

### Shadow Vocabulary
- **Feuille** (`0 1px 1px rgb(4 33 31 / .16), 0 18px 36px -18px rgb(4 33 31 / .6)`): pièces, title sticker, bordereau.
- **Ruban** (`0 2px 3px rgb(0 0 0 / .35)`, hover `0 8px 14px -6px rgb(0 0 0 / .5)`): Dymo button.
- **Cartouche** (`0 2px 4px rgb(4 33 31 / .24)`): the plan title block, nearly flush on the plan.
- **Onglet** (`inset 0 0 0 1px rgb(4 33 31 / .25), -2px 2px 6px -2px rgb(0 0 0 / .3)`): intercalaire tabs.
- **Couverture levée** (`0 calc(var(--ouverture) * 40px) 60px -20px rgb(4 33 31 / .5)`): grows as the cover hinges open.
- **Dos** (`0 -30px 60px -30px rgb(4 33 31 / .55)`): the back of the folder sliding over the plan.

### Named Rules
**The Flat Material Rule.** Board, paper, ink and tape are flat colour. No grain, noise, ink bleed, emboss, punched holes or paper curl.

## Shapes

Sheets, the cartouche and the label grid are square-cornered rectangles ruled in `encre`. Small radii belong only to physical objects that have them: Dymo tape (3px), rubber stamps (4px, with a 3px double border in the ink colour), intercalaire tabs (6px on the free edge only). The title sticker has an inset double rule (1px border plus 1px outline 4px inside, 7px from the edge). Stamps sit rotated (−6° on odd pièces, 4° on even, −8° on the cover, −10° for "Dossier clos") and print with `multiply`. The comparison-slider handle is the only circle.

## Components

### Dymo button (primary action)
Black tape with embossed off-white capitals.
- **Shape:** 3px radius, padding 0.7em 1.1em, trailing stroked SVG arrow.
- **Hover / Focus:** lifts 2px with a deeper shadow over 0.25s; focus is the global 2px violet outline offset 3px.
- **Variants:** the spine label (vertical, non-interactive) and the "Recentrer le plan" tape on the cartouche (11.5px, appears only after the reader moves the map).

### Tampon (stamp)
Flat violet ink, double border, uppercase condensed text, slight rotation, multiply blending. Used for the cover date range, each pièce's date and "Dossier clos". Decorative (`aria-hidden`); the same date is always also in the label grid.

### Intercalaires (navigation)
Year tabs protruding from the folder's edge, Courier Prime 700 13px. Odd and even tabs alternate between the two light turquoises; hover slides a tab out; the current tab (`aria-current="step"`) becomes paper with violet numerals and sits flush. A pièce without a year of its own leaves no tab current. Tabs and cartouche fade in once the cover is mostly open and fade out on the back of the dossier.

### Pièce (card)
- **Corner Style:** square.
- **Background:** `feuille`, Feuille shadow.
- **Internal Padding:** 40px sides and top (22px on phones).
- **Measure block:** "Sur le plan :" paragraph in typed 14px under a dashed `filet` rule, stating what the map shows and how it was measured.
- **Label grid (piece-pied):** a full-bleed ruled footer, 1.5px `encre` top rule, cells separated by 1px `encre`: N° (bold), date range, Réf., then Sources on a full-width row with violet links. Every pièce carries all four cells.

### Cartouche (signature component)
The plan's title block, 320px, ruled in `encre`: plan title row, legend (SVG swatches 28×14 drawn from the same colour, width and dash as the map layer), a footer row with the plan number in violet, the year in four bordered typed cells, a north arrow that rotates with the bearing, and a black-and-white scale bar with a typed value; then the live readout (latitude, longitude, zoom, French number formatting) and the sources line. A pale alert row appears only when the map or data cannot load.

### Title sticker (étiquette)
White label on the cover: inset double rule, display title, subtitle, a `filet` rule, the typed cote line, and the cover stamp on its own line aligned right.

### Map labels and tooltips
Place labels are HTML markers in the dossier's type (see Typography), fading in per plate. The headquarters marker is a 9px violet square. Tooltips are small paper boxes with a 1px `encre` border, 2px radius, no tip.

### Calque (before/after slider)
A 1950–1965 aerial layer clipped over current imagery, divided by a 2px white line; the handle is a 40px paper circle with an `encre` ring and chevrons, flanked by typed date tags. Keyboard: arrows (Shift for larger steps), Home, End.

### Motion
- **Cover hinge:** the cover rotates on its top edge from 0 to −34° (perspective 1800px) over the first 0.9 viewport of scroll.
- **River drawing:** on load the Durance trace draws itself downstream via a line-progress gradient over 4.2s, ease-out cubic.
- **Year strike:** changed year digits are retyped one cell at a time (70ms stagger, 0.32s drop-in); unchanged digits stay still and the cartouche never reflows.
- **Camera flights:** each pièce flies the camera to its plate (2.6s, curve 1.5) while layer opacities cross-fade over 0.8s.
- **Easing:** `cubic-bezier(.16, 1, .3, 1)` for every UI transition.
- **Reduced motion:** no smooth scrolling, no cover rotation, no UI transitions or year animation; the camera jumps instead of flying and the river appears fully drawn.

## Do's and Don'ts

### Do:
- **Do** let the turquoise chemise own entire regions (cover, back, page ground) and put content on white sheets.
- **Do** give every pièce the same label grid: N°, date, Réf., Sources, typed in Courier Prime.
- **Do** stamp dates in flat violet with a 3px double border and a slight rotation, and repeat the same date in text.
- **Do** keep map colours identical to the QGIS palette and to the cartouche legend swatches; one thematic subject at full strength per plate.
- **Do** set French text with a narrow no-break space before `:` `;` `?` `!` and no-break spaces in numbers, after `n°` and inside « guillemets ».
- **Do** change Archivo's width, not its family, to move between heading, reading and tape voices.
- **Do** give every motion an instant equivalent under `prefers-reduced-motion`.

### Don't:
- **Don't** add grain, noise, ink texture, emboss, punched holes or any simulated paper material; all materials are flat.
- **Don't** use turquoise as an accent on a sheet or violet as a surface fill on the page.
- **Don't** set narrative paragraphs or pièce headings in Courier Prime.
- **Don't** round sheets, the cartouche or the label grid.
- **Don't** introduce a second accent hue on the sheets; red is reserved for digues on the map and unfinished fields.
- **Don't** use any SMAVD logo or brand identity; the page is an independent work.
