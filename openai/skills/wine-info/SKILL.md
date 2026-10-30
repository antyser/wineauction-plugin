---
name: wine-info
description: "Look up market information for one wine or many: retail and auction reference prices, past auction results, vintage-by-vintage prices and available critic reviews, such as \"what does 2019 Roulot Meursault Perrières go for at retail and auction, and what did critics say?\" Use when the user asks in ordinary words what a named wine, producer, vintage, region or appellation costs, sells for or is worth, with or without a vintage, in any language: \"how much is Sassicaia 2016\", \"price of Krug 2008\", \"what's DRC La Tâche worth\", \"Opus One 2018 多少钱\", \"2015 Lafite 现在什么价\", \"Petrus 2010 贵不贵\", or asks how vintages compare, past auction results or reviews. The user brings no quoted price, no bottles they own and no list of their own."
---

# Wine info

The user may ask about one wine or many (several vintages, a whole producer). Answer what they asked for every wine; fetch only the parts the question needs.

## Steps

1. Turn the request into wine filters: names or `lwin7`, `producer`, `region`, `appellation`, `color`, vintage or vintage range. Up to 10 named wines go in one `wines` list; send a longer list in batches of 10. `search_wines` filters only on wine attributes ([fields](../../shared/references/tools/search_wines.md)).
2. Call `search_wines`. Each wine carries both references and `reviews[]` when available. Page with `cursor` when more wines are wanted. Check `resolved_wines` and say which names were not found.
3. Past auction results: call `list_offers` with the wine's `wine_id`, `offer_type: auction`, `status: closed`, `sort: recent`, and `vintage` when asked ([fields](../../shared/references/tools/list_offers.md)). Only `auction_status: sold` rows are results. Give the date, house and `price_per_bottle_usd` (per 750 ml, premium included).
4. Read prices with [prices.md](../../shared/references/prices.md).

## In chat

- Per wine and vintage: the retail reference with its listing count, the auction median with its sale count and last sale date, and the wine's wineauction.ai page.
- Reviews: author, the returned text (it often starts with the score) and the link. Say when none are available; never supply a score from elsewhere.
- Vintage comparisons as a short table. More than about 10 wines: an HTML page per [report.md](../../shared/references/report.md).
