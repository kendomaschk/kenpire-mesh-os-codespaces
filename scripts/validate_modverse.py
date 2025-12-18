# validate_modverse.py
import json
import os
from pathlib import Path

MODVERSE_PATH = Path("src/kenpire/vault/modverse_features.vault.json")

if not MODVERSE_PATH.exists():
    print("❌ ModVerse Vault missing.")
    exit(1)

with open(MODVERSE_PATH) as f:
    data = json.load(f)

print(f"✅ ModVerse Vault loaded successfully with {len(data)} entries.")
