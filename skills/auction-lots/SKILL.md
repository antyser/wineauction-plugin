---
name: auction-lots
description: "Check wine auction lots, one or hundreds, each of one or many bottles, against retail and auction reference prices. Use when the user shares an auction sheet, catalog, lot list or a hammer price (PDF, photo, link or pasted text) and asks whether the estimates or prices are good, names a wine auction or auction house (Acker, Sotheby's, Christie's, Zachys, K&L and others) and asks which lots are below market, ending soon or what a sale's lots sold for, or wants a recurring watch on upcoming sales. Past sales of one named wine belong to wine-info."
---

# Auction lots

A lot often holds several bottles (6, 12, a mixed case) and a sheet can hold hundreds of lots. The user's own input comes first. When they bring a sheet or lots, evaluate exactly those; look a sale up in WineAuction only when they name one without bringing it.

## A sheet or lots the user brings

1. Parse with [parse-list.md](../wineauction-reference/references/parse-list.md), `offer_type: other`, one row per lot and wine. Use the price the user gives; when the sheet has only estimates, evaluate the low and high estimate as two prices and say they are estimates. Pass `buyers_premium` (from the sheet, else ask or state the assumption) when the price is a hammer price.
2. Evaluate with [evaluate.md](../wineauction-reference/references/evaluate.md). Mixed lots get no per-bottle price; list them in the reply.
3. Present with [report.md](../wineauction-reference/references/report.md), keeping the lot numbers as `ref`.

## A sale or house the user names

1. Choose the status: `live` for current or upcoming sales, `closed` for ended sales and results. When the request mixes them ("closed lots ending tomorrow"), ask which one is meant before calling a tool.
2. Scope: for a named sale, call `list_auctions` ([fields](../wineauction-reference/references/tools/list_auctions.md)) with the status and house and use the sale's `auction_slug`; for a house only, use `house`; for "ending soon", `ending_within_hours`.
3. Call `list_offers` ([fields](../wineauction-reference/references/tools/list_offers.md)) with `offer_type: auction`, the status, the scope, and the user's filters (`region`, `color`, `appellation`, `min_price_usd` / `max_price_usd` per 750 ml). Use `mixed_lot: exclude` unless the user wants mixed lots.
   - Below market: `sort: discount_vs_retail` or `discount_vs_auction` with the user's `min_discount_pct`; with no threshold given, 20 is a reasonable default and say you used it.
   - Ending soon: `sort: end_time`.
   - Results: `status: closed`, `sort: recent`, optional `sold_after` / `sold_before`. Only `auction_status: sold` rows are sales; never count unsold lots.
   - Page with `cursor` and save each page. Keep a price range exactly as given; if it is inverted, say so instead of swapping it.
4. Present with [report.md](../wineauction-reference/references/report.md). Label results from different sales or houses separately and link each lot.

Read prices with [prices.md](../wineauction-reference/references/prices.md): a live discount is at the current or opening bid, not the likely hammer price.

## Recurring watch

When the user wants a regular check and the client supports scheduled tasks, suggest one that reruns the same `list_offers` query before each sale's end. Report only lots that are new or further below a reference than last time, comparing with the previous run in the conversation. Do not store the watch anywhere else.

These tools cannot place bids. When asked to bid, say so and offer to research the lot instead.
