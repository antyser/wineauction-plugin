---
name: wineauction-reference
description: "Shared reference for the other WineAuction skills: tool fields, how to read the retail and auction reference prices, list parsing, batch evaluation and the HTML report. Read a file here when another WineAuction skill links to it; it is not a task skill on its own."
---

# WineAuction reference

The task skills link here for the parts they share. Read only the file a task skill names.

| File | What it covers |
| --- | --- |
| [references/prices.md](references/prices.md) | The two reference prices, discounts and markups, when to flag a reference as doubtful, links. Every task skill relies on it. |
| [references/parse-list.md](references/parse-list.md) | Turning a PDF, web page, photo or pasted list into priced rows. |
| [references/evaluate.md](references/evaluate.md) | Sending rows to `evaluate_offers` in batches and checking each match. |
| [references/report.md](references/report.md) | Report rows, the HTML renderer, and what to say in chat. |
| [references/design-system.md](references/design-system.md) | Colours, type and layout for any HTML view. |
| [references/tools/](references/tools/) | Inputs and outputs of each tool: [search_wines](references/tools/search_wines.md), [list_offers](references/tools/list_offers.md), [evaluate_offers](references/tools/evaluate_offers.md), [list_auctions](references/tools/list_auctions.md), [list_retail_stores](references/tools/list_retail_stores.md), [list_restaurants](references/tools/list_restaurants.md). |

The renderer is [scripts/render.py](scripts/render.py); it reads its template from `assets/report.html`.

The tools only read data. They cannot bid, buy, check out, list or contact a seller.
