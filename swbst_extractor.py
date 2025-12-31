import json

INPUT_FILE = "triage_scan_output.json"
OUTPUT_FILE = "swbst_candidates.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

stories = []

for artifact in data["artifacts"]:
    stories.append({
        "Somebody": "KenPire system",
        "Wanted": f"to manage or preserve {artifact['path']}",
        "But": "system drift and manual edits introduce risk",
        "So": "the artifact must be classified and understood",
        "Then": "it can be refined, deprecated, or operationalized",
        "source_artifact": artifact["path"],
        "last_modified": artifact["last_modified"]
    })

with open(OUTPUT_FILE, "w") as f:
    json.dump({"swbst": stories}, f, indent=2)

print(f"SWBST extraction complete. Output written to {OUTPUT_FILE}")
