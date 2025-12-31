import json
from collections import defaultdict
from datetime import datetime

INPUT_FILE = "triage_scan_output.json"
OUTPUT_FILE = "triage_by_date.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

groups = defaultdict(list)

for artifact in data["artifacts"]:
    date_only = artifact["last_modified"].split("T")[0]
    groups[date_only].append(artifact["path"])

output = {
    "grouped_by_date": dict(sorted(groups.items()))
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=2)

print(f"Date clustering complete. Output written to {OUTPUT_FILE}")
