---
name: deal-watch
description: Looks up specific wines, a producer, a region or appellation, or a style, and show their market references with the best current offers; optionally repeat the check on a schedule. Use for "any good Bienvenues-Batard-Montrachet out there", "what is white Burgundy from Roulot going for", "check Rousseau for me every week".
---

# Deal watch

The tools come from the WineAuction connector.

## Steps

1. Turn the request into wine filters:
   - names or `lwin7`
   - producer
   - region and `appellation`
   - `color`
   - vintage range

   `search_wines` filters only on the wine, never on offer fields such as price, discount or seller.
2. Call `search_wines`. Each wine in the result carries:
   - its `retail` and `auction` references
   - up to two `best_offers`

   To see every offer for one wine, call `list_offers` with that wine's `wine_id`.
3. Judge the deals yourself from each offer's `discount_vs_retail_pct` and `discount_vs_auction_pct`. Positive means the offer is cheaper than the reference. Apply the user's price band or discount threshold to these results.
4. To scan one auction, store or restaurant by price or discount instead, use the auction-deals skill (`list_offers`).

## Output

Build the page with the wine-report skill:
- one row per offer in `best_offers`, carrying the wine's references;
- `group` set to the appellation or producer.

In the chat reply, list the wines that have an offer 20% or more below either reference.

## Scheduling

When the user wants a recurring watch and the client supports scheduled tasks, suggest a weekly one that reruns the same `search_wines` query. Report only deals that are new or better than last time; compare against the previous run's results in the conversation. Do not store the user's watch list anywhere else.
