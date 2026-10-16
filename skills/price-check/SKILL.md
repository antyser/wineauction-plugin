---
name: price-check
description: Turns a wine list, merchant newsletter or price list (PDF, photo, web page, URL or pasted text) into priced rows, judges every row with evaluate_offers against WineAuction retail and auction references, and delivers one filterable HTML report. Use for "check this wine list", "is this newsletter any good", or "is this a good price" for one or more wines.
---

# Price check

The user brings wines with prices: a restaurant wine list, a merchant email or newsletter, a futures offer, or a price list. This skill runs the whole job in one pass: extract the text, parse it into rows, evaluate every row, and render one HTML report.

The tools come from the WineAuction connector. Work in a folder of your own and keep every intermediate file there.

## 1. Get the text

- PDF: run `pdftotext -layout list.pdf list.txt` when it is installed; otherwise read the PDF directly. If a page yields no text, it is a scan: read that page as an image.
- Web page or saved HTML: strip it to text with a short Python script (`html.parser`). Shops often hold the real product data in embedded JSON (`application/ld+json`, or a Shopify `product` object); prefer that over the visible text. If the page says it shows only part of the results ("24 of 42"), say so in the reply.
- URL: download it first, then treat it as a PDF or a web page.
- Photo or screenshot: read it as an image.
- Pasted text: use it as is.

For a long list, parse with a script rather than by hand, then check a sample of rows from several pages against the page images, especially where columns sit side by side.

Keep the section headings (Champagne, Burgundy, Reds, Half bottles and so on). Skip cover, introduction and by-the-glass pages, and wine prose that names wines without a price.

## 2. Parse into rows

Make one row per wine and bottle price. Keep what the source states, and do not guess missing facts:

- `raw_wine_name`: producer first, then the cuvée and appellation, then the colour when the wine is not red, then the vintage. For example "Louis Roederer Cristal Brut 2015", "Château Carbonnieux Pessac-Léognan Blanc 2019", "Domaine Tempier Bandol Rosé 2023". When the colour or grape comes only from the section heading ("White Bordeaux", "Chardonnay"), add it to the name: without it, a white or rosé is usually matched to the producer's red. Restaurant rows have no `producer` field, so the producer goes in the name. Fix plain typos ("Louis Roeder" → "Louis Roederer") because they break matching; keep everything else as written.
- `vintage`: the year, if the source gives it. Leave it out for NV.
- `price`, `currency`: the price as printed. Use USD unless the source says otherwise. Every row needs a price.
- `quantity`: the bottles the price covers. A case, OWC or 6-pack price covers 12 or 6 ("From $X / OWC6" is a 6-bottle price). Restaurant rows default to 1.
- `format_ml`: 375, 750, 1500 and so on. Read it from a "Half bottles", "Demi" or "Magnum" heading or a size in the line; default 750. A heading's size applies to every line under it until the next heading.
- `offer_type`: `restaurant` for a wine list; `retail` for a shop, newsletter, futures offer or price list.
- `section`: the list heading, on restaurant rows only.
- `producer`: on retail rows, the producer when the source names it separately.
- `is_pre_arrival` (retail): true when the line says pre-arrival or pre-sale. `is_future` (retail): true for en primeur or futures.
- `is_mixed_lot`: true when one price covers different wines (a mixed case). It still gets matched, but no per-bottle price exists; list it in the reply and leave it out of the report.
- A line with several vintages becomes one row per vintage; a wine listed in two sizes becomes one row per size. A wine listed twice at different prices stays twice.

Skip by-the-glass and carafe prices, coravin pours, flights, cocktails, beer, cider, sake and spirits. Also skip sherry, vermouth, port and dessert-wine sections when their prices are clearly per pour: a price far below any bottle on the list, or a section that gives a pour size. Where a line shows glass and bottle prices side by side, keep only the bottle price. When unsure, keep the row and flag it. Count what you skipped, by kind.

Keep a separate `refs.json`, in the same order as the rows, with what the report needs but the tool must not receive:
- `ref`: a short locator. Use the bin number, else the SKU, else page and line ("p15 #3"), never the whole line.
- `group`: a short tab name, at most about 12 distinct values per report. Use the broad section on a restaurant list ("Champagne", "White Burgundy", "Half bottles"), else the region.
- `printed_price` and any flag you already have.

Write the rows to `rows_in.json` before calling any tool, so a failed call can be retried without re-parsing.

## 3. Evaluate

