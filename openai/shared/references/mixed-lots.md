# Pricing a mixed lot

A mixed lot (or mixed case) is one price for several different wines. The tools give it no per-bottle price and no references, so work it out yourself from its parts.

## 1. List every wine in it

- From `list_offers`: `auction_lot_items[]` gives `{name, vintage, bottles, bottle_size_ml}` per wine.
- When `auction_lot_items` is null, only the first wine is named: the listing name and `bottles` describe the lot, not that wine, and `bottle_size_ml` may be null. Read the full contents from the user's sheet, the seller's lot page (`url`) or the lot page on wineauction.ai (`wineapp_url`).
- Keep the counts exactly as stated. If the contents still cannot be read in full, say which part is unknown and do not price the lot.

## 2. Price each wine

Call `search_wines` with a `wines` list of up to 10 `{query, vintage}` (or `lwin7`) per call and take each wine's `retail` and `auction` views. Apply [prices.md](prices.md) to each part: a part with 1–2 sales, a stale retail reference (`live_offer_count` 0) or references more than 3× apart is weak. List any part that was not found.

## 3. Add up the lot

- Bottle-equivalents per part: `bottles × bottle_size_ml / 750`.
- Lot retail value: Σ part retail per 750 ml × its bottle-equivalents. Lot auction value: the same with the auction view. Compute each only when every part has that reference; otherwise give the covered share ("auction value covers 9 of 12 bottles").
- Lot price: the price with buyer's premium (listed price, final price or estimate, saying which).
- Lot discount vs retail = 1 − lot price ÷ lot retail value; the same for auction.
- For the report: `price_usd` = lot price ÷ total bottle-equivalents, `retail_usd` and `auction_usd` = lot value ÷ total bottle-equivalents, the two discounts as computed, `mixed_items` with every part, and a flag for any weak or missing part.

Show the breakdown in chat for the lots you highlight: each part with bottles, size and reference, then the totals.
