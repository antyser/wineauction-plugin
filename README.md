# WineAuction plugin

Check wine prices against market references, find deals in live auctions, and look up wines or regions with their best current offers. The data comes from [WineAuction](https://wineauction.ai).

## What it adds

- **WineAuction connector** (`https://wineauction.ai/api/mcp`): you sign in with your WineAuction account the first time you use it.
- **Skills**, organised by what you want:
  - `check-offers`: you already have offers. Bring a wine list, merchant newsletter, price list or pasted text, or name an auction, auction house, store or restaurant, and get the ones worth attention, with an HTML report for long lists.
  - `find-wine`: you have no offers yet. Name wines, a producer, a region or a style and get market references with the best current offers, optionally rechecked on a schedule.

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

The plugin does not collect anything itself. Each tool call sends your query (wine names, filters, or the prices you ask it to evaluate) to `https://wineauction.ai/api/mcp` and returns results. All tools are read-only. The HTML report is generated locally and loads Google Fonts when viewed with network access; without it, system fonts are used. See the [privacy policy](https://wineauction.ai/privacy) and [terms](https://wineauction.ai/terms).

## Support

Open an issue at [github.com/antyser/wineauction-plugin/issues](https://github.com/antyser/wineauction-plugin/issues).

## Notes

- Prices are USD per 750 ml. Auction prices include the buyer's premium.
- `evaluate_offers` judges up to 25 rows per call in the skills; long lists are sent in batches.
- The tools only read data. They cannot bid, buy or contact anyone.

## Build and verify a release

Both versioned manifests use the same release version. The portable package keeps `plugin.json`, `mcp.json`, `skills/` and `assets/` at the repository root; the Claude marketplace manifests remain available alongside them. The 30-row newsletter under `review/fixtures/` is synthetic supplied-price input for workflow review, not a set of real merchant offers or market references.

After committing the release candidate, build the ZIP from tracked files with:

```
python3 scripts/build_release.py
```

The default output is `~/Downloads/wineauction-plugin-1.1.0.zip`. To verify a candidate commit and its packaged renderer, run:

```
scripts/local_ci.sh "$(git rev-parse HEAD)"
```

The local check requires a clean checkout at the supplied commit, validates the manifests and review cases, builds and inspects the ZIP, and exercises the renderer from the archive. It uses Python 3 and Node.js.
