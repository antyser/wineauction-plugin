# evaluate_offers

Judge priced offers the user brings: a retail email, a price list, a restaurant list or auction lots. Each row counts as one Wine Price Query; there is no cap. Every row needs a price; to look up prices without one, use `search_wines`.

| Input | Type / values | Meaning |
|---|---|---|
| `offers[]` | 1–100 rows | One wine and its offer per row. |
| `offers[].offer_type` | retail / restaurant / other | Where the offer comes from; other is priced like retail. |
| `offers[].raw_wine_name` | text | The wine as written, vintage included. |
| `offers[].lwin7` | 7 digits | Known LWIN; skips name matching. |
| `offers[].vintage` | 1700–2099 | Vintage; when absent, the single year in `raw_wine_name`. |
| `offers[].price`, `currency` | positive number, 3-letter code; `price` required | The quoted price for `quantity` bottles. A row without a price rejects the whole request, uncharged. |
| `offers[].quantity` | whole number 1–100,000 | Bottles the price covers. Restaurant rows default to 1; retail and other rows need it, else `unit_price` is `{reason: missing_quantity}`. |
| `offers[].format_ml` | positive integer | Bottle size; when absent, read from the name (375ml, 1.5L), else 750. |
| `offers[].buyers_premium` | 0–1, e.g. 0.25 | Pass when `price` is an auction hammer price; the unit price adds it. |
| `offers[].is_mixed_lot` | boolean, default false | The price covers several wines (no per-bottle price). |
| `offers[].source_url` | URL | Page where the offer is listed. |
| `offers[].is_out_of_stock`, `is_pre_arrival`, `is_in_bond`, `is_future` | boolean | Retail row status, recorded as given. |
| `offers[].serving_type`, `section` | text | Restaurant rows: bottle / glass, section of the list. |
| `source` | `{merchant_name, merchant_url, location, document_title, observed_at, notes}` | Where the rows came from; logged, never used for pricing. |
| `include_vintages` | boolean, default false | Also return both views for other vintages, to find the value vintage. |

| Output | Meaning |
|---|---|
| `results[]` | One per input row, in order. |
| `results[].input` | The row as sent. |
| `results[].outcome` | matched / unmatched (no such wine; read `hint`) / not_computed (identification failed; retry). |
| `results[].wine` | The identified wine: `wine_id`, `display_name`, `producer`, `region`, `country`, `lwin7`, `lwin11`, `slug`. The matched vintage is the last four digits of `lwin11`. There is no colour field; check the colour against `display_name`. |
| `results[].wineapp_wine_url` | The wine's page on wineauction.ai for this vintage. |
| `results[].unit_price` | `{amount, currency: USD, per_ml: 750, buyers_premium}`, or `{reason}` when it cannot be computed: missing_currency, missing_fx_rate, missing_quantity, missing_format_ml, mixed_lot, missing_buyers_premium. |
| `results[].retail`, `auction` | The two views. Without a vintage, retail pools all vintages and auction is null. |
| `results[].discount_vs_retail_pct`, `discount_vs_auction_pct` | Discount of `unit_price` against each view. |
| `results[].vintages[]` | Only with `include_vintages`: `{vintage, retail, auction}`. |
| `results[].hint` | What to pass next. |
| `as_of` | Data time. |

Show results to the user with the `wine-report` skill; price-check renders its own report.
