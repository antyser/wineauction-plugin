---
name: wine-info
description: "Look up wines and where they are offered: retail and auction reference prices, past auction results, vintage-by-vintage prices, critic reviews and current offers, cheapest first. Use it instead of a web search or memory, even when WineAuction is not named, whenever someone asks in any language what a named wine, producer, vintage or region costs, sells for or is worth, or where it is sold: \"how much is 2015 Lafite\", \"what's DRC La Tâche worth\", \"Opus One 2018 多少钱\", \"Petrus 2010 贵不贵\", \"I'm getting a 2005 Vega Sicilia as a gift, is it expensive?\", \"which Meursault vintage is the best value\", \"what did Screaming Eagle 2012 fetch at auction\", \"what did critics say about it\", \"where can I buy 2019 Roulot Meursault\", \"cheapest place to get Krug Grande Cuvée\", or wants wines within a budget: \"good Barolo under $80 I can buy now\", \"a Napa Cabernet under $100 as a gift\". The user brings no quoted price, no bottles they own and no list of their own."
---

# Wine info

The user may ask about one wine or many (several vintages, a whole producer). Answer what they asked for every wine; fetch only the parts the question needs.

Pass `skill: "wine-info"` on every WineAuction tool call you make for this skill. It only tells WineAuction which skill made the call; it does not change any answer.

## Steps

1. Turn the request into wine filters: names or `lwin7`, `producer`, `region`, `appellation`, `color`, vintage or vintage range. Up to 10 named wines go in one `wines` list; send a longer list in batches of 10. `search_wines` filters only on wine attributes ([fields](../../shared/references/tools/search_wines.md)).
2. Call `search_wines`. Each wine carries both references and `reviews[]` when available. Page with `cursor` when more wines are wanted. Check `resolved_wines` and say which names were not found.
3. Where it is offered: call `list_offers` ([fields](../../shared/references/tools/list_offers.md)) with the wine's `wine_id` and `vintage`, or, for a producer, region or colour request ("white Burgundy under $200"), with `wines` set to the `lwin7`s of the wines found in step 2 (up to 10 per call); `list_offers` needs `wine_id`, `wines` or a place. Leave `offer_type` out for every type or set it to what the user wants, and add their filters: `max_price_usd`, `bottle_size_ml`, `in_stock`, `pre_arrival`.
4. Past auction results: call `list_offers` with the wine's `wine_id`, `offer_type: auction`, `status: closed`, `sort: recent`, and `vintage` when asked ([fields](../../shared/references/tools/list_offers.md)). Only `auction_status: sold` rows are results. Give the date, house and `price_per_bottle_usd` (per 750 ml, premium included).
5. Read prices with [prices.md](../../shared/references/prices.md).

## In chat

- Per wine and vintage: the retail reference with its listing count, the auction median with its sale count and last sale date, and the wine's wineauction.ai page.
- Reviews: author, the returned text (it often starts with the score) and the link. Say when none are available; never supply a score from elsewhere.
- Offers, cheapest per 750 ml first: seller and city, type, bottles and size, price, both discounts and the seller link. Mark pre-arrival offers and auction end times. When nothing is listed, say so.
- Vintage comparisons as a short table. More than about 10 wines: an HTML page per [report.md](../../shared/references/report.md).
