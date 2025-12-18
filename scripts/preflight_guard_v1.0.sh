#!/usr/bin/env bash
set -e

echo "🛡️ Running preflight guard v1.0..."

# 1. Shell check
if [[ "$OSTYPE" != msys* ]]; then
  echo "❌ ERROR: Not running in MSYS shell"
  exit 1
fi

# 2. Python path check
PY=$(command -v python3 || true)
if [[ "$PY" != "/usr/bin/python3" ]]; then
  echo "❌ ERROR: python3 not resolving to /usr/bin/python3"
  exit 1
fi

# 3. Python version check
VERSION=$(python3 --version 2>&1)
if [[ "$VERSION" != "Python 3.12.12" ]]; then
  echo "❌ ERROR: Python version mismatch. Expected 3.12.12, got $VERSION"
  exit 1
fi

# 4. Runtime assertion presence
ASSERT_PATH="docs/audit/runtime_assertions.json"
if [[ ! -f "$ASSERT_PATH" ]]; then
  echo "❌ ERROR: Runtime assertion file missing: $ASSERT_PATH"
  exit 1
fi

# 5. Authority map enforcement
AUTH_CARD_PATH="docs/control/smartcards/smartcard_authority_map_v1.0.json"
if [[ ! -f "$AUTH_CARD_PATH" ]]; then
  echo "❌ ERROR: SmartCard authority map missing: $AUTH_CARD_PATH"
  exit 1
fi

if ! grep -q "\"kenpire-mesh-os-codespaces\"" "$AUTH_CARD_PATH"; then
  echo "❌ ERROR: Authority map does not declare correct source_of_truth"
  exit 1
fi

echo "✅ Preflight guard passed — mesh may proceed."
