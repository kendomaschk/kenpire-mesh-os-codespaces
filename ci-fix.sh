#!/bin/bash

echo "Patching GitHub Actions CI guards..."
find .github/workflows -name "*.yml" -print0 | while IFS= read -r -d '' file; do
  sed -i.bak -E 's/flake8 src\/ tests\//if [ -d tests ] \&\& flake8 src\/ tests\//' "$file"
  sed -i.bak -E 's/pytest tests\//if [ -d tests ] \&\& pytest tests\//' "$file"
done

echo "CI guard patch complete."
