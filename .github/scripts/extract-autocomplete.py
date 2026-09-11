"""Extract autocomplete JSON from sozluk.gov.tr JS bundle.

The autocomplete data is embedded as `const eA=JSON.parse('...')` inside
the minified JS bundle. This script parses the JS file, extracts the JSON
string (handling escaped single quotes), and writes it as a standalone JSON
file.
"""

import json
import sys


def extract_autocomplete(js_path, output_path):
    with open(js_path, encoding="utf-8") as f:
        content = f.read()

    marker = "const eA=JSON.parse('"
    start = content.find(marker)
    if start < 0:
        print(
            "::error::Could not find eA variable in JS bundle", file=sys.stderr
        )
        sys.exit(1)

    json_start = start + len(marker)

    # Walk through the single-quoted JS string, skipping escaped characters
    pos = json_start
    while pos < len(content):
        ch = content[pos]
        if ch == "\\":
            pos += 2  # skip escaped character
            continue
        if ch == "'":
            break  # found the closing single quote
        pos += 1

    json_str = content[json_start:pos]

    # Unescape single quotes that were escaped for the JS string literal
    json_str = json_str.replace("\\'", "'")

    data = json.loads(json_str)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"Extracted {len(data)} entries")


if __name__ == "__main__":
    extract_autocomplete(sys.argv[1], sys.argv[2])
