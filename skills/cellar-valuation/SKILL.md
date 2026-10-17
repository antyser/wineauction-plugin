---
name: cellar-valuation
description: "Value a collection of wines the user owns, bottle by bottle and in total, from retail and auction reference prices. Use when the user shares a cellar list, inventory spreadsheet, CellarTracker or Vivino export, or a list of bottles they own and asks what it is worth, for insurance, resale or estate purposes."
---

# Cellar valuation

The user has no prices, only bottles. Value each at the auction median (what similar bottles have sold for) and the retail reference (what replacing it would cost), and keep the two totals separate.

## Steps

1. Read the list into rows of `{name, vintage, bottles, size_ml}`, using the text-extraction and naming rules in [parse-list.md](../wineauction-reference/references/parse-list.md) (no price field). Save them to `cellar.json`.
2. Call `search_wines` with a `wines` list of up to 10 `{query, vintage}` per call, one call after another, saving each response ([fields](../wineauction-reference/references/tools/search_wines.md)). Check `resolved_wines`: retry a not-found name once with a fuller producer, cuvée or appellation, then list it as not valued.
3. Per row, multiply each reference per 750 ml by the bottles, adjusting for size (a magnum counts as 2 × 750 ml, a half as 0.5) and flag non-750 formats, since large formats usually trade above that.
4. Apply [prices.md](../wineauction-reference/references/prices.md): a value resting on 1–2 sales or on references more than 3× apart is flagged, and a row with neither reference counts as "no market data", not zero.

## Present

- Totals: auction-based value and retail-based value, each with how many bottles it covers, plus bottles not valued.
- The ten most valuable rows, and the flagged ones.
- More than about 10 rows: an HTML page per [report.md](../wineauction-reference/references/report.md), with `price_usd` left empty and the references filled, and a `--method` line saying values are references, not offers.

These are market references, not an appraisal; say so when the user mentions insurance or an estate.
