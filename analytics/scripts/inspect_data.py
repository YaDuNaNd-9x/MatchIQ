
import json
from pathlib import Path

DATA_DIR = Path("data/raw/football_json")

files = sorted(DATA_DIR.glob("epl_*.json"))

print("=" * 60)
print("MATCHIQ - RAW FOOTBALL DATA INSPECTION")
print("=" * 60)

total_matches = 0

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    matches = data.get("matches", [])

    total_matches += len(matches)

    print(f"\nSeason: {data.get('name')}")
    print(f"File: {file.name}")
    print(f"Matches: {len(matches)}")

    if matches:
        print("Available columns:", list(matches[0].keys()))
        print("Sample match:")
        print(json.dumps(matches[0], indent=4))

print("\n" + "=" * 60)
print("TOTAL MATCHES:", total_matches)
print("=" * 60)
