# WineAuction design system

The report template already uses these tokens. Use them when adjusting the template or building another view, so it matches wineauction.ai.

| Token | Light | Dark |
| --- | --- | --- |
| background | #fbf8f1 | oklch(0.14 0.012 28) |
| foreground | #231a1c | oklch(0.96 0.008 75) |
| card | #ffffff | oklch(0.2 0.012 28) |
| primary (links, focus) | #c2452a | oklch(0.7 0.13 32) |
| muted | #f2ebdd | oklch(0.275 0.012 28) |
| muted foreground | #7a6e66 | oklch(0.698 0.008 32) |
| border | #ece3d3 | oklch(1 0 0 / 9%) |

Discount badges:

| Discount | Badge |
| --- | --- |
| 30% or more below the reference | strong sage (`g3`) |
| 10% or more below the reference | light sage (`g2`) |
| 10% or more above the reference | red (`r`) |
| Doubtful reference | amber (`flag`) |

Type:

| Use | Font | Size |
| --- | --- | --- |
| Headings | Cormorant Garamond 600 | |
| Body | Geist 400/500 | 14px |
| Lot numbers | Geist Mono | 12px |
| Numbers | tabular | |

Layout:
- One column, max width 1180px, radius 8px, 1px borders, no shadows.
- Order: picks as cards, then one table with the filters above it.
