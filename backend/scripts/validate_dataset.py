import json
from pathlib import Path
import sys

DATASET_DIR = Path("networkdataset")

REQUIRED_FIELDS = {
    "incident_id": str,
    "category": str,
    "title": str,
    "symptoms": list,
    "errors": list,
    "root_cause": str,
    "resolution_steps": list,
    "validation_steps": list,
    "tools": list,
    "severity": str,
    "environment": str
}


def fail(msg):
    print(f"[DATASET VALIDATION FAILED] {msg}")
    sys.exit(1)


def validate_file(file_path, seen_ids):
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"{file_path.name}: invalid JSON ({e})")

    if not isinstance(data, list) or len(data) == 0:
        fail(f"{file_path.name}: must be a non-empty list")

    for i, incident in enumerate(data):
        if not isinstance(incident, dict):
            fail(f"{file_path.name}[{i}]: incident must be an object")

        for field, field_type in REQUIRED_FIELDS.items():
            if field not in incident:
                fail(f"{file_path.name}[{i}]: missing field '{field}'")

            if not isinstance(incident[field], field_type):
                fail(
                    f"{file_path.name}[{i}]: field '{field}' must be {field_type.__name__}"
                )

            if field_type == list and len(incident[field]) == 0:
                fail(f"{file_path.name}[{i}]: field '{field}' cannot be empty")

        incident_id = incident["incident_id"]
        if incident_id in seen_ids:
            fail(f"Duplicate incident_id detected: {incident_id}")

        seen_ids.add(incident_id)


def main():
    if not DATASET_DIR.exists():
        fail("networkdataset directory not found")

    json_files = [
        f for f in DATASET_DIR.glob("*.json")
        if f.name != "schema.json"
    ]

    if not json_files:
        fail("No dataset files found")

    seen_ids = set()

    for file in json_files:
        validate_file(file, seen_ids)

    print(f"[OK] Dataset validation passed ({len(seen_ids)} incidents)")


if __name__ == "__main__":
    main()
