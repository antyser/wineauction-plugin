# list_auctions

Auction events, not lots. Pass an `auction_slug` to `list_offers` for the lots.

| Input | Type / values | Meaning |
|---|---|---|
| `house` | as in `list_offers` | Auction house. |
| `status` | live (default) / closed | Open or ended. |
| `ending_within_hours` | positive number | live only. |
| `ended_after`, `ended_before` | ISO time | closed only. |
| `sort` | end_time_asc / end_time_desc | Default: live soonest first, closed newest first. |
| `limit`, `offset` | 1–100, default 25 | Paging. |

| Output | Meaning |
|---|---|
| `auctions[].auction_id`, `auction_slug`, `auction_name`, `house` | The auction. |
| `auctions[].status`, `end_time` | live / closed and end time. |
| `auctions[].lot_count` | Number of lots. |
| `auctions[].buyers_premium_pct`, `currency` | Premium in percent and currency. |
| `auctions[].wineapp_url` | Auction page on wineauction.ai. |
| `total`, `has_more`, `next_offset`, `as_of` | Paging and data time. |
