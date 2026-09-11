r"""Extract autocomplete JSON from sozluk.gov.tr JS bundle.

The autocomplete data is embedded as `const eA=JSON.parse('...')` and
`const SA=JSON.parse(\`...\`)` inside the minified JS bundle. This script
parses both, combines them, deduplicates, and sorts them alphabetically
(Turkish locale).
"""

import json
import sys


def extract_json_var(content, var_name):
    marker = f"const {var_name}=JSON.parse("
    start = content.find(marker)
    if start < 0:
        return None
    
    quote = content[start + len(marker)]
    json_start = start + len(marker) + 1
    
    pos = json_start
    while pos < len(content):
        ch = content[pos]
        if ch == "\\":
            pos += 2
            continue
        if ch == quote:
            break
        pos += 1
        
    raw_str = content[json_start:pos]
    if quote == "'":
        raw_str = raw_str.replace("\\'", "'")
    elif quote == "`":
        raw_str = raw_str.replace("\\`", "`").replace("\\${", "${")
    elif quote == '"':
        raw_str = raw_str.replace('\\"', '"')
        
    return json.loads(raw_str)


# Turkish sorting map
alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
tr_map = {}
for i, char in enumerate(alphabet):
    tr_map[char] = i * 2
    tr_map[char.upper()] = i * 2 + 1
tr_map["I"] = alphabet.index("ı") * 2 + 1
tr_map["İ"] = alphabet.index("i") * 2 + 1

def tr_key(item):
    text = item.get("madde", "")
    key = []
    for c in text:
        if c in tr_map:
            key.append(tr_map[c] + 100)
        else:
            key.append(ord(c))
    return key


def main(js_path, output_path):
    with open(js_path, encoding="utf-8") as f:
        content = f.read()

    eA_data = extract_json_var(content, "eA") or []
    SA_data = extract_json_var(content, "SA") or []
    
    if not eA_data and not SA_data:
        print("::error::Could not find eA or SA variables in JS bundle", file=sys.stderr)
        sys.exit(1)

    all_data = eA_data + SA_data
    
    # Deduplicate by madde
    unique_dict = {}
    for item in all_data:
        unique_dict[item["madde"]] = item
        
    unique_list = list(unique_dict.values())
    unique_list.sort(key=tr_key)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_list, f, ensure_ascii=False)

    print(f"Extracted {len(eA_data)} from eA, {len(SA_data)} from SA.")
    print(f"Total unique entries saved: {len(unique_list)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract-autocomplete.py <js_bundle_path> <output_json_path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
