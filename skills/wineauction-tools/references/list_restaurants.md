# list_restaurants

Find a restaurant, then pass its `id` as `merchant_id` to `list_offers`.

| Input | Type / values | Meaning |
|---|---|---|
| `search` | text | Name. |
| `country` | text | Country. |
| `near_latitude`, `near_longitude` | coordinates | Sort by distance; rows gain `distance_miles`. |
| `limit`, `offset` | default 100; max 300 | Paging. |

| Output | Meaning |
|---|---|
| `id`, `slug`, `name` | The merchant; `id` is `list_offers` `merchant_id`. |
| `city`, `state`, `country` | Location. |
| `michelin_stars`, `star_wine_list_award`, `wine_spectator_award`, `cuisine` | Ratings and cuisine. |
| `total_wines`, `last_scraped_at` | Current offers and last crawl. |
| `wineapp_url` | Page on wineauction.ai. |
| `total`, `has_more` | Paging. |
