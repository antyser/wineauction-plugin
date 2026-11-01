# Reading WineAuction prices

## The two references

Every wine and offer carries two reference views, in US dollars per 750 ml:

- `retail`: the lowest retail price (`price_usd`) among `offer_count` offers, and how many retail offers are on sale now (`live_offer_count`).
- `auction`: the median hammer price with buyer's premium (`price_usd`), with `sale_count`, `last_sale_at` and `vintage_basis`. It is the median for the exact vintage when that vintage has sales, otherwise for all vintages of the wine pooled; `vintage_basis` says which (`exact` or `any_vintage`). A wine without a vintage always gets the pooled figure.

## What a reference rests on

The server picks each reference by a fixed order and returns one figure; it does not cross-check it. Read these fields before you lean on a number:

| Field | Values | What it means |
| --- | --- | --- |
| `retail.window` | `live30d` | This vintage, at least 2 offers on sale in the last 30 days. The strongest retail reference. |
| | `1y` | This vintage, offers seen in the past year, sold out ones included. It can rest on a single offer. |
| | null | A Wine-Searcher figure (`source: wine_searcher`) or the latest vintages (below). |
| `retail.vintage_basis` | `exact` | This vintage. |
| | `latest_vintages` | No price for this vintage: the lowest offer across the wine's 10 latest vintages. Not this vintage's price. |
| | `any_vintage` | A wine without a vintage: every vintage pooled. |
| `retail.offer_count` | number | How many offers the price is the lowest of. Null for a Wine-Searcher figure. |
| `retail.market` | `GLOBAL`, or a market such as `US` | Where those offers are. |
| `retail.live_offer_count` | number | Offers on sale now. 0 means the price is not a current one. |
| `auction.vintage_basis` | `exact` / `any_vintage` | This vintage's sales, or every vintage of the wine pooled. |
| `auction.sale_count`, `last_sale_at` | number, date | How many sales over the past 5 years, and the latest. |

The order for retail is: live30d, then 1y, then Wine-Searcher, then the latest vintages. A 1y price from one offer therefore wins over a latest-vintages price from fifty.

## When a reference is thin, check it

A reference is thin when any of these hold:

- `retail.offer_count` or `auction.sale_count` is 1 or 2.
- `vintage_basis` is not `exact`, or `retail.source` is `wine_searcher`.
- `auction.last_sale_at` is more than 2 years old.
- The retail and auction references are more than 3× apart.

Before you call a price a deal or a rip-off on a thin reference, look around it:

1. Neighbouring vintages: `search_wines` with the wine's name as `query` (no year in it) and `vintage_min`/`vintage_max` covering about 10 vintages around it (or the latest 10), or `evaluate_offers` with `include_vintages: true`. Each vintage comes with its own views and counts. If most vintages sit in one band and this one is far off, the single point is suspect.
2. Recent sales: `list_offers` with `wine_id`, `offer_type: auction`, `status: closed`, `sort: recent`. Read the individual hammer prices, not just the median.
3. Current offers: `list_offers` with `wine_id` and `offer_type: retail` shows the offers behind a retail figure.

Then say which evidence you used, for example: "The retail reference is one offer from last year; across the 2010–2019 vintages retail runs $180–$240, so $210 is about market." When the checks still leave little evidence, say the call is uncertain instead of quoting a precise discount. For long lists, check only the rows you will highlight or that the user asks about; the rest keep their flag.

Either view is null when there is no data. A null auction view means no vintage of the wine has recorded sales in the data; it does not prove the wine never sold. Answer sale-history questions from closed lots (`list_offers` with `status: closed`).

The references are market prices, not listings.

## Discounts and markups

- `discount_vs_retail_pct` and `discount_vs_auction_pct` are positive when the price is below the reference.
- Always name the reference you quote: "18% below the auction median", not "18% off".
- On a restaurant list both are usually negative; the negative of `discount_vs_retail_pct` is the markup over retail.
- A current auction lot's listed price is provisional until the sale closes; say so when comparing it.

## Flag a reference as doubtful when

- The reference is thin (above) and you did not check it.
- `auction.sale_count` is 1 or 2: one or two sales are weak evidence.
- `vintage_basis` is not `exact`: on auction the median pools every vintage of the wine, not this vintage's sales, and `discount_vs_auction_pct` is set against that pooled median; on retail `latest_vintages` is another vintage's price. Tell the user whenever you quote it.
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

## Access

Retail offers and stores need a signed-in WineAuction account. Restaurant offers need a plan with Restaurant access; when it is missing, the tools skip them and return a `notice`. Pass the notice on in plain words; do not fill the gap from other websites.
