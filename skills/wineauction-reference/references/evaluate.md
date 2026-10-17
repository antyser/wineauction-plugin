# Evaluating rows with evaluate_offers

Fields: [tools/evaluate_offers.md](tools/evaluate_offers.md).

## Calls

1. Call `evaluate_offers` with `offers` (the rows from [parse-list.md](parse-list.md)) and `source` (`{merchant_name, document_title, observed_at, merchant_url}`). The tool rejects any field it does not know, so send only the row fields.
2. Send 25 rows per call, one call after another. Larger responses are too big for many clients to show. Save each response to disk (`results.json`) before the next call, and collect every batch before you report. A 1,000-row list takes about 40 calls and 20–30 minutes; say so before starting a list that large.
3. If a call fails, keep the results you have, render a partial report from them, and say how many rows were evaluated and how many remain.

## Checking each result

- `outcome: unmatched`: no wine was found. Retry once, in one batch at the end, every unmatched row whose name you can make fuller (full producer name, cuvée, appellation) or correct. List what is still unmatched as not found. Never invent a price.
- `outcome: not_computed`: identification failed; retry it once.
- Compare `wine.display_name`, `wine.color` and `wine.vintage` with the line. Flag rather than trust a match that names a different wine, cuvée or colour (a "Blanc" line matched to the red, a Chardonnay matched to the Pinot Noir), a different vintage, or NV against a vintage.
- Apply the doubtful-reference rules in [prices.md](prices.md).

## Report rows

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
| `flags` | short strings for every doubt, and "Printed $99 for 375 ml" on half bottles and large formats |

Write `not_found.json` as a list of `{name, hint}` for the rows still unmatched. Then present with [report.md](report.md).