1. Call `evaluate_offers` with `offers` (the rows) and `source` (`{merchant_name, document_title, observed_at, merchant_url}`). The tool rejects any field it does not know, so send only the fields from step 2.
2. Send 25 rows per call, one call after another. A 100-row response is about 80 KB and many clients cannot show it inline. After each call, append the response to `results.json` before the next call. Each row counts as one Wine Price Query; there is no cap. A 1,000-row list takes about 40 calls and 20–30 minutes; tell the user that before you start a list that large.
3. If a call fails, keep the results you already have, render a partial report from them, and tell the user how many rows were evaluated and how many remain.
4. Read each result:
   - `outcome: unmatched`: no wine was found. Retry once, in one batch at the end, any unmatched row whose name you can make fuller (full producer name, cuvée, appellation) or correct. List what is still unmatched under "not found". Do not invent a price.
   - `wine`: `wine_id`, `display_name`, `producer`, `region`, `country`, `lwin7`, `lwin11`, `slug`. The matched vintage is the last four digits of `lwin11`; `wineapp_wine_url` ends with the vintage too.
   - `unit_price.amount`: the price per 750 ml in USD. A $99 half bottle shows as $198, and a $300 magnum as $150.
   - `retail`: the retail reference per 750 ml, with `live_offer_count` (0 means only past offers). `auction`: the exact-vintage auction median per 750 ml, with `sale_count`; null when that vintage has no sales.
   - `discount_vs_retail_pct`, `discount_vs_auction_pct`: positive means cheaper than the reference. On a restaurant list both are usually negative; the negative of `discount_vs_retail_pct` is the markup over retail.
5. Check every match against the line it came from, and flag rather than trust it when:
   - `display_name` names a different wine, cuvée or colour (a "Blanc" line matched to the red, a Chardonnay matched to the Pinot Noir), or a different vintage, or NV against a vintage;
   - the retail and auction references are more than 3× apart, or the retail reference is below a third of a retail list price;
   - a matched row has neither reference: report it as "no market data" instead of a discount;
   - the row is a half bottle or a large format: the references are for 750 ml bottles, so large formats normally cost more per 750 ml;
   - on a retail list, the retail discount is exactly 0: the merchant's own listing may be the reference. Rank that list by `discount_vs_auction_pct` instead.

## 4. Render the report

Write `rows.json` with one object per matched row that has a unit price:

| key | from |
| --- | --- |
| `name` | wine name with producer (no vintage) |
| `vintage` | vintage |
| `group`, `ref` | from `refs.json` |
| `seller` | the restaurant or merchant |
| `bottles`, `size_ml` | `quantity` and `format_ml` |
| `price_usd` | the evaluate result's `unit_price.amount` (per 750 ml) |
| `retail_usd`, `retail_live` | `retail.price_usd`, `retail.live_offer_count` |
| `auction_usd`, `auction_sales` | `auction.price_usd`, `auction.sale_count` |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | as returned |
| `wineapp_url` | `wineapp_wine_url` |
| `flags` | a list of short strings: every doubt from step 3.5, and "Printed $99 for 375 ml" on half bottles and large formats |

Write `not_found.json` as a list of `{name, hint}` for the rows still unmatched. Then run, from this skill's directory or with absolute paths:

```
python3 scripts/render.py rows.json report.html \
  --title "<Seller> wine list: value check" \
  --eyebrow "WineAuction · <Seller> · <kind of list> · <date>" \
  --lede "Every bottle on the list against retail and exact-vintage auction prices, per 750 ml." \
  --method "Markup is the list price over the retail reference, per 750 ml." \
  --not-found not_found.json \
  --skipped "Skipped 12 by-the-glass, 140 spirits, 10 cocktails."
```

The page has best-value cards, a table with group tabs, a minimum-discount filter, a max price per bottle, sort, search and a doubtful-reference toggle, and the not-found list. It flags by itself an auction price from 1–2 sales and references more than 3× apart. It needs no server and follows the viewer's light or dark mode. If the client can show an HTML artifact, show the page there; otherwise give the user the file. When nothing matched, skip the page and give only the chat reply.

## 5. Reply in chat

Give these short lists:
- the five best values (smallest markup on a restaurant list, biggest discount otherwise), leaving out flagged rows;
- anything clearly overpriced;
- the matches you flagged as doubtful, in one line each;
- wines that were not found;
- the totals: rows parsed, evaluated, matched, not found, skipped by kind.

Never claim a wine is in stock or can be bought at the reference price. The references are market prices, not offers.
