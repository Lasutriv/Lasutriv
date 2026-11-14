# Profile themes

The profile README changes look by itself, every ten seconds, through all of
the themes in this folder. Each folder here is one complete look: a banner
(`header.svg`), five section headers (`section-*.svg`) and a closing strip
(`footer.svg`).

## How it works

[`assets/rotate/`](../rotate/) holds seven files, one for each image on the
page. Each file contains every theme and plays them in turn, so the README embeds
just those seven. There is no workflow, script or server behind it: GitHub shows
the files as images and the images animate themselves.

- Each theme gets ten seconds, with a half-second dissolve to the next one, and
  its intro (typing, drawing, stamping) plays again on every turn.
- All seven images use the same order and timing, so they change look together.
  Each image starts its clock when the browser loads it, so they can drift apart
  a little over time.
- The order is [`rotation.txt`](rotation.txt). The first theme is what visitors
  see when the page loads, and what shows if their browser asks for reduced
  motion or cannot play animation.

## Changing it

| To | Do this |
|---|---|
| Keep one look for good | Leave only that theme's line in `rotation.txt`, then regenerate the files below. With one theme the files simply show it. |
| Reorder, add or drop a look | Edit `rotation.txt`, then regenerate. |
| Change how long each look stays | Regenerate with another turn length. |

The files in `assets/rotate/` are generated from the folders here by Summit Tec's
README theme tooling (`src/rotate.ts` in `foundation-development-kit`), so
regenerate them there rather than editing them by hand:

```sh
node src/rotate.ts profiles/lasutriv.json <this repo>/assets/themes <this repo>/assets/rotate
```

Add `--seconds 15` for a different turn length. Commit the seven files that come
out.

## The themes

| Folder | Look |
|---|---|
| `summit-ascent` | Line-art mountain with a climbing route, in Summit Tec navy and gold |
| `field-dossier` | Amber CRT dossier with a sonar sweep |
| `neon-arcade` | Synthwave arcade marquee over a rolling grid |
| `castaway-chart` | Antique sea chart with a route to an X |
| `mission-control` | Flight-ops console with a mission clock |
| `royal-charter` | Illuminated charter on vellum with a wax seal |
| `low-poly-dawn` | Faceted mountain range at sunrise |
| `paper-dossier` | Typewritten memo in a manila folder |
| `pixel-quest` | 16-bit RPG status screen |
| `parchment-record` | Summit Tec document on parchment with a gold seal |
| `circuit-trace` | Green circuit board with signal pulses |
| `directorate-poster` | Constructivist poster on cream paper |
| `observatory` | Night sky with a mountain-shaped constellation |
| `hazard-protocol` | Acid-yellow warning label |
| `glass-aurora` | Frosted glass over drifting coloured light |
| `blueprint` | Cyanotype drafting sheet |
| `navy-sonar` | The sonar dossier in Summit Tec navy and gold |

## Where the art comes from

- **`field-dossier`** is drawn by [`generate.py`](field-dossier/generate.py),
  which writes its files next to itself: `python3 field-dossier/generate.py`.
- **The other sixteen** are drawn by Summit Tec's README theme tooling and
  committed here as finished files. Regenerate them there rather than editing
  them by hand.
- **Fonts.** See [`FONTS.md`](FONTS.md) for the embedded fonts and their licences.

## Adding a theme

Add a folder with the same seven file names, then add its name to `rotation.txt`
and regenerate. All seven files in a folder must be the same size as their
counterparts in the other folders, and a theme's intro has to finish within its
ten seconds.

The images must work as plain images: no scripts, nothing loaded from elsewhere,
and well-formed XML. A file that is not well-formed shows as a blank image.
