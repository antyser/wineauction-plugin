---
name: wineauction-tools
description: Explains every input and output field of the WineAuction tools (search_wines, list_offers, evaluate_offers, list_auctions, list_retail_stores, list_restaurants). Use before building a WineAuction call, or when a user asks what a field, discount or reference price in the results means.
---

# WineAuction tool fields

The tools come from the WineAuction connector. This page holds the conventions shared by all of them; open the file for the tool you are calling.

## Conventions

- Every field ending in `_usd` is US dollars per 750 ml, buyer's premium included. `price` is the seller's own price, in its own currency, for `bottles` bottles; an auction `price` excludes the premium.
- Discount = (1 − price per bottle / reference) × 100, one decimal. Positive means cheaper than the reference, negative dearer; null when either side is missing.
- Times are ISO 8601 UTC.
- Paging: pass the previous page's `next_cursor` as `cursor`. A null `next_cursor` means there are no more pages.
- `notice`, `resolved_wines`, `facets` and `vintages` appear only when they have content. Other fields are null when they have no value.
- Errors come back as `{error: {code, message, fields}}`; `fields` names the bad inputs. A rejected request uses no quota.

## Reference views

Each wine (wine plus vintage) carries two reference prices side by side. Either is null when there is no data.

| View | Fields | Meaning |
|---|---|---|
| `retail` | `price_usd`, `live_offer_count` | Lowest retail price. Falls back from offers seen in the last 30 days to one year, then to neighbouring vintages, then to Wine-Searcher. `live_offer_count` 0 means only past offers. |
| `auction` | `price_usd`, `sale_count`, `last_sale_at` | Median hammer price with premium over the last 5 years, this vintage only; null when the vintage has no sales. With `sale_count` of 1–2 the reference is shaky. |

## Tool index

| Tool | Use it for | Fields |
| --- | --- | --- |
| `search_wines` | Finding wines by name or attributes, with both references and up to 2 offers each | [references/search_wines.md](references/search_wines.md) |
| `list_offers` | Every offer for one wine, or the offers in one auction, house, store or restaurant; also closed auction results. Defines the offer row | [references/list_offers.md](references/list_offers.md) |
| `evaluate_offers` | Judging priced offers the user brings (metered) | [references/evaluate_offers.md](references/evaluate_offers.md) |
| `list_auctions` | Auction events, not lots | [references/list_auctions.md](references/list_auctions.md) |
| `list_retail_stores` | Finding a store for `merchant_id` | [references/list_retail_stores.md](references/list_retail_stores.md) |
| `list_restaurants` | Finding a restaurant for `merchant_id` | [references/list_restaurants.md](references/list_restaurants.md) |

Show results to the user with the `wine-report` skill.
