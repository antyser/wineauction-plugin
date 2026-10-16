---
name: check-offers
description: The user already has offers and wants the ones worth attention. Takes a wine list, newsletter, price list or pasted text (PDF, photo, URL) and judges every row, or scans a named auction, house, store or restaurant list for deals. Use for "check this wine list", "is this newsletter any good", "is $85 fair for this wine", "best deals in the Acker sale".
---

# Check offers

The user already has offers. Find the ones worth attention. The tools come from the WineAuction connector. If the user has no offers and wants them found for particular wines, use the find-offers skill instead.

Pick the source:

- **A document or text they bring** (wine list, merchant email or newsletter, futures offer, price list, pasted lines, a price for one wine): parts A and C.
- **A named auction, auction house, store or restaurant**: parts B and C.

Work in a folder of your own and keep every intermediate file there.

## A. Judge a document

### 1. Get the text

- PDF: run `pdftotext -layout list.pdf list.txt` when it is installed; otherwise read the PDF directly. If a page yields no text, it is a scan: read that page as an image.
- Web page or saved HTML: strip it to text with a short Python script (`html.parser`). Shops often hold the real product data in embedded JSON (`application/ld+json`, or a Shopify `product` object); prefer that over the visible text. If the page says it shows only part of the results ("24 of 42"), say so in the reply.
- URL: download it first, then treat it as a PDF or a web page.
- Photo or screenshot: read it as an image.
- Pasted text: use it as is.

For a long list, parse with a script rather than by hand, then check a sample of rows from several pages against the page images, especially where columns sit side by side.

Keep the section headings (Champagne, Burgundy, Reds, Half bottles and so on). Skip cover, introduction and by-the-glass pages, and wine prose that names wines without a price.

### 2. Parse into rows

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

### 3. Evaluate

1. Call `evaluate_offers` with `offers` (the rows) and `source` (`{merchant_name, document_title, observed_at, merchant_url}`). The tool rejects any field it does not know, so send only the fields from step 2.
2. Send 25 rows per call, one call after another. A 100-row response is about 80 KB and many clients cannot show it inline. After each call, save the response to disk (`results.json`) before the next call, and collect every batch before you report. A 1,000-row list takes about 40 calls and 20–30 minutes; tell the user that before you start a list that large.
3. If a call fails, keep the results you already have, render a partial report from them, and tell the user how many rows were evaluated and how many remain.
4. Read each result (fields in [references/evaluate_offers.md](references/evaluate_offers.md)):
   - `outcome: unmatched`: no wine was found. Retry once, in one batch at the end, any unmatched row whose name you can make fuller (full producer name, cuvée, appellation) or correct. List what is still unmatched under "not found". Do not invent a price.
   - `wine.color` and `wine.vintage` are what the tool matched; compare them with the line.
5. Check every match against the line it came from, and flag rather than trust it when:
   - `wine.display_name` or `wine.color` names a different wine, cuvée or colour (a "Blanc" line matched to the red, a Chardonnay matched to the Pinot Noir), or `wine.vintage` is a different vintage, or NV against a vintage;
   - the retail and auction references are more than 3× apart, or the retail reference is below a third of a retail list price;
   - a matched row has neither reference: report it as "no market data" instead of a discount;
   - the row is a half bottle or a large format: the references are for 750 ml bottles, so large formats normally cost more per 750 ml;
   - on a retail list, the retail discount is exactly 0: the merchant's own listing may be the reference. Rank that list by `discount_vs_auction_pct` instead.

### Rows for the report (evaluate_offers)

Write `rows.json` with one object per matched row that has a unit price:

| key | from |
| --- | --- |
| `name` | wine name with producer (no vintage) |
| `vintage` | vintage |
| `group`, `ref` | from `refs.json` |
| `seller` | the restaurant or merchant |
| `bottles`, `size_ml` | `quantity` and `format_ml` |
| `price_usd` | the result's `unit_price.amount` (per 750 ml) |
| `retail_usd`, `retail_live` | `retail.price_usd`, `retail.live_offer_count` |
| `auction_usd`, `auction_sales` | `auction.price_usd`, `auction.sale_count` |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | as returned |
| `wineapp_url` | `wineapp_wine_url` |
| `flags` | short strings: every doubt from step 5, and "Printed $99 for 375 ml" on half bottles and large formats |

Write `not_found.json` as a list of `{name, hint}` for the rows still unmatched.

## B. Scan a named auction, house, store or restaurant

1. Identify the place.
   - Auction: call `list_auctions` (status `live`) and pick the sale by house and name; use its slug as `auction_slug`. If the user names only a house, use `house`.
   - Store or restaurant: find its `merchant_id` with `list_retail_stores` or `list_restaurants`, and set `offer_type` to `retail` or `restaurant`.
