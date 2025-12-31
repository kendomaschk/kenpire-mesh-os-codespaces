import os
import json
from datetime import datetime

# Root directory of the repo
REPO_ROOT = "."

# File extensions of interest
EXTENSIONS = [".py", ".json", ".sh", ".md"]

# Directories to ignore
IGNORE_DIRS = {".git", "__pycache__", "venv", "env", "node_modules", "dist", "build"}

# Function to walk the repo and collect file metadata
def scan_repo():
    artifact_list = []

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                full_path = os.path.join(root, file)
                stat = os.stat(full_path)

                artifact_list.append({
                    "path": os.path.relpath(full_path, REPO_ROOT),
                    "size_bytes": stat.st_size,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

    return artifact_list

# Write output to JSON
def write_manifest(artifacts, output_file="triage_scan_output.json"):
    with open(output_file, "w") as f:
        json.dump({"artifacts": artifacts}, f, indent=2)

if __name__ == "__main__":
    artifacts = scan_repo()
    write_manifest(artifacts)
    print(f"Triage scan complete. {len(artifacts)} artifacts written to triage_scan_output.json")
