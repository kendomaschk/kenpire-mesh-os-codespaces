import json
from collections import defaultdict
from datetime import datetime

INPUT_FILE = "triage_scan_output.json"
OUTPUT_FILE = "triage_heatmap.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

heatmap = defaultdict(int)

for artifact in data["artifacts"]:
    date = artifact["last_modified"].split("T")[0]
    heatmap[date] += 1

heatmap_out = [
    {"date": date, "artifact_count": count}
    for date, count in sorted(heatmap.items())
]

with open(OUTPUT_FILE, "w") as f:
    json.dump({"heatmap": heatmap_out}, f, indent=2)

print(f"Heat map generated: {OUTPUT_FILE}")
