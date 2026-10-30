---
name: merchant-offer-check
description: "Compare a merchant's printed prices, for one wine or a whole price list, per bottle or per 6-pack or case, with retail and auction market reference prices, per 750 ml. Use when the user shares a merchant email, newsletter, futures or en primeur offer, price list or offer sheet, or gives a single price for a named wine and asks whether it is high, fair or low against the market: \"is $300 for Pingus 2019 expensive?\", \"店里卖 $200，划算吗\". A price on a restaurant list belongs to restaurant-wine-list; bottles the user already owns belong to cellar-valuation."
---

# Merchant price comparison

For each printed price, report how it compares with the retail and auction references for that exact wine and vintage. The input may be one wine or a long list, and a price may cover one bottle, a 6-pack, a case or a mixed case; always work from the bottles and size the price covers.

## Steps

1. Get the rows.
   - One or a few prices ("$950 a bottle for Lafite 2010", "$5,700 for six"): one row per price with `offer_type: retail`, `quantity` and `format_ml`. Pass `include_vintages: true` to compare vintages.
   - An email, list or offer sheet: parse it with [parse-list.md](../../shared/references/parse-list.md), `offer_type: retail`.
   - Evaluate the rows with [evaluate.md](../../shared/references/evaluate.md).
2. Read prices with [prices.md](../../shared/references/prices.md). Show the price per 750 ml next to the printed price.
3. Present with [report.md](../../shared/references/report.md).

## In chat

- For one price: the price per 750 ml, both references, how far it sits from each, and which reference the comparison rests on.
- For a list: the rows furthest below and furthest above a reference, leaving out flagged rows, and futures rows marked as such.
- When the user also asks about reviews, call `search_wines` with the matched `lwin7` and `vintage` and quote `reviews[]` as the wine-info skill does.
