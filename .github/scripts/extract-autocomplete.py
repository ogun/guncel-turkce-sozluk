r"""Extract autocomplete JSON from sozluk.gov.tr JS bundle.

The autocomplete data is embedded as `const eA=JSON.parse('...')` and
`const SA=JSON.parse(\`...\`)` inside the minified JS bundle. This script
parses both, combines them, deduplicates, and sorts them alphabetically
(Turkish locale).
"""

import json
import sys


def extract_all_madde_arrays(content):
    """Finds all JSON.parse(string_literal) in the JS bundle, parses them, 
    and returns combined data for arrays that contain objects with a 'madde' key.
    """
    marker = "JSON.parse("
    idx = 0
    all_data = []
    
    while True:
        idx = content.find(marker, idx)
        if idx == -1:
            break
            
        quote = content[idx + len(marker)]
        if quote in ("'", "`", '"'):
            start = idx + len(marker) + 1
            pos = start
            while pos < len(content):
                ch = content[pos]
                if ch == "\\":
                    pos += 2
                    continue
                if ch == quote:
                    break
                pos += 1
                
            raw_str = content[start:pos]
            if quote == "'":
                raw_str = raw_str.replace("\\'", "'")
            elif quote == "`":
                raw_str = raw_str.replace("\\`", "`").replace("\\${", "${")
            elif quote == '"':
                raw_str = raw_str.replace('\\"', '"')
            
            try:
                parsed_data = json.loads(raw_str)
                # Check if it's a list of dicts with 'madde'
                if isinstance(parsed_data, list) and len(parsed_data) > 0 and isinstance(parsed_data[0], dict) and "madde" in parsed_data[0]:
                    all_data.extend(parsed_data)
                    print(f"Found and extracted {len(parsed_data)} entries from a JSON.parse call.")
            except json.JSONDecodeError:
                pass
                
        idx += len(marker)
        
    return all_data


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

    all_data = extract_all_madde_arrays(content)
    
    if not all_data:
        print("::error::Could not find any autocomplete JSON arrays in the JS bundle", file=sys.stderr)
        sys.exit(1)

    # Deduplicate by madde
    unique_dict = {}
    for item in all_data:
        unique_dict[item["madde"]] = item
        
    unique_list = list(unique_dict.values())
    unique_list.sort(key=tr_key)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_list, f, ensure_ascii=False)

    print(f"Total unique entries saved: {len(unique_list)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract-autocomplete.py <js_bundle_path> <output_json_path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
