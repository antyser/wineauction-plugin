---
name: merchant-offer-check
description: "Judge prices a merchant has quoted against retail and auction market prices. Use when the user shares a merchant email, newsletter, promotion, futures or en primeur offer, price list or offer sheet, names a wine shop and asks about its prices, or asks whether a quoted price for a wine is good."
---

# Merchant offer check

The question is whether each quoted price is below, at or above the market for that exact wine and vintage.

## Steps

1. Get the rows.
   - A single quote ("$950 a bottle for Lafite 2010", "$5,700 for six"): one row with `offer_type: retail`, `quantity` and `format_ml`. Pass `include_vintages: true` when the user might consider another vintage.
   - An email, list or offer sheet: parse it with [parse-list.md](../wineauction-reference/references/parse-list.md), `offer_type: retail`.
   - Evaluate the rows with [evaluate.md](../wineauction-reference/references/evaluate.md).
   - A named store: find its `id` with `list_retail_stores` ([fields](../wineauction-reference/references/tools/list_retail_stores.md)), then call `list_offers` with `offer_type: retail`, `merchant_id`, the user's filters and `sort: discount_vs_auction` (the store's own listing is often the retail reference). Page with `cursor` and save each page.
2. Read prices with [prices.md](../wineauction-reference/references/prices.md). Show the per-bottle price per 750 ml next to the printed price.
3. Present with [report.md](../wineauction-reference/references/report.md).

## In chat

- For one quote: the per-bottle price, both references, both discounts, and a plain verdict naming the reference it rests on.
- For a list: the five rows furthest below a reference, leaving out flagged rows; anything clearly above both references; pre-arrival and futures rows marked as such.
