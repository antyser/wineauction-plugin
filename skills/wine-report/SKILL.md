---
name: wine-report
description: Renders WineAuction price results (evaluate_offers, list_offers, search_wines) as one self-contained HTML page in the WineAuction design, with best-deal cards and a filterable table (group tabs, minimum discount, max price per bottle, sort, search, doubtful-reference toggle). Use after price-check, auction-deals or deal-watch whenever there are more than a handful of rows, or when the user asks for a page, report or table to look at.
---

# Wine report

Turn tool results into rows, fill `assets/report.html` with `scripts/render.py`, and give the user the HTML file. If the client can show an HTML artifact, show the page there instead.

## Row format

Write a JSON list with one object per wine, lot or listing. Leave a key out, or set it to null, when the data has no value.

| key | from |
| --- | --- |
| `name` | wine name with producer (no vintage) |
| `vintage` | vintage |
| `group` | tab to filter on: region, appellation, colour, or the list section of a restaurant list. Use one kind for the whole report |
| `seller` | auction house, merchant or restaurant |
| `ref` | lot number, list line or SKU |
| `bottles`, `size_ml` | bottles and bottle size |
| `price_usd` | price per 750 ml in USD: `price_per_bottle_usd`, or the evaluate result's `unit_price.amount` |
| `retail_usd`, `retail_live` | `retail.price_usd`, `retail.live_offer_count` |
| `auction_usd`, `auction_sales` | `auction.price_usd`, `auction.sale_count` |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | as returned; positive means cheaper than the reference |
| `url` | the seller's page for the offer |
| `wineapp_url` | the wineauction.ai page (`wineapp_url` or `wineapp_wine_url`) |
| `ends_at` | `auction_end_time` |
| `flags` | short notes on anything you judged doubtful, such as "Retail from 2008 vintage" |

The page adds two flags by itself:
- an auction price from 1–2 sales;
- retail and auction references more than 3× apart.

Rows that carry a flag are hidden until the user ticks "Show doubtful references".

Leave unmatched wines and mixed lots out of the rows. List them in the chat reply instead.

## Render

```
python3 scripts/render.py rows.json report.html \
  --title "Acker Autumn Harvest: white Burgundy deals" \
  --eyebrow "WineAuction · Acker · live lots · 16 Oct 2026" \
  --lede "Every white Burgundy lot, priced per 750 ml with the 25% premium, against retail and exact-vintage auction prices." \
  --method "Price per bottle uses the current bid, or the starting bid when there is none."
```

Run it from this skill's directory, or pass absolute paths. The script exits with a clear message when the rows file is missing or is not valid JSON. Keep the title to one line. Put the as-of time and the data scope in the eyebrow.

The page:
- needs no server;
- loads only Google Fonts; without network access it falls back to system fonts and stays fully usable;
- follows the viewer's light or dark mode.

See `references/design-system.md` for the tokens if the template has to be adapted.
