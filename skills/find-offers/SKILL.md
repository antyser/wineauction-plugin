---
name: find-offers
description: The user has no offers yet and wants offers for the wines they want: named wines, a producer, a region or appellation, or a style. Shows market references and the best current offers; can repeat on a schedule. Use for "any good Bienvenues-Batard-Montrachet out there", "what is Roulot going for", "check Rousseau weekly".
---

# Find offers

The user has no offers; find offers for what they want. The tools come from the WineAuction connector. If they already hold offers (a list, a newsletter, a named auction or store), use the check-offers skill instead.

## Steps

1. Turn the request into wine filters: names or `lwin7`, `producer`, `region`, `appellation`, `color`, vintage range. `search_wines` filters only on the wine, never on offer fields such as price, discount or seller. Field meanings are in [references/search_wines.md](references/search_wines.md).
2. Call `search_wines`. Each wine carries its `retail` and `auction` references and up to two `best_offers`. Page with `cursor` if more wines are wanted.
3. For every offer of a wine the user picks, call `list_offers` with that wine's `wine_id` (optionally `vintage`); the offer fields are in [../check-offers/references/list_offers.md](../check-offers/references/list_offers.md). Save each response to disk.
4. Judge deals from each offer's `discount_vs_retail_pct` and `discount_vs_auction_pct`, and apply the user's price band or discount threshold. Treat the auction reference as weak when `auction.sale_count` is 1–2, and either reference as doubtful when the two differ by more than 3×.

If the user instead wants one auction, store or restaurant scanned by price or discount, use check-offers.

## Present

Up to about 10 offers: answer in chat. More: one HTML page, built with the check-offers renderer. That script lives in the sibling skill, so from this skill's directory run:

```
python3 ../check-offers/scripts/render.py rows.json report.html --title "..." --eyebrow "WineAuction · ..." --lede "..." --method "..."
```

`rows.json` can be the raw `search_wines` `wines` list (the script makes one row per best offer, with the wine's name and references) or the `list_offers` `offers` list. To control the keys, build one row per offer:

| key | from |
| --- | --- |
| `name`, `vintage` | `wine_name`, `vintage` |
| `group` | appellation or producer |
| `seller`, `ref` | `seller_name`; "Lot <number>" or a SKU |
| `bottles`, `size_ml` | `bottles`, `bottle_size_ml` |
| `price_usd` | `price_per_bottle_usd` |
| `retail_usd`, `retail_live`, `auction_usd`, `auction_sales` | the wine's `retail` and `auction` views |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | as returned on the offer |
| `url`, `wineapp_url`, `ends_at` | the seller's page, the wine's (`wineapp_wine_url`) or offer's (`wineapp_url`) wineauction.ai page, `auction_end_time` |
| `flags` | doubts |

In chat list only the wines with an offer 20% or more below either reference, with the price, both references and the link; add totals. Say that an auction discount is at the current or opening bid.

## Scheduling

When the user wants a recurring watch and the client supports scheduled tasks, suggest a weekly one that reruns the same `search_wines` query. Report only deals that are new or better than last time, comparing against the previous run's results in the conversation. Do not store the user's watch list anywhere else.

## Reading results

- `_usd` fields are US dollars per 750 ml; auction prices include the buyer's premium.
- Discount: positive means cheaper than the reference. Always say which reference you quote.
- `retail` and `auction` are the two references; either is null when there is no data. `auction` is this exact vintage only, so null means it never sold.
- Link a wine with `wineapp_url` (on `search_wines` results) and an offer with its own `wineapp_url`.
