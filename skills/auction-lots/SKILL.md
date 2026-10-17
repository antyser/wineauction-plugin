---
name: auction-lots
description: "Scan wine auction lots against retail and auction reference prices, and report past auction results. Use when the user names a wine auction or auction house (Acker, Sotheby's, Christie's, Zachys, K&L and others), asks which live lots are below market or ending soon, asks what lots sold for, or wants a recurring watch on upcoming sales."
---

# Auction lots

## Steps

1. Choose the status from the request: `live` for current or upcoming sales, `closed` for ended sales and results. When the request mixes them ("closed lots ending tomorrow"), ask which one is meant before calling a tool.
2. Identify the scope.
   - A named sale: call `list_auctions` ([fields](../wineauction-reference/references/tools/list_auctions.md)) with that status and the house, and pick the sale by name; use its `auction_slug`.
   - A house only: use `house`.
   - "Ending soon": `ending_within_hours`.
3. Call `list_offers` ([fields](../wineauction-reference/references/tools/list_offers.md)) with `offer_type: auction`, the status, the scope, and the user's filters (`region`, `color`, `appellation`, `min_price_usd` / `max_price_usd` per 750 ml). Use `mixed_lot: exclude` unless the user wants mixed lots.
   - Below market: `sort: discount_vs_retail` or `discount_vs_auction` with the user's `min_discount_pct`; when they gave no threshold, 20 is a reasonable default and say you used it.
   - Ending soon: `sort: end_time`.
   - Results: `status: closed`, `sort: recent`, optional `sold_after` / `sold_before`. Only `auction_status: sold` rows are sales; never count unsold lots.
   - Page with `cursor` and save each page. Keep a price range exactly as given; if it is inverted, say so instead of swapping it.
4. Read prices with [prices.md](../wineauction-reference/references/prices.md): live discounts are at the current or opening bid.
5. Present with [report.md](../wineauction-reference/references/report.md). Label results from different sales or houses separately and link each lot.

## Recurring watch

When the user wants a regular check and the client supports scheduled tasks, suggest one that reruns the same `list_offers` query before each sale's end. Report only lots that are new or further below a reference than last time, comparing with the previous run in the conversation. Do not store the watch anywhere else.

These tools cannot place bids. When asked to bid, say so and offer to research the lot instead.
