# Presenting results

**Up to about 10 rows**: answer in chat. **More**: render one self-contained HTML page and give the user the file; show it as an HTML artifact when the client can.

## Rows from list_offers or search_wines

Build `rows.json` with one row per offer (rows from `evaluate_offers` are described in [evaluate.md](evaluate.md)). Leave mixed lots out and mention notable ones in the reply.

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

`--not-found` and `--skipped` are optional. The page has best-value cards, a table with group tabs, a minimum-discount filter, a maximum price, sort, search, a doubtful-reference toggle and the not-found list. It flags an auction price from 1–2 sales and references more than 3× apart by itself, needs no server, and follows light or dark mode. When nothing matched, skip the page. Follow [design-system.md](design-system.md) for any other HTML view.

## In chat

Give only what the task skill asks for, and always:

- the reference each discount or markup is measured against;
- the matches flagged as doubtful, one line each (colour, cuvée or vintage mismatches first);
- what was not found;
- totals: rows parsed, evaluated, matched, not found, skipped by kind.
