---
name: auction-deals
description: Finds the best-value lots in one wine auction or auction house, optionally narrowed to a style or region such as white Burgundy, Champagne or a single appellation. Use for "what are the deals in the Acker sale", "anything good in Zachys this week", "white Burgundy lots under $300".
---

# Auction deals

The tools come from the WineAuction connector.

## Steps

1. Identify the auction.
   - If the user names a sale, call `list_auctions` (status `live`) and pick it by house and name. Use its slug as `auction_slug` in the next step.
   - If the user names only a house, use `house`.
2. Call `list_offers` with:
   - `offer_type: auction`;
   - `status: live` unless the user asks about past sales;
   - the user's preferences as filters:
     - `region`, for example Burgundy or Champagne;
     - `color`: red, white, rose, sparkling, dessert or fortified;
     - `appellation`, for example Meursault or Bienvenues-Batard-Montrachet;
     - `min_price_usd` / `max_price_usd`, per 750ml;
     - `mixed_lot: exclude` unless the user wants mixed lots;
   - `sort: discount_vs_retail` or `discount_vs_auction`, with `min_discount_pct` (20 is a sensible default);
   - `limit` 25, then page with `cursor` (the previous `next_cursor`) while the results stay interesting.
3. For each lot:
   - `price_per_bottle_usd` includes the buyer's premium. It uses the current bid if there is one, otherwise the starting bid.
   - Compare it with `retail.price_usd` and `auction.price_usd`.
   - Treat the auction reference as weak when `auction.sale_count` is 1–2. Treat either reference as doubtful when the two differ by more than 3×.

## Output

Build the page with the wine-report skill, one row per lot:
- `group`: region, or colour when the user asked for one region.
- `ref`: "Lot <number>".
- `seller`: house and sale name.
- `ends_at`: `auction_end_time`.

Leave mixed lots out of the rows, and mention any good ones in the reply.

In the chat reply, give:
- up to five top picks, each with lot number, price per bottle, both references and the closing time;
- the lots that look cheap only because a reference is suspect.

Prices rise as bidding goes on. Say that the discount is at the current or starting bid, not at the likely hammer price.

