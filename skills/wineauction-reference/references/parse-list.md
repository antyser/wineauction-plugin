# Parsing a list into rows

Work in a folder of your own and keep every intermediate file there.

## 1. Get the text

- PDF: run `pdftotext -layout list.pdf list.txt` when it is installed; otherwise read the PDF directly. A page with no text is a scan: read that page as an image.
- Web page or saved HTML: strip it to text with a short Python script (`html.parser`). Shops often hold the real product data in embedded JSON (`application/ld+json`, or a Shopify `product` object); prefer that over the visible text. If the page shows only part of the results ("24 of 42"), say so in the reply.
- URL: download it first, then treat it as a PDF or a web page.
- Photo or screenshot: read it as an image.
- Pasted text: use it as is.

For a long list, parse with a script rather than by hand, then check a sample of rows from several pages against the page images, especially where columns sit side by side.

Keep the section headings (Champagne, Burgundy, Reds, Half bottles and so on). Skip cover, introduction and by-the-glass pages, and prose that names wines without a price.

## 2. One row per wine and bottle price

Keep what the source states; do not guess missing facts.

- `raw_wine_name`: producer first, then the cuvée and appellation, then the colour when the wine is not red, then the vintage. For example "Louis Roederer Cristal Brut 2015", "Château Carbonnieux Pessac-Léognan Blanc 2019", "Domaine Tempier Bandol Rosé 2023". When the colour or grape comes only from the section heading ("White Bordeaux", "Chardonnay"), add it to the name: without it, a white or rosé is usually matched to the producer's red. Restaurant rows have no `producer` field, so the producer goes in the name. Fix plain typos ("Louis Roeder" → "Louis Roederer"); keep everything else as written.
- `vintage`: the year, if the source gives it. Leave it out for NV.
- `price`, `currency`: the price as printed. USD unless the source says otherwise. Every row needs a price.
- `quantity`: the bottles the price covers. A case, OWC or 6-pack price covers 12 or 6 ("From $X / OWC6" is a 6-bottle price). Restaurant rows default to 1.
- `format_ml`: 375, 750, 1500 and so on, from a "Half bottles", "Demi" or "Magnum" heading or a size in the line; default 750. A heading's size applies to every line under it until the next heading.
- `offer_type`: `restaurant` for a wine list; `retail` for a shop, newsletter, futures offer or price list.
- `section`: the list heading, on restaurant rows only.
- `producer`: on retail rows, when the source names it separately.
- `is_pre_arrival` (retail): true when the line says pre-arrival or pre-sale. `is_future` (retail): true for en primeur or futures.
- `is_mixed_lot`: true when one price covers different wines (a mixed case). It still gets matched, but has no per-bottle price; list it in the reply and leave it out of the report.
- A line with several vintages becomes one row per vintage; a wine in two sizes becomes one row per size. A wine listed twice at different prices stays twice.

Skip by-the-glass and carafe prices, Coravin pours, flights, cocktails, beer, cider, sake and spirits. Also skip sherry, vermouth, port and dessert-wine sections when their prices are clearly per pour: far below any bottle on the list, or a section that gives a pour size. Where a line shows glass and bottle prices side by side, keep only the bottle price. When unsure, keep the row and flag it. Count what you skipped, by kind.

## 3. Side file for the report

Keep `refs.json`, in the same order as the rows, with what the report needs but the tool must not receive:

- `ref`: a short locator: the bin number, else the SKU, else page and line ("p15 #3"), never the whole line.
- `group`: a short tab name, at most about 12 distinct values per report: the broad section on a restaurant list ("Champagne", "White Burgundy", "Half bottles"), else the region.
- `printed_price` and any flag you already have.

Write the rows to `rows_in.json` before calling any tool, so a failed call can be retried without re-parsing.
