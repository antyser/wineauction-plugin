# list_offers

List offers: every offer for one wine (pass `wine_id`) or for a few named wines (pass `wines`), or the offers in one place: an auction, an auction house, a retail store or a restaurant. Also use it for closed auction results. The two scopes combine, e.g. one wine's lots in one auction.

| Input | Type / values | Meaning |
|---|---|---|
| `offer_type` | auction / retail / restaurant | Which offers. Required when listing a place alone; with `wine_id` or `wines`, omit it for all types. |
| `wine_id`, `vintage` | UUID, year | Every offer for one wine, from `search_wines`, optionally one vintage. No place needed; sorted by price per bottle, lowest first. |
| `auction_slug` | text | One auction, from `list_auctions`. |
| `house` | sothebys / christies / klwines / acker / heritage / spectrum / unicorn / zachys / hdh / brentwood | Every auction of one house. |
| `merchant_id` | UUID | One store or restaurant, from `list_retail_stores` or `list_restaurants`. |
| `status` | live (default) / closed / all | Auctions: open, ended or both. |
| `ending_within_hours` | positive number | Auctions ending within this many hours. |
| `sold_after`, `sold_before` | ISO 8601 UTC ending in `Z` | End-time window for closed auctions. |
| `wines` | list of ≤10 `{query` or `lwin7, vintage}` | Only these wines. |
| `region`, `appellation`, `classification`, `color` | as in `search_wines` | Wine attributes. |
| `min_discount_pct` | 0–100 | At least this much below the retail or the auction reference (either one). |
| `min_price_usd`, `max_price_usd` | number | Price range per 750 ml. |
| `mixed_lot` | include (default) / exclude / only | Auctions: lots of different wines. |
| `bottle_size_ml` | integer, e.g. 375 / 750 / 1500 | Only this bottle size. |
| `in_stock` | boolean, default true | Retail: true keeps in-stock offers only; false also includes out-of-stock ones. |
| `pre_arrival` | include (default) / only / exclude | Retail: pre-arrival offers. |
| `serving` | bottle / glass | Restaurant: by the bottle or by the glass. |
| `sort` | end_time / price_asc / price_desc / recent / discount_vs_retail / discount_vs_auction | end_time and recent are meant for auctions (recent puts the latest sales first); on other offers they order by listing expiry. Default: end_time for an auction place, otherwise price_asc. |
| `limit`, `cursor` | 1–100, default 25 | Paging. |

| Output | Meaning |
|---|---|
| `offers[]` | Offer rows with wine fields and both views; see below. |
| `resolved_wines[]` | Only with `wines`, as in `search_wines`. |
| `notice` | Present when there is something the caller should know. |
| `has_more`, `next_cursor`, `as_of` | Paging and data time. |

## Offer row

The rows in `list_offers.offers[]` and in `search_wines` `best_offers[]`. Inside `best_offers[]` the wine fields and views are left out because the wine already carries them.

| Field | Meaning |
|---|---|
| `offer_type`, `offer_id` | auction / retail / restaurant; `offer_id` for de-duplication. |
| `wine_id`, `wine_name`, `producer`, `vintage`, `region`, `appellation`, `color`, `lwin7` | The identified wine; all but `wine_name` are null when unidentified. |
| `wineapp_wine_url` | The wine's page on wineauction.ai for this vintage. |
| `retail`, `auction` | The two reference views; null for a mixed lot. |
| `listing_name` | The seller's own name for it. |
| `bottles`, `bottle_size_ml` | Bottle count and size in ml. |
| `price`, `currency` | The seller's price and currency. For an auction it covers the whole lot: current bid, else opening bid, else the hammer price once closed; premium excluded. |
| `price_per_bottle_usd` | Per 750 ml in USD, premium included; null for a mixed lot. |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | Discount of the per-bottle price against each view. |
| `seller_name`, `seller_country`, `seller_city` | Auction house, merchant or restaurant. |
| `url` | The page on the seller's site. |
| `wineapp_url` | This offer on wineauction.ai: lot, store or restaurant page. |
| `auction_name`, `auction_lot_number` | Auction and lot number (auction only). |
| `auction_status` | live / sold / unsold. |
| `auction_end_time` | When the auction ends. |
| `auction_estimate_low`, `auction_estimate_high` | House estimate for the whole lot, in `currency`. |
| `auction_buyers_premium_pct` | Premium in percent, e.g. 25. |
| `auction_lot_items[]` | Mixed lots only: `{name, vintage, bottles, bottle_size_ml}` per wine. |
| `retail_in_stock`, `retail_pre_arrival`, `retail_last_seen_at` | Retail: in stock, pre-arrival, last time seen on sale. |
| `restaurant_serving`, `restaurant_section` | Restaurant: bottle / glass, section of the list. |
