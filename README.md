# WineAuction plugin

Compare presented wine offers with retail and auction market prices, and find wine prices, historical auction sales, current offers, and available critic reviews. The data comes from [WineAuction](https://wineauction.ai).

## What it adds

- **WineAuction connector** (`https://wineauction.ai/api/mcp`): you sign in with your WineAuction account the first time you use it.
- **Skills**, one per use case:
  - `restaurant-wine-list`: a restaurant wine list you bring (photo, PDF, link or text), or a named restaurant. Shows the markup of each bottle over retail and auction prices.
  - `merchant-offer-check`: a merchant email, newsletter, futures offer, price list or a single quoted price. Judges each price against the market.
  - `auction-lots`: an auction sheet or lots you bring, or a named auction or house. Lots below market, lots ending soon, sale results, and a recurring watch.
  - `wine-info`: a wine, producer, vintage or region: retail and auction prices, past sales, critic reviews and where it is currently offered.
  - `cellar-valuation`: a list of bottles you own. Value per bottle and in total, at auction and at retail.
  - `wineauction-reference`: shared tool fields, price-reading rules, list parsing and the HTML report renderer that the skills above link to.

Version 1.2.0 reorganises the skills by use case. The tools are unchanged.

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

Natural-language skill-routing examples are kept separately in `review/trigger-cases.json`, one per task skill; the OpenAI review cases continue to cover the six connector tools and the existing workflow examples.

After committing the release candidate, build the ZIP from tracked files with:

```
python3 scripts/build_release.py
```

The default output is `~/Downloads/wineauction-plugin-1.2.0.zip`. To verify a candidate commit and its packaged renderer, run:

```
scripts/local_ci.sh "$(git rev-parse HEAD)"
```

The local check requires a clean checkout at the supplied commit, validates the manifests and review cases, builds and inspects the ZIP, and exercises the renderer from the archive. It uses Python 3 and Node.js.

### OpenAI package

OpenAI's plugin review blocks two skills, so the ZIP uploaded to OpenAI is a variant of the full plugin, built from the same commit:

- `python3 scripts/build_release.py` builds the full plugin for Claude and Codex (all five task skills and `skills/wineauction-reference`).
- `python3 scripts/build_openai_package.py` builds `~/Downloads/wineauction-plugin-1.2.0-openai.zip`. It drops `skills/auction-lots`, moves `skills/wineauction-reference` to a root `shared/` folder without its `SKILL.md` and `agents/`, rewrites the `../wineauction-reference/` links to `../../shared/`, then applies the files under `openai/` over the result (same paths as in the package): the app-name `plugin.json`, an `mcp.json` without its own OAuth block, the four task `SKILL.md` files and the shared references that use neutral price-research wording.

The OpenAI build checks that no file links to a missing path, that nothing still references `auction-lots` or `wineauction-reference`, and that no secret-like material is packaged. Both builds run in `scripts/local_ci.sh`. Edit the `openai/` copy, not the tracked file, to change what OpenAI receives.
