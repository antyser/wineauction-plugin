# search_wines

Find wines: price a list of named wines, follow a watch list, or find wines by region or colour. Each wine comes with both reference views and up to 2 offers. It filters by wine attributes only. For every offer of one wine, or to filter by price, discount or seller, use `list_offers`.

| Input | Type / values | Meaning |
|---|---|---|
| `query` | text, ≤200 chars | Free text: wine, producer or place. Matched word by word against the catalog and ranked by relevance; a year in it becomes `vintage`. |
| `wines` | list of ≤10 `{query` or `lwin7, vintage}` | Specific wines. Each is identified on its own; see `resolved_wines`. |
| `vintage`, `vintage_min`, `vintage_max` | year | One vintage, or a range (not both). A range lists only vintages that have price data. An explicit `vintage` beats a year in `query`; a year in `query` beats a range. |
| `producer` | text | Producer. |
| `region` | text | Broad region, e.g. Burgundy, Champagne. |
| `appellation` | text | Village or vineyard, e.g. Meursault, Bienvenues-Bâtard-Montrachet. |
| `classification` | text | e.g. Grand Cru, Premier Cru. |
| `color` | red / white / rose / sparkling / dessert / fortified | Colour. |
| `offer_types` | distinct values from auction / retail / restaurant; default auction and retail | Where `best_offers` come from. Restaurant needs a paid plan. |
| `limit` | 1–50, default 25 | Wines per page. |
| `cursor` | text | Previous page's `next_cursor`. |

| Output | Meaning |
|---|---|
| `wines[]` | One entry per wine and vintage. |
| `wines[].wine_id`, `wine_name`, `producer`, `vintage`, `region`, `appellation`, `color`, `lwin7` | The catalog wine. Pass `wine_id` to `list_offers` for every offer of the wine; pass `lwin7` to `evaluate_offers` or `list_offers`. |
| `wines[].wineapp_url` | The wine's page on wineauction.ai for this vintage. |
| `wines[].retail`, `wines[].auction` | The two reference views. |
| `wines[].offer_count` | Current offers for this wine. |
| `wines[].best_offers[]` | Up to 2 offer rows, largest discount first, without the wine fields and views already given above. |
| `wines[].reviews[]` | Up to 3 newest critic reviews for this wine and vintage (currently from K&L): `{author, text, url}`. `author` is the critic (e.g. Decanter), `text` starts with the score and is cut at 500 characters, `url` is the merchant page that published it. `url` may be null. Absent when there are none. An entry without a vintage gets reviews from all vintages. |
| `resolved_wines[]` | Only with `wines`: `{query, lwin7, status}`, status matched or not_found. |
| `has_more`, `next_cursor`, `as_of` | Paging and data time. |
