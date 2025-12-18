# jepa_enforcer.py add-on
def validate_capsule_features(capsule_name: str, declared_features: list):
    vault_path = Path("src/kenpire/vault/modverse_features.vault.json")
    if not vault_path.exists():
        raise FileNotFoundError("Vault missing.")

    with open(vault_path) as f:
        vault = json.load(f)

    if capsule_name not in vault:
        raise ValueError(f"{capsule_name} not in ModVerse vault.")

    expected = set(vault[capsule_name])
    provided = set(declared_features)

    if expected != provided:
        raise ValueError(f"❌ Feature mismatch for {capsule_name}!\nExpected: {expected}\nGot: {provided}")
    
    print(f"✅ {capsule_name} passed JEPA feature check.")
