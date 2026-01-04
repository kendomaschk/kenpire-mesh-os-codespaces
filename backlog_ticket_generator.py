import json
import uuid

INPUT_FILE = "swbst_candidates.json"
OUTPUT_FILE = "example_backlog_tickets.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

tickets = []

for story in data["stories"]:
    ticket = {
        "ticket_id": f"KP-{uuid.uuid4().hex[:6].upper()}",
        "title": f"Refine artifact: {story['source_artifact']}",
        "description": {
            "Somebody": story["Somebody"],
            "Wanted": story["Wanted"],
            "But": story["But"],
            "So": story["So"],
            "Then": story["Then"]
        },
        "acceptance_criteria": [
            "Decision recorded: KEEP / REFACTOR / ARCHIVE",
            "Linked to refined artifacts",
            "Reviewed in Refinement Capsule"
        ],
        "source": "Refinement Capsule",
        "status": "EXAMPLE_ONLY"
    }
    tickets.append(ticket)

with open(OUTPUT_FILE, "w") as f:
    json.dump({"tickets": tickets}, f, indent=2)

print(f"Example backlog tickets generated: {OUTPUT_FILE}")
