---
name: where-to-buy
description: "List current offers across retail stores, live auctions and restaurants for a specific wine, or for wines matching a producer, region, colour and price, each against the market references. Use when the user asks where a wine is available now, who has it in stock, the lowest current price for it, which wines of a region or producer are currently offered below market or under a budget, or wants a recurring check for new offers."
---

# Where to buy

## Steps

1. Scope the search.
   - A specific wine: identify it with `search_wines` ([fields](../wineauction-reference/references/tools/search_wines.md)) and take its `wine_id` (and vintage). When several wines match, show the top few and ask which one only if the user clearly means one.
   - A producer, region, appellation or colour ("white Burgundy under $200", "Roulot"): use those as `list_offers` filters directly, or pass up to 10 named wines as `wines`.
2. Call `list_offers` ([fields](../wineauction-reference/references/tools/list_offers.md)) with the scope, leaving `offer_type` out for every type or setting it to what the user wants, plus their filters: `max_price_usd`, `bottle_size_ml`, `in_stock`, `pre_arrival`. For a request about value or deals, add `min_discount_pct` and sort by `discount_vs_retail` or `discount_vs_auction` with `offer_type` set; when the user gave no threshold, 20 is a reasonable default and say you used it. Page with `cursor` and save each page.
3. Read prices with [prices.md](../wineauction-reference/references/prices.md). An auction lot's price is its current or opening bid, not a price you can pay.

## In chat

- The offers ordered by price per 750 ml (or by discount for a value request): wine, seller and city, type, bottles and size, price, both discounts, the seller link and the wineauction.ai link. Mark pre-arrival offers and auction end times.
- More than about 10 offers: an HTML page per [report.md](../wineauction-reference/references/report.md).
- When nothing is listed, say so and give the references from `search_wines`.

## Recurring check

When the user wants a regular check and the client supports scheduled tasks, suggest a weekly one that reruns the same query. Report only offers that are new or cheaper than last time, comparing with the previous run in the conversation. Do not store the watch anywhere else.

These tools cannot buy or reserve anything; the links go to the seller's own page.
