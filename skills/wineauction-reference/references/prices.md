# Reading WineAuction prices

## The two references

Every wine and offer carries two reference views, in US dollars per 750 ml:

- `retail`: the lowest current retail price (`price_usd`) and how many retail offers are on sale (`live_offer_count`).
- `auction`: the median hammer price with buyer's premium (`price_usd`), with `sale_count`, `last_sale_at` and `vintage_basis`. It is the median for the exact vintage when that vintage has sales, otherwise for all vintages of the wine pooled; `vintage_basis` says which (`exact` or `any_vintage`). A wine without a vintage always gets the pooled figure.

Either view is null when there is no data. A null auction view means no vintage of the wine has recorded sales in the data; it does not prove the wine never sold. Answer sale-history questions from closed lots (`list_offers` with `status: closed`).

The references are market prices, not offers. Never say a wine is in stock or can be had at a reference price.

## Discounts and markups

- `discount_vs_retail_pct` and `discount_vs_auction_pct` are positive when the price is below the reference.
- Always name the reference you quote: "18% below the auction median", not "18% off".
- On a restaurant list both are usually negative; the negative of `discount_vs_retail_pct` is the markup over retail.
- A live auction lot is priced at its current bid, else its opening bid, with premium. Bidding raises it, so say the discount is at the current or opening bid, not at the likely hammer price.

## Flag a reference as doubtful when

- `auction.sale_count` is 1 or 2: one or two sales are weak evidence.
- `auction.vintage_basis` is `any_vintage`: the median pools every vintage of the wine, not this vintage's sales, and `discount_vs_auction_pct` is set against that pooled median. Tell the user whenever you quote it.
- `retail.live_offer_count` is 0: the retail reference is stale, not a current price.
- The retail and auction references are more than 3× apart.
- The retail reference is below a third of a retail list price on the same line.
- The bottle is a half bottle or a large format: references are per 750 ml and large formats usually cost more per 750 ml. Show the printed price and size, such as "Printed $99 for 375 ml".
- On a merchant's own list, the retail discount is exactly 0: the merchant's listing may be the reference itself. Rank by the auction discount instead.
- A matched row has neither reference: report "no market data", not a discount.

## Units and quantities

- `_usd` fields are per 750 ml. Auction prices include the buyer's premium.
- Offers are rarely a single bottle. A case, OWC or 6-pack price covers 12 or 6 bottles, an auction lot covers its `bottles` of `bottle_size_ml`, and a mixed lot covers several wines. Compare per 750 ml, but always show the quantity and the price as quoted next to it: "6 × 750 ml, $5,700 lot ($950 per bottle)".
- A mixed lot has no per-bottle price from the tools. Split it into its wines and price it with [mixed-lots.md](mixed-lots.md); never quote the first wine's reference for the whole lot.

## Links

- A wine: `wineapp_wine_url` (or `wineapp_url` on a `search_wines` wine).
- An offer: its `wineapp_url` on wineauction.ai, and `url` for the seller's own page.
- Quote a specific lot or offer with both links when available.

## Access

Retail offers and stores need a signed-in WineAuction account. Restaurant offers need a plan with Restaurant access; when it is missing, the tools skip them and return a `notice`. Pass the notice on in plain words; do not fill the gap from other websites.
