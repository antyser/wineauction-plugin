---
name: price-check
description: Judges wine prices someone already has against WineAuction retail and auction references. Use for a merchant newsletter or email offer, a pasted price list, a restaurant wine list (text or photo), or "is this a good price" for one or more named wines.
---

# Price check

The user brings wines with prices: a merchant email or newsletter, a price list, or a restaurant wine list. Find which are good deals and which are overpriced.

The tools come from the WineAuction connector.

## Steps

1. Extract one row per wine and price from the source. Keep what the source states, and do not guess missing facts:
   - `raw_wine_name`: producer, wine and vintage as written.
   - `vintage`: the year, if the source gives it.
   - `price`, `currency`, `quantity`: the bottles the price covers. A case or 6-pack price covers 6 or 12, and a by-the-glass price is not a bottle price, so skip it.
   - `format_ml`: 375, 750, 1500 and so on, when stated.
   - `offer_type`: `retail` for a shop, newsletter or price list; `restaurant` for a wine list.
2. Put where the rows came from in `source`: merchant, document title and date.
3. Call `evaluate_offers` with up to 100 rows per call. Each row costs one Wine Price Query. If the batch is larger than the user's remaining allowance, the call is rejected and nothing is charged; say so and offer a smaller batch.
4. Read each result:
   - `outcome: unmatched`: list it under "not found" with the hint. Do not invent a price.
   - `retail`: the retail reference.
   - `auction`: the exact-vintage auction reference, which is null when that vintage has no sales. Quote `sale_count` with it.
   - `discount_vs_retail_pct` and `discount_vs_auction_pct`: a positive value means cheaper than the reference.
5. Sort by the larger of the two discounts, best first. For a restaurant list, the delta against retail is the markup: lowest markup first.

## Output

Build the page with the wine-report skill, one row per priced wine:
- `group`: the list section for a restaurant list, else the region.
- `price_usd`: the evaluate result's `unit_price.amount`.
- `seller`: the merchant or restaurant.
- `ref`: the line or SKU when the source has one.
- `flags`: anything you doubted, for example "price looks like a case price".

In the chat reply, give three short lists:
- the five best deals;
- anything clearly overpriced;
- wines that were not found, with the hint for each.

Never claim a wine is in stock or can be bought at the reference price. The references are market prices, not offers.

