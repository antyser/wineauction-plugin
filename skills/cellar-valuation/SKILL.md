---
name: cellar-valuation
description: "Value wines the user owns, from one bottle to a whole collection, per wine and in total, from retail and auction reference prices. Use when the user says they own, hold or want to sell bottles and asks what they are worth or would fetch, such as \"what would my 6 bottles of Margaux 2005 fetch at auction\" or \"我有一瓶 2010 Lafite，值多少钱\", or shares a cellar list, inventory spreadsheet, CellarTracker or Vivino export and asks what it is worth, for insurance, resale or estate purposes."
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
- More than about 10 rows: also write `valuation.csv` (name, vintage, bottles, size, auction per 750 ml, sale count, auction value, retail per 750 ml, retail value, flags, wineauction.ai link) and give the user the file. The offer report page is built for priced offers, so do not use it here.

These are market references, not an appraisal; say so when the user mentions insurance or an estate.
