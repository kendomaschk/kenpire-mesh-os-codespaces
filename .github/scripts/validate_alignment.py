import json
import sys
from pathlib import Path

def check_alignment():
    base = Path("docs/control/smartcards")
    alignment = base / "smartcard_gold_repo_alignment_v1.0.json"

    if not alignment.exists():
        print("❌ Missing smartcard_gold_repo_alignment_v1.0.json")
        sys.exit(1)

    try:
        with open(alignment) as f:
            card = json.load(f)
        assert card.get("card_id") == "smartcard_gold_repo_alignment_v1.0"
    except Exception:
        print("❌ Invalid gold repo alignment SmartCard")
        sys.exit(1)

    print("✅ Gold repo alignment verified.")

if __name__ == "__main__":
    check_alignment()
