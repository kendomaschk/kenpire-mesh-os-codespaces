import json

INPUT_FILE = "triage_scan_output.json"
OUTPUT_FILE = "swbst_candidates.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

stories = []

for artifact in data["artifacts"]:
    stories.append({
        "source_artifact": artifact["path"],
        "Somebody": "System maintainer",
        "Wanted": "to understand the purpose of this artifact",
        "But": "context and intent were not explicitly documented",
        "So": "the artifact requires narrative refinement",
        "Then": "a KEEP / REFACTOR / ARCHIVE decision can be made"
    })

with open(OUTPUT_FILE, "w") as f:
    json.dump({"stories": stories}, f, indent=2)

print(f"SWBST candidates generated: {OUTPUT_FILE}")
