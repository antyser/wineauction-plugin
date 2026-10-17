# Reading WineAuction prices

## The two references

Every wine and offer carries two reference views, in US dollars per 750 ml:

- `retail`: the lowest current retail price (`price_usd`) and how many retail offers are on sale (`live_offer_count`).
- `auction`: the median hammer price with buyer's premium for this exact vintage (`price_usd`), with `sale_count` and `last_sale_at`.

Either view is null when there is no data. A null auction view means this vintage has no recorded sales in the data; it does not prove the wine never sold. Answer sale-history questions from closed lots (`list_offers` with `status: closed`).

The references are market prices, not offers. Never say a wine is in stock or can be had at a reference price.

## Discounts and markups

- `discount_vs_retail_pct` and `discount_vs_auction_pct` are positive when the price is below the reference.
- Always name the reference you quote: "18% below the auction median", not "18% off".
- On a restaurant list both are usually negative; the negative of `discount_vs_retail_pct` is the markup over retail.
- A live auction lot is priced at its current bid, else its opening bid, with premium. Bidding raises it, so say the discount is at the current or opening bid, not at the likely hammer price.

## Flag a reference as doubtful when

- `auction.sale_count` is 1 or 2: one or two sales are weak evidence.
- The retail and auction references are more than 3× apart.
- The retail reference is below a third of a retail list price on the same line.
- The bottle is a half bottle or a large format: references are per 750 ml and large formats usually cost more per 750 ml. Show the printed price and size, such as "Printed $99 for 375 ml".
- On a merchant's own list, the retail discount is exactly 0: the merchant's listing may be the reference itself. Rank by the auction discount instead.
- A matched row has neither reference: report "no market data", not a discount.

## Units

- `_usd` fields are per 750 ml. Auction prices include the buyer's premium.
- A case, OWC or 6-pack price covers 12 or 6 bottles. A price for several bottles is divided before comparing.

## Links

- A wine: `wineapp_wine_url` (or `wineapp_url` on a `search_wines` wine).
- An offer: its `wineapp_url` on wineauction.ai, and `url` for the seller's own page.
- Quote a specific lot or offer with both links when available.

## Access

Retail offers and stores need a signed-in WineAuction account. Restaurant offers need a plan with Restaurant access; when it is missing, the tools skip them and return a `notice`. Pass the notice on in plain words; do not fill the gap from other websites.
