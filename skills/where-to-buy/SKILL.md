---
name: where-to-buy
description: "List where a specific wine is currently offered, across retail stores, live auctions and restaurants, with each price against the market references. Use when the user asks where a named wine or vintage is available now, who has it in stock, or for the lowest current price for it."
---

# Where to buy

## Steps

1. Identify the wine with `search_wines` ([fields](../wineauction-reference/references/tools/search_wines.md)) and take its `wine_id` (and vintage). When several wines match, ask which one or show the top few.
2. Call `list_offers` with `wine_id` and `vintage`, leaving `offer_type` out for every type or setting it to what the user wants; offers come lowest price first ([fields](../wineauction-reference/references/tools/list_offers.md)). Add the user's filters: `max_price_usd`, `bottle_size_ml`, `in_stock`, `pre_arrival`. Page with `cursor` and save each page.
3. Read prices with [prices.md](../wineauction-reference/references/prices.md). An auction lot's price is its current or opening bid, not a price you can pay.

## In chat

- The offers ordered by price per 750 ml: seller and city, type, bottles and size, price, both discounts, the seller link and the wineauction.ai link. Mark pre-arrival offers and auction end times.
- More than about 10 offers: an HTML page per [report.md](../wineauction-reference/references/report.md).
- When nothing is listed, say so and give the references from `search_wines`.

These tools cannot buy or reserve anything; the links go to the seller's own page.