2. Call `list_offers` (fields in [references/list_offers.md](references/list_offers.md)) with:
   - `offer_type` (`auction` for a sale or house) and `status: live` unless the user asks about past sales;
   - the user's preferences as filters: `region`, `color`, `appellation`, `min_price_usd` / `max_price_usd` (per 750 ml); for auctions `mixed_lot: exclude` unless they want mixed lots;
   - `sort: discount_vs_retail` or `discount_vs_auction`, with `min_discount_pct` (20 is a sensible default);
   - `limit` 25, then page with `cursor` (the previous `next_cursor`) while the results stay interesting. Save each page to disk.
3. For each offer, compare `price_per_bottle_usd` (premium included; for an auction it uses the current bid, else the opening bid) with `retail.price_usd` and `auction.price_usd`. Treat the auction reference as weak when `auction.sale_count` is 1–2, and either reference as doubtful when the two differ by more than 3×.

### Rows for the report (list_offers)

One row per offer; leave mixed lots out (mention good ones in the reply).

| key | from |
| --- | --- |
| `name`, `vintage` | `wine_name` (or `listing_name`), `vintage` |
| `group` | `appellation` or `region`; colour when the user asked for one region |
| `ref` | "Lot <`auction_lot_number`>" for auctions, else a SKU or list section |
| `seller` | `seller_name`, plus `auction_name` for a sale |
| `bottles`, `size_ml` | `bottles`, `bottle_size_ml` |
| `price_usd` | `price_per_bottle_usd` |
| `retail_usd`, `retail_live`, `auction_usd`, `auction_sales` | from the `retail` and `auction` views |
| `discount_vs_retail_pct`, `discount_vs_auction_pct` | as returned |
| `url` | the seller's page for the offer |
| `wineapp_url` | the offer's `wineapp_url` |
| `ends_at` | `auction_end_time` |
| `flags` | doubts, such as "Retail from 2008 vintage" |

Prices rise as bidding goes on: say that an auction discount is at the current or opening bid, not at the likely hammer price.

## C. Present

**Up to about 10 rows**: answer in chat. **More**: render one self-contained HTML page and give the user the file; if the client can show an HTML artifact, show it there. Run it from this skill's directory or with absolute paths:

```
python3 scripts/render.py rows.json report.html \
  --title "<Seller> wine list: value check" \
  --eyebrow "WineAuction · <Seller> · <kind of list> · <date>" \
  --lede "Every bottle on the list against retail and exact-vintage auction prices, per 750 ml." \
  --method "Markup is the list price over the retail reference, per 750 ml." \
  --not-found not_found.json \
  --skipped "Skipped 12 by-the-glass, 140 spirits, 10 cocktails."
```

`--not-found` and `--skipped` are optional. The page has best-value cards, a table (wine, vintage, price per 750 ml, retail and auction references, both discounts, link to wineauction.ai) with group tabs, minimum-discount filter, max price per bottle, sort, search, a doubtful-reference toggle (on by default) and the not-found list. It flags by itself an auction price from 1–2 sales and references more than 3× apart. It needs no server and follows light or dark mode. The script also accepts raw `list_offers` offers, `evaluate_offers` results and `search_wines` wines, filling the keys above from their fields, but build the rows yourself when you have extra context (`ref`, `group`, `flags`). When nothing matched, skip the page. The template's design tokens are in [references/design-system.md](references/design-system.md).

In chat give only:
- the five best values (smallest markup on a restaurant list, biggest discount otherwise), leaving out flagged rows;
- anything clearly overpriced;
- the matches you flagged as doubtful, one line each (colour, cuvée or vintage mismatches first);
- wines not found;
- totals: rows parsed, evaluated, matched, not found, skipped by kind.

Never claim a wine is in stock or can be bought at the reference price. The references are market prices, not offers.

## Reading results

- `_usd` fields are US dollars per 750 ml; auction prices include the buyer's premium.
- Discount: positive means cheaper than the reference. Always say which reference you quote. On a restaurant list both are usually negative; the negative of `discount_vs_retail_pct` is the markup.
- `retail` and `auction` are the two references; either is null when there is no data. `auction` is this exact vintage only, so null means it never sold.
- Link a wine with `wineapp_wine_url` and an offer with `wineapp_url`, and an offer's own page with `url`.
- Field meanings for every tool are in `references/`: [evaluate_offers](references/evaluate_offers.md), [list_offers](references/list_offers.md), [list_auctions](references/list_auctions.md), [list_retail_stores](references/list_retail_stores.md), [list_restaurants](references/list_restaurants.md).
