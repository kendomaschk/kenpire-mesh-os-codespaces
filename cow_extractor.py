import json

INPUT_FILE = "triage_scan_output.json"
OUTPUT_FILE = "cow_candidates.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

cow_entries = []

for artifact in data["artifacts"]:
    cow_entries.append({
        "Connections": f"Relates to system scope containing {artifact['path']}",
        "Observations": f"Artifact last modified on {artifact['last_modified']}",
        "Wonderings": "Is this artifact still active, duplicated, or superseded?",
        "source_artifact": artifact["path"]
    })

with open(OUTPUT_FILE, "w") as f:
    json.dump({"cow": cow_entries}, f, indent=2)

print(f"COW extraction complete. Output written to {OUTPUT_FILE}")
