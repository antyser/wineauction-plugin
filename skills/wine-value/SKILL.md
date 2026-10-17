---
name: wine-value
description: "Price and critic research for a named wine: its retail and auction reference prices, past auction sales, vintage-by-vintage prices and available critic reviews, such as \"what does 2019 Roulot Meursault Perrières go for, and what did critics say?\" Use when the user asks what a wine, producer, vintage, region or appellation costs or sells for, how vintages compare on price, what a named wine fetched at auction, or what critics said about it, without bringing a price of their own."
---

# Wine value

## Steps

1. Turn the request into wine filters: names or `lwin7`, `producer`, `region`, `appellation`, `color`, vintage or vintage range. Up to 10 named wines go in one `wines` list. `search_wines` filters only on wine attributes, never on price or seller ([fields](../wineauction-reference/references/tools/search_wines.md)).
2. Call `search_wines`. Each wine carries both references, `reviews[]` when available, and a two-offer sample. Page with `cursor` when more wines are wanted. Check `resolved_wines` and say which names were not found.
3. Past sales: call `list_offers` with the wine's `wine_id`, `offer_type: auction`, `status: closed`, `sort: recent`, and `vintage` when asked ([fields](../wineauction-reference/references/tools/list_offers.md)). Only `auction_status: sold` rows are sales. Give the date, house, `price_per_bottle_usd` (per 750 ml, premium included; `price` is the lot's hammer without premium) and the lot link. Save each page to disk.
4. Read prices with [prices.md](../wineauction-reference/references/prices.md).

## In chat

- Per wine and vintage: the retail reference with its offer count, the auction median with its sale count and last sale date, and the wine's wineauction.ai link.
- Reviews: author, the returned text (it often starts with the score) and the link. Say when none are available; never supply a score from elsewhere.
- Vintage comparisons as a short table. More than about 10 wines: an HTML page per [report.md](../wineauction-reference/references/report.md).

When the user then wants to know where it is on sale now, the where-to-buy skill covers it.
