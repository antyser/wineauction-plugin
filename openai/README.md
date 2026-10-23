# WineAuction

Compare presented wine offers with retail and auction market prices, and find wine prices, historical auction sales, current offers, and available critic reviews. The data comes from [WineAuction](https://wineauction.ai).

## Skills

- `restaurant-wine-list`: a restaurant wine list you bring (photo, PDF, link or text), or a named restaurant. Shows the markup of each bottle over retail and auction prices.
- `merchant-offer-check`: a merchant email, newsletter, futures offer, price list or a single quoted price. Judges each price against the market.
- `wine-info`: a wine, producer, vintage or region: retail and auction prices, past sales and critic reviews.
- `cellar-valuation`: a list of bottles you own. Value per bottle and in total, at auction and at retail.

## Data

The plugin does not collect anything itself. Each tool call sends your query (wine names, filters, or the prices you ask it to evaluate) to `https://wineauction.ai/api/mcp` and returns results. All tools are read-only. The HTML report is generated locally and loads Google Fonts when viewed with network access; without it, system fonts are used. See the [privacy policy](https://wineauction.ai/privacy) and [terms](https://wineauction.ai/terms).

## Support

[wineauction.ai/contact](https://wineauction.ai/contact)

Prices are USD per 750 ml. Auction prices include the buyer's premium.
