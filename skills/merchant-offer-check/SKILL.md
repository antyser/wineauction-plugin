---
name: merchant-offer-check
description: "Judge the prices a merchant has quoted, for one wine or a whole list, per bottle or per 6-pack or case, against retail and auction market prices. Use when the user shares a merchant email, newsletter, promotion, futures or en primeur offer, price list or offer sheet, wants a named wine shop's whole listing checked against the market, or gives a single price for a named wine and asks whether it is expensive, fair, a good deal or worth paying, at a shop, from a seller or online: \"is $300 for Pingus 2019 expensive?\", \"should I buy Harlan 2019 at $1,100?\", \"店里卖 $200，划算吗\". A price on a restaurant list belongs to restaurant-wine-list; a price at auction belongs to auction-lots; bottles the user already owns belong to cellar-valuation."
---

# Merchant offer check

The question is whether each quoted price is below, at or above the market for that exact wine and vintage. The input may be one wine or a long list, and a price may cover one bottle, a 6-pack, a case or a mixed case; always work from the bottles and size the price covers.

## Steps

1. Get the rows.
   - One or a few quotes ("$950 a bottle for Lafite 2010", "$5,700 for six"): one row per quote with `offer_type: retail`, `quantity` and `format_ml`. Pass `include_vintages: true` when the user might consider another vintage.
   - An email, list or offer sheet: parse it with [parse-list.md](../wineauction-reference/references/parse-list.md), `offer_type: retail`.
   - Evaluate the rows with [evaluate.md](../wineauction-reference/references/evaluate.md).
   - A store named without a list: find its `id` with `list_retail_stores` ([fields](../wineauction-reference/references/tools/list_retail_stores.md)), then call `list_offers` with `offer_type: retail`, `merchant_id`, the user's filters and `sort: discount_vs_auction` (the store's own listing is often the retail reference). Page with `cursor` and save each page.
2. Read prices with [prices.md](../wineauction-reference/references/prices.md). Show the per-bottle price per 750 ml next to the printed price.
3. Present with [report.md](../wineauction-reference/references/report.md).

## In chat

- For one quote: the per-bottle price, both references, both discounts, and a plain verdict naming the reference it rests on.
- For a list: the five rows furthest below a reference, leaving out flagged rows; anything clearly above both references; pre-arrival and futures rows marked as such.
- When the user also asks about reviews, call `search_wines` with the matched `lwin7` and `vintage` and quote `reviews[]` as the wine-info skill does.
