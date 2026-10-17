# list_retail_stores

Find a store, then pass its `id` as `merchant_id` to `list_offers`.

| Input | Type / values | Meaning |
|---|---|---|
| `query` | text | Name. |
| `countries`, `states`, `cities` | `{include, exclude}` lists | Location. |
| `near_latitude`, `near_longitude` | coordinates | Sort by distance; rows then carry `distance_miles`. |
| `limit`, `offset` | default 30, max 300 | Paging. |

| Output | Meaning |
|---|---|
| `merchants[]` | One row per store. |
| `merchants[].id`, `slug`, `name`, `merchant_type` | The store; `id` is `list_offers` `merchant_id`. |
| `merchants[].city`, `state`, `country` | Location. |
| `merchants[].website_url` | Website. |
| `merchants[].total_wines`, `last_scraped_at` | Current offers and last crawl. |
| `merchants[].distance_miles` | Only with `near_latitude` and `near_longitude`. |
| `total`, `has_more`, `next_offset` | Paging: pass `next_offset` as `offset`. |
