# WineAuction plugin

Check wine prices against market references, find deals in live auctions, and look up wines or regions with their best current offers. The data comes from [WineAuction](https://wineauction.ai).

## What it adds

- **WineAuction connector** (`https://wineauction.ai/api/mcp`): you sign in with your WineAuction account the first time you use it.
- **Skills:**
  - `price-check`: judge prices you already have, from a merchant newsletter, a price list or a restaurant wine list.
  - `auction-deals`: the best-value lots in one auction, filtered by region, colour or appellation.
  - `wine-report`: renders any of the above as an HTML page in the WineAuction design, with best-deal cards and a filterable table.
  - `wineauction-tools`: what every tool input and output field means. Short conventions plus one reference file per tool.
  - `deal-watch`: wines, a producer or a region with market references and their best current offers, optionally checked on a schedule.

## Install

Claude Code:

```
/plugin marketplace add antyser/wineauction-plugin
/plugin install wineauction@wineauction
```

Then run `/mcp` and sign in to `wineauction`.

Codex and ChatGPT:

```
codex plugin marketplace add antyser/wineauction-plugin
```

Then install **WineAuction** from the plugin directory in the app and sign in when asked. The repo carries both manifests: `.claude-plugin/` and `.mcp.json` for Claude, `plugin.json`, `mcp.json` and `.agents/plugins/` for OpenAI. The skills in `skills/` are shared.

Claude (web and desktop) and Cowork: go to Customize > Plugins, add the marketplace `antyser/wineauction-plugin`, then install **WineAuction**. Open the plugin's Connectors tab and connect the WineAuction connector, signing in with your WineAuction account.

## Data

The plugin does not collect anything itself. Each tool call sends your query (wine names, filters, or the prices you ask it to evaluate) to `https://wineauction.ai/api/mcp` and returns results. All tools are read-only. The `wine-report` page is generated locally and loads Google Fonts when viewed with network access; without it, system fonts are used. See the [privacy policy](https://wineauction.ai/privacy) and [terms](https://wineauction.ai/terms).

## Support

Open an issue at [github.com/antyser/wineauction-plugin/issues](https://github.com/antyser/wineauction-plugin/issues).

## Notes

- Prices are USD per 750 ml. Auction prices include the buyer's premium.
- `evaluate_offers` uses one Wine Price Query per row: free accounts get 500 per month.
- The tools only read data. They cannot bid, buy or contact anyone.
