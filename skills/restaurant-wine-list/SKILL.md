---
name: restaurant-wine-list
description: "Compare every bottle on a restaurant wine list, from one to hundreds, with retail and auction prices to show the markup on each. Use when the user shares a restaurant wine list (photo, PDF, link or pasted text), names a restaurant and asks about its list, asks whether one bottle's price on a restaurant list is fair, or asks which bottle on a list is the best value or least marked up."
---

# Restaurant wine list

The question is markup: how far each bottle's list price sits above what the same wine costs at retail and at auction. The list the user brings comes first; look a restaurant up in WineAuction only when they name one without bringing its list.

## Steps

1. Get the rows.
   - A list the user brings: parse it with [parse-list.md](../wineauction-reference/references/parse-list.md), `offer_type: restaurant`, keeping sections. Then evaluate it with [evaluate.md](../wineauction-reference/references/evaluate.md).
   - A restaurant named without its list: find its `id` with `list_restaurants` ([fields](../wineauction-reference/references/tools/list_restaurants.md)), then call `list_offers` with `offer_type: restaurant`, `merchant_id`, `serving: bottle` and any preference the user gave (colour, region, maximum price). Sort `discount_vs_retail` so the smallest markups come first. Page with `cursor` and save each page.
2. Read prices with [prices.md](../wineauction-reference/references/prices.md). Markup is the negative of `discount_vs_retail_pct`.
3. Present with [report.md](../wineauction-reference/references/report.md), with `--markup` and `--method "Markup is the list price over the retail reference, per 750 ml."`.

## In chat

- The five bottles with the smallest markup over retail, leaving out flagged rows, with list price, retail reference and markup.
- Anything priced far above the rest of the list relative to retail.
- If the user gave a budget, a style or a dish, the best-value bottles that fit it.
- For one bottle the user asks about: its list price, both references and the markup.
- When the user also asks about reviews, call `search_wines` with the matched `lwin7` and `vintage` and quote `reviews[]` as the wine-info skill does.

Restaurant offers need a plan with Restaurant access. When a tool returns a notice that they were skipped, say so; a list the user brings can still be evaluated.
