# Profile themes

The profile README shows a different look every day. Each folder here is one
complete look: a banner (`header.svg`), five section headers (`section-*.svg`)
and a closing strip (`footer.svg`).

## How the rotation works

1. [`theme.yml`](../../.github/workflows/theme.yml) runs once a day. It picks
   the day's theme by its position in [`rotation.txt`](rotation.txt) and copies
   that folder's seven images to the `theme` branch.
2. [`README.md`](../../README.md) embeds its images from the `theme` branch, so
   the README itself never changes.
3. The workflow also runs when anything in this folder changes on `dev`, so new
   art goes live straight away.

A new theme can take a few minutes to appear, because GitHub caches images.

## Changing it

| To | Do this |
|---|---|
| Show one theme right now | Actions → **Profile theme** → **Run workflow**, and type the folder name. It stays until the next daily run. |
| Keep one theme for good | Leave only that theme's line in `rotation.txt`. |
| Change the order, or drop a theme | Edit `rotation.txt`. |
| Rotate more or less often | Change the `cron` line in `theme.yml`, and the `86400` (seconds in a day) beside it to match. |
| Stop rotating | Disable the **Profile theme** workflow under Actions. The last theme shown stays. |

## The themes

| Folder | Look |
|---|---|
| `field-dossier` | Amber CRT dossier with a sonar sweep |
| `summit-ascent` | Line-art mountain with a climbing route, in Summit Tec navy and gold |
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

Add a folder with the same seven file names, then add its name to
`rotation.txt`. The workflow refuses to publish a folder that is missing a file.

The images must work as plain images: no scripts, nothing loaded from elsewhere,
and well-formed XML. A file that is not well-formed shows as a blank image.
