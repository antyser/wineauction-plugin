import argparse
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "report.html"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill the WineAuction report template.")
    parser.add_argument("rows", help="JSON file with a list of report rows")
    parser.add_argument("output", help="HTML file to write")
    parser.add_argument("--title", required=True)
    parser.add_argument("--eyebrow", default="WineAuction")
    parser.add_argument("--lede", default="")
    parser.add_argument("--method", default="")
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
    data = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE.read_text()
    for key, value in (
        ("__TITLE__", args.title),
        ("__EYEBROW__", args.eyebrow),
        ("__LEDE__", args.lede),
        ("__METHOD__", args.method),
    ):
        page = page.replace(key, html.escape(value))
    Path(args.output).write_text(page.replace("__DATA__", data))


if __name__ == "__main__":
    main()
