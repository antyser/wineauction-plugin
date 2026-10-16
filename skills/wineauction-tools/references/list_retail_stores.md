# list_retail_stores

Find a store, then pass its `id` as `merchant_id` to `list_offers`. Needs sign-in.

| Input | Type / values | Meaning |
|---|---|---|
| `query` | text | Name. |
| `countries`, `states`, `cities` | `{include, exclude}` | Location. |
| `near_latitude`, `near_longitude` | coordinates | Sort by distance; rows gain `distance_miles`. |
| `limit`, `offset` | default 30; max 300 | Paging. |

| Output | Meaning |
|---|---|
| `id`, `slug`, `name` | The merchant; `id` is `list_offers` `merchant_id`. |
| `city`, `state`, `country` | Location. |
| `website_url` | Website. |
| `total_wines`, `last_scraped_at` | Current offers and last crawl. |
| `total`, `has_more` | Paging. |
