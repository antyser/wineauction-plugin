---
name: wine-info
description: "Look up one wine or many at once: their retail and auction reference prices, past auction sales, vintage-by-vintage prices, available critic reviews, and where it is currently offered, such as \"what does 2019 Roulot Meursault Perrières go for, what did critics say, and who has it?\" Use when the user asks in ordinary words what a named wine, producer, vintage, region or appellation costs, sells for or is worth, with or without a vintage, in any language: \"how much is Sassicaia 2016\", \"price of Krug 2008\", \"what's DRC La Tâche worth\", \"Opus One 2018 多少钱\", \"2015 Lafite 现在什么价\", \"Petrus 2010 贵不贵\", \"which Meursault vintage is the best value\", or asks how vintages compare, what it fetched at auction, its reviews or where it is available now. Read it before calling the WineAuction tools for such a question. The user brings no price they were quoted, no bottles they own and no list of their own."
---

# Wine info

The user may ask about one wine or a list of many (a watch list, several vintages, a whole producer). Answer what they asked for every wine; fetch only the parts the question needs.

## Steps

1. Turn the request into wine filters: names or `lwin7`, `producer`, `region`, `appellation`, `color`, vintage or vintage range. Up to 10 named wines go in one `wines` list; send a longer list in batches of 10, one call after another. `search_wines` filters only on wine attributes, never on price or seller ([fields](../wineauction-reference/references/tools/search_wines.md)).
2. Call `search_wines`. Each wine carries both references, `reviews[]` when available, and a two-offer sample. Page with `cursor` when more wines are wanted. Check `resolved_wines` and say which names were not found.
3. Where it is offered: call `list_offers` ([fields](../wineauction-reference/references/tools/list_offers.md)) with the wine's `wine_id` and `vintage`, or, for a producer, region or colour request ("white Burgundy under $200"), with those attributes as filters. Leave `offer_type` out for every type or set it to what the user wants, and add their filters: `max_price_usd`, `bottle_size_ml`, `in_stock`, `pre_arrival`. For a value or deal question, add `min_discount_pct` and sort by `discount_vs_retail` or `discount_vs_auction` with `offer_type` set; with no threshold given, 20 is a reasonable default and say you used it.
4. Past sales: call `list_offers` with the wine's `wine_id`, `offer_type: auction`, `status: closed`, `sort: recent`, and `vintage` when asked. Only `auction_status: sold` rows are sales. Give the date, house, `price_per_bottle_usd` (per 750 ml, premium included; `price` is the lot's hammer without premium) and the lot link.
5. Page with `cursor` and save each page to disk. Read prices with [prices.md](../wineauction-reference/references/prices.md).

## In chat

- Per wine and vintage: the retail reference with its offer count, the auction median with its sale count and last sale date, and the wine's wineauction.ai link.
- Reviews: author, the returned text (it often starts with the score) and the link. Say when none are available; never supply a score from elsewhere.
- Offers, ordered by price per 750 ml (or by discount for a value question): seller and city, type, bottles and size, price, both discounts, the seller link and the wineauction.ai link. Mark pre-arrival offers and auction end times; an auction lot's price is its current or opening bid. When nothing is listed, say so.
- Vintage comparisons as a short table. More than about 10 wines or offers: an HTML page per [report.md](../wineauction-reference/references/report.md).

## Recurring check

When the user wants a regular check and the client supports scheduled tasks, suggest a weekly one that reruns the same query. Report only offers that are new or cheaper than last time, comparing with the previous run in the conversation. Do not store the watch anywhere else.

These tools cannot buy or reserve anything; links go to the seller's own page.
