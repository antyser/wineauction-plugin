import argparse
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "report.html"


def first(*values):
    for value in values:
        if value is not None:
            return value
    return None


def normalize(row: dict) -> dict:
    """Fill report keys from a raw evaluate_offers, list_offers or search_wines object.

    Keys already present in the row win. Nested objects are read when the flat key is absent.
    """
    if not isinstance(row, dict):
        return row
    out = dict(row)
    wine = row.get("wine") or {}
    inp = row.get("input") or {}
    retail = row.get("retail") or {}
    auction = row.get("auction") or {}
    unit = row.get("unit_price") or {}
    name = first(row.get("name"), row.get("wine_name"), wine.get("display_name"), row.get("listing_name"), inp.get("raw_wine_name"))
    out["name"] = name if name is not None else "(unnamed)"
    out.setdefault("vintage", first(wine.get("vintage"), inp.get("vintage")))
    out.setdefault("bottles", first(row.get("bottles"), inp.get("quantity")))
    out.setdefault("size_ml", first(row.get("bottle_size_ml"), inp.get("format_ml")))
    out.setdefault("price_usd", first(row.get("price_per_bottle_usd"), unit.get("amount") if isinstance(unit, dict) else None))
    out.setdefault("retail_usd", retail.get("price_usd"))
    out.setdefault("retail_live", retail.get("live_offer_count"))
    out.setdefault("auction_usd", auction.get("price_usd"))
    out.setdefault("auction_sales", auction.get("sale_count"))
    out.setdefault("seller", row.get("seller_name"))
    if not out.get("ref") and row.get("auction_lot_number"):
        out["ref"] = "Lot " + str(row["auction_lot_number"])
    if not out.get("ends_at") and row.get("auction_end_time"):
        out["ends_at"] = row["auction_end_time"]
    if not out.get("wineapp_url"):
        out["wineapp_url"] = first(row.get("wineapp_url"), row.get("wineapp_wine_url"))
    if not out.get("group"):
        out["group"] = first(row.get("appellation"), row.get("region"), wine.get("region"))
    offer_type = first(row.get("offer_type"), inp.get("offer_type"))
    status = row.get("auction_status")
    out.setdefault("quoted_price", first(row.get("price"), inp.get("price")))
    out.setdefault("quoted_currency", first(row.get("currency"), inp.get("currency")))
    out.setdefault("premium_pct", row.get("auction_buyers_premium_pct"))
    if out.get("premium_pct") is None and isinstance(inp.get("buyers_premium"), (int, float)):
        out["premium_pct"] = round(inp["buyers_premium"] * 100, 2)
    out.setdefault("estimate_low", row.get("auction_estimate_low"))
    out.setdefault("estimate_high", row.get("auction_estimate_high"))
    out.setdefault("status", status)
    if status == "sold":
        out.setdefault("sold_at", row.get("auction_end_time"))
    out.setdefault("serving", first(row.get("restaurant_serving"), inp.get("serving_type")))
    out.setdefault("pre_arrival", first(row.get("retail_pre_arrival"), inp.get("is_pre_arrival")))
    if "retail_in_stock" in row:
        out.setdefault("in_stock", row["retail_in_stock"])
    elif "is_out_of_stock" in inp:
        out.setdefault("in_stock", not inp["is_out_of_stock"])
    out.setdefault("mixed_items", row.get("auction_lot_items"))
    if not out.get("price_label"):
        if offer_type == "auction":
            out["price_label"] = {"live": "Current or opening bid", "sold": "Hammer incl. premium"}.get(status)
        elif offer_type == "restaurant":
            out["price_label"] = "List price"
        elif offer_type == "retail" and row.get("price") is not None:
            out["price_label"] = "Price"
        elif inp:
            out["price_label"] = "Quoted price"
    return out


def expand(rows: list) -> list:
    """A search_wines wine becomes one row per best offer, carrying the wine's name and references."""
    out = []
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("best_offers"), list):
            for offer in row["best_offers"]:
                merged = {k: v for k, v in row.items() if k not in ("best_offers", "reviews", "offer_count")}
                merged.update({k: v for k, v in offer.items() if v is not None})
                merged["wineapp_url"] = row.get("wineapp_url") or offer.get("wineapp_url")
                merged["offer_wineapp_url"] = offer.get("wineapp_url")
                out.append(merged)
        else:
            out.append(row)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill the WineAuction report template.")
    parser.add_argument("rows", help="JSON file with a list of report rows")
    parser.add_argument("output", help="HTML file to write")
    parser.add_argument("--title", required=True)
    parser.add_argument("--eyebrow", default="WineAuction")
    parser.add_argument("--lede", default="")
    parser.add_argument("--method", default="")
    parser.add_argument(
        "--not-found",
        help="JSON file with a list of {name, hint} for rows that matched no wine",
    )
    parser.add_argument("--markup", action="store_true", help="show markup over each reference instead of discount")
    parser.add_argument("--skipped", default="", help="one line on what was skipped")
    args = parser.parse_args()
    try:
        rows = json.loads(Path(args.rows).read_text())
    except OSError as error:
        sys.exit(f"Cannot read rows file {args.rows}: {error.strerror}")
    except json.JSONDecodeError as error:
        sys.exit(
            f"Rows file {args.rows} is not valid JSON "
            f"(line {error.lineno}, column {error.colno}: {error.msg}). "
            "It must hold a JSON list of row objects."
        )
    if not isinstance(rows, list):
        sys.exit(f"Rows file {args.rows} must hold a JSON list of row objects.")
    rows = [normalize(row) for row in expand(rows)]
    data = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    not_found = json.loads(Path(args.not_found).read_text()) if args.not_found else []
    not_found_data = json.dumps(not_found, ensure_ascii=False).replace("</", "<\\/")
    skipped_data = json.dumps(args.skipped, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE.read_text()
    for key, value in (
        ("__TITLE__", args.title),
        ("__EYEBROW__", args.eyebrow),
        ("__LEDE__", args.lede),
        ("__METHOD__", args.method),
    ):
        page = page.replace(key, html.escape(value))
    page = page.replace("__MARKUP__", "true" if args.markup else "false")
    page = page.replace("__NOT_FOUND__", not_found_data).replace("__SKIPPED__", skipped_data)
    Path(args.output).write_text(page.replace("__DATA__", data))


if __name__ == "__main__":
    main()
