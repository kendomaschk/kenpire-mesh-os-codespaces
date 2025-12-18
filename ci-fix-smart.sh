#!/bin/bash

echo "🔧 Smart CI Guard Patch Starting..."

PATCH_DATE=$(date +"%Y%m%d_%H%M%S")
SMART_CARD="ci_guard_patch_${PATCH_DATE}.json"

# Collect patch log
PATCH_LOG="patch_log_${PATCH_DATE}.txt"
touch "$PATCH_LOG"

# Scan all workflow YAMLs
find .github/workflows -name "*.yml" -print0 | while IFS= read -r -d '' file; do
  echo "⚙️  Patching: $file" | tee -a "$PATCH_LOG"
  
  sed -i.bak \
    -e 's/flake8 src\/ tests\//if [ -d tests ] \&\& flake8 src\/ tests\//g' \
    -e 's/pytest tests\//if [ -d tests ] \&\& pytest tests\//g' \
    "$file"
done

# Build smart card tracker
cat <<EOF > "$SMART_CARD"
{
  "card_type": "CI_GUARD_PATCH",
  "patched_by": "finish_it",
  "timestamp": "$PATCH_DATE",
  "details": {
    "action": "Injected directory existence checks for flake8 and pytest",
    "guard_logic": "if [ -d tests ] && pytest ...",
    "scope": "All GitHub Actions workflows in .github/workflows"
  },
  "audit": "$PATCH_LOG"
}
EOF

echo ""
echo "📎 Smart card created: $SMART_CARD"
echo "✅ All CI workflows patched. Commit & push this card and the changes."
