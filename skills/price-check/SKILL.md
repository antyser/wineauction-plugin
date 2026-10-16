---
name: price-check
description: Turns a wine list, merchant newsletter or price list (PDF, photo, URL or pasted text) into priced rows, judges every row with evaluate_offers against WineAuction retail and auction references, and delivers one filterable HTML report. Use for "check this wine list", "is this newsletter any good", or "is this a good price" for one or more wines.
---

# Price check

The user brings wines with prices: a restaurant wine list, a merchant email or newsletter, or a price list. This skill runs the whole job in one pass: extract the text, parse it into rows, evaluate every row, and render one HTML report.

The tools come from the WineAuction connector.

## 1. Get the text

- PDF: run `pdftotext -layout list.pdf list.txt` when it is installed; otherwise read the PDF directly. If a page yields no text, it is a scan: read that page as an image.
- URL: download it first, then treat it as a PDF or a web page.
- Photo or screenshot: read it as an image.
- Pasted text: use it as is.

Keep the section headings (Champagne, Burgundy, Reds, Half bottles and so on). They become the report's tabs.

## 2. Parse into rows

Make one row per wine and bottle price. Keep what the source states, and do not guess missing facts:

- `raw_wine_name`: producer, wine and appellation as written, plus the vintage.
- `vintage`: the year, if the source gives it. Leave it out for NV.
- `price`, `currency`: the bottle price. Use USD unless the source says otherwise.
- `quantity`: the bottles the price covers. A case or 6-pack price covers 12 or 6.
- `format_ml`: 375, 750, 1500 and so on. Read it from a "Half bottles" or "Magnum" heading or a size in the line; default 750.
- `offer_type`: `restaurant` for a wine list, `retail` for a shop, newsletter or price list.
- Also keep, for the report only: the section heading (`group`) and the list's own line number or bin (`ref`).

Skip by-the-glass prices, coravin pours, flights, cocktails, beer, sake and spirits. Count what you skipped. Write the rows to `rows_in.json` before calling any tool, so a failed call can be retried without re-parsing.

## 3. Evaluate

1. Put where the rows came from in `source`: restaurant or merchant, document title and date.
2. Call `evaluate_offers` with up to 100 rows per call, in order. Each row costs one Wine Price Query. If a batch is larger than the remaining allowance, the call is rejected and nothing is charged: stop, and tell the user how many rows were evaluated and how many remain.
3. Read each result:
   - `outcome: unmatched`: list it under "not found" with the hint. Do not invent a price.
   - `retail`: the retail reference. `live_offer_count` 0 means only past offers.
   - `auction`: the exact-vintage auction reference, null when that vintage has no sales. Quote `sale_count` with it.
   - `discount_vs_retail_pct` and `discount_vs_auction_pct`: positive means cheaper than the reference. On a restaurant list both are usually negative; the negative of `discount_vs_retail_pct` is the markup over retail.
4. Check every match against the line it came from: producer, wine and vintage must agree. When the match is a different wine or vintage, flag it in `flags` rather than trusting the discount.

## 4. Render the report

Write `rows.json` with one object per matched row:

| key | from |
| --- | --- |
| `name` | wine name with producer (no vintage) |
| `vintage` | vintage |
| `group` | the list section for a restaurant list, else the region |
| `seller` | the restaurant or merchant |
| `ref` | the list's line number, bin or SKU |
| `bottles`, `size_ml` | `quantity` and `format_ml` |
| `price_usd` | the evaluate result's `unit_price.amount` (per 750 ml) |
| `retail_usd`, `retail_live` | `retail.price_usd`, `retail.live_offer_count` |
| `auction_usd`, `auction_sales` | `auction.price_usd`, `auction.sale_count` |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | as returned |
| `wineapp_url` | the wineauction.ai page from the result |
| `flags` | anything you doubted, such as "matched a different vintage" or "price looks like a case price" |

Then run, from this skill's directory or with absolute paths:

```
python3 scripts/render.py rows.json report.html \
  --title "Macarena wine list: value check" \
  --eyebrow "WineAuction · Macarena · restaurant list · 16 Oct 2026" \
  --lede "Every bottle on the list against retail and exact-vintage auction prices, per 750 ml." \
  --method "Markup is the list price over the lowest retail reference."
```

The page has best-deal cards and a table with section tabs, a minimum-discount filter, a max price per bottle, sort, search and a "Show doubtful references" toggle. It flags by itself an auction price from 1–2 sales and references more than 3× apart. It needs no server and follows the viewer's light or dark mode. If the client can show an HTML artifact, show the page there; otherwise give the user the file.

## 5. Reply in chat

Give four short lists:
- the five best values (lowest markup on a restaurant list, biggest discount otherwise);
- anything clearly overpriced;
- wines that were not found, with the hint for each;
- the totals: rows parsed, evaluated, matched, not found, skipped.

Never claim a wine is in stock or can be bought at the reference price. The references are market prices, not offers.
