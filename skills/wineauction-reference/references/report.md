# Presenting results

**Up to about 10 rows**: answer in chat. **More**: render one self-contained HTML page and give the user the file; show it as an HTML artifact when the client can.

## Rows from list_offers or search_wines

Build `rows.json` with one row per offer (rows from `evaluate_offers` are described in [evaluate.md](evaluate.md)). Multi-bottle lots, cases and mixed lots are rows like any other; their per-750 price is shown beside the quoted lot total. A mixed lot's prices and discounts come from [mixed-lots.md](mixed-lots.md).

| key | from |
| --- | --- |
| `name`, `vintage` | `wine_name` (or `listing_name`), `vintage` |
| `group` | `appellation` or `region`; colour when the request covers one region |
| `ref` | "Lot <`auction_lot_number`>" for auctions, else a SKU or list section |
| `seller` | `seller_name`, plus `auction_name` for a sale |
| `bottles`, `size_ml` | `bottles`, `bottle_size_ml` |
| `price_usd` | `price_per_bottle_usd` |
| `retail_usd`, `retail_live`, `auction_usd`, `auction_sales` | the `retail` and `auction` views |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | as returned |
| `url` | the seller's page for the offer |
| `wineapp_url` | the offer's `wineapp_url`, else the wine's |
| `ends_at` | `auction_end_time` |
| `flags` | doubts, such as "Retail from 2008 vintage" |
| `price_label` | text above the price: "Current or opening bid", "Hammer incl. premium", "Low estimate incl. premium", "List price", "Quoted price", "Price" |
| `quoted_price`, `quoted_currency` | the price as quoted for the whole row (lot, case or bottle); shown when `bottles` > 1, `size_ml` is not 750 or the currency is not USD |
| `premium_pct` | buyer's premium, shown "+25% premium" |
| `estimate_low`, `estimate_high` | house estimate in `quoted_currency` |
| `status` | live / sold / unsold / withdrawn; badge for the last three |
| `sold_at` | ISO date of a closed lot, shown "sold Oct 3" |
| `serving` | glass / half / magnum; badge unless bottle |
| `pre_arrival`, `in_stock` | booleans; "Out of stock" shows only when `in_stock` is false |
| `mixed_items` | list of `{name, vintage, bottles, bottle_size_ml}`; "Mixed lot" badge and the items under the title |

All the keys from `price_label` on are optional; an absent key renders as nothing. The renderer fills them from raw `list_offers` fields (`price`, `currency`, `auction_buyers_premium_pct`, `auction_estimate_*`, `auction_status`, `restaurant_serving`, `retail_pre_arrival`, `retail_in_stock`, `auction_lot_items`).

The renderer also accepts raw `list_offers` offers, `evaluate_offers` results and `search_wines` wines (one row per best offer) and fills these keys itself. Build the rows yourself when you have extra context (`ref`, `group`, `flags`).

## Render

The renderer is in this reference skill. From a task skill's directory:

```
python3 ../wineauction-reference/scripts/render.py rows.json report.html \
  --title "<Seller> wine list: value check" \
  --eyebrow "WineAuction · <Seller> · <kind of list> · <date>" \
  --lede "Every bottle on the list against retail and exact-vintage auction prices, per 750 ml." \
  --method "Markup is the list price over the retail reference, per 750 ml." \
  --not-found not_found.json \
  --skipped "Skipped 12 by-the-glass, 140 spirits, 10 cocktails."
```

`--markup` shows markup over each reference (+N%, green at 0 or below, amber to 100%, red above) instead of discount: the badge columns, the filter, the best-value cards and their text all switch. Use it for restaurant lists.

`--not-found` and `--skipped` are optional. The page has best-value cards, a table with group tabs, a minimum-discount filter, a maximum price, sort, search, a doubtful-reference toggle and the not-found list. It flags an auction price from 1–2 sales and references more than 3× apart by itself, needs no server, and follows light or dark mode. When nothing matched, skip the page. Follow [design-system.md](design-system.md) for any other HTML view.

## In chat

Give only what the task skill asks for, and always:

- the reference each discount or markup is measured against;
- the matches flagged as doubtful, one line each (colour, cuvée or vintage mismatches first);
- what was not found;
- totals: rows parsed, evaluated, matched, not found, skipped by kind.
