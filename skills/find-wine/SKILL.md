---
name: find-wine
description: "Use when the user expresses interest in finding information about wines: a named wine, producer, vintage, region, or appellation; retail or auction prices; historical auction sales; available offers; or professional reviews. Search wines and relevant offers to answer the request."
---

# Find wine

Use this skill for information about wines and their markets, whether or not the user already has offers. It can return retail and auction references, current offers, closed auction lots, and critic reviews when WineAuction provides them. If the user gives an offer or names an auction, store, or restaurant list and asks you to assess its prices against the market, use the check-offers skill.

## Steps

1. Turn the request into wine filters: names or `lwin7`, `producer`, `region`, `appellation`, `color`, vintage range. `search_wines` filters only on wine attributes, never on offer fields such as price, discount or seller. Field meanings are in [references/search_wines.md](references/search_wines.md).
2. Call `search_wines` for wine details, retail and auction references, and its best current offers. Use `reviews[]` when the user asks about professional reviews; include the author, returned review text (which may include a score), and link when available. Reviews may be absent. Page with `cursor` if more wines are wanted.
3. When the user asks for available current offers beyond `search_wines`' two-offer sample, or needs seller, price, or discount filters, call `list_offers` with the matched wine's `wine_id` and optional `vintage`. The offer fields are in [../check-offers/references/list_offers.md](../check-offers/references/list_offers.md). Save each response to disk.
4. When the user asks for historical auction sales, call `list_offers` with the wine's `wine_id`, `offer_type: auction`, `status: closed`, and `sort: recent`; add `vintage` when requested. Only rows with `auction_status: sold` are completed sales. Report the sale date and returned price fields, and distinguish prices that include the buyer's premium from hammer prices. Do not count unsold lots as sales.
5. Assess discounts only when the user asks whether an offer is a deal or gives a price/discount threshold. Apply the user's threshold. For a deal request without a threshold, retain the existing presentation rule of showing offers at least 20% below either reference. Market prices, historical sales, current offers, and review requests do not need to pass that deal filter. Treat the auction reference as weak when `auction.sale_count` is 1–2, and either reference as doubtful when the two differ by more than 3×.

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

For a market-information request, report the requested references and relevant offers without filtering by discount. For a deal assessment, include the offers that meet the user's threshold or the 20% default, with the price, both references, and link; add totals. Say that a live auction discount is measured at the current or opening bid.

## Scheduling

When the user wants a recurring watch and the client supports scheduled tasks, suggest a weekly one that reruns the same `search_wines` query. Report only deals that are new or better than last time, comparing against the previous run's results in the conversation. Do not store the user's watch list anywhere else.

## Reading results

- `_usd` fields are US dollars per 750 ml; auction prices include the buyer's premium.
- Discount: positive means cheaper than the reference. Always say which reference you quote.
- `retail` and `auction` are the two references; either is null when no reference data is available. A null auction reference does not show whether the wine has sold; use closed auction lots to answer sale-history questions.
- Link a wine with `wineapp_url` (on `search_wines` results) and an offer with its own `wineapp_url`.
