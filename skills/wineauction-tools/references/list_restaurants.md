# list_restaurants

Find a restaurant, then pass its `id` as `merchant_id` to `list_offers`.

| Input | Type / values | Meaning |
|---|---|---|
| `search` | text | Name. |
| `country` | text | Country. |
| `near_latitude`, `near_longitude` | coordinates | Sort by distance; rows then carry `distance_miles`. |
| `limit`, `offset` | default 100, max 300 | Paging. |

| Output | Meaning |
|---|---|
| `restaurants[]` | One row per restaurant. |
| `restaurants[].id`, `slug`, `name` | The restaurant; `id` is `list_offers` `merchant_id`. |
| `restaurants[].city`, `state`, `country`, `neighborhood`, `metro_area`, `latitude`, `longitude` | Location. |
| `restaurants[].michelin_stars`, `michelin_designation`, `star_wine_list_award`, `wine_spectator_award`, `cuisine` | Ratings and cuisine. |
| `restaurants[].total_wines`, `last_scraped_at` | Current wines on the list and last crawl. |
| `restaurants[].wineapp_url` | Page on wineauction.ai. |
| `total`, `offset`, `limit`, `has_more` | Paging: the next page starts at `offset + limit`; there is no `next_offset`. |
