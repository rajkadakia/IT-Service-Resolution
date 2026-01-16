import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  
DATASET_DIR = BASE_DIR / "networkdataset"

def load_all_incidents():
    incidents = []

    for file in DATASET_DIR.glob("*.json"):
        if file.name == "schema.json":
            continue

        with open(file, "r", encoding="utf-8") as f:
            incidents.extend(json.load(f))

        if len(incidents) > 500:
            raise RuntimeError("Too many incidents — split categories")

    return incidents



def create_chunks(incident):
    problem_chunk = {
        "incident_id": incident["incident_id"],
        "category": incident["category"],
        "chunk_type": "problem",
        "text": f"""
Title: {incident['title']}
Symptoms: {', '.join(incident['symptoms'])}
Errors: {', '.join(incident['errors'])}
Root cause: {incident['root_cause']}
Severity: {incident['severity']}
Environment: {incident['environment']}
""".strip()
    }

    resolution_chunk = {
        "incident_id": incident["incident_id"],
        "category": incident["category"],
        "chunk_type": "resolution",
        "text": f"""
Resolution steps:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(incident['resolution_steps']))}

Validation steps:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(incident['validation_steps']))}

Tools: {', '.join(incident['tools'])}
""".strip()
    }

    return problem_chunk, resolution_chunk

def get_all_chunks():
    incidents = load_all_incidents()
    chunks = []

    for incident in incidents:
        problem_chunk, resolution_chunk = create_chunks(incident)
        chunks.append(problem_chunk)
        chunks.append(resolution_chunk)

    return chunks



def main():
    incidents = load_all_incidents()

    for incident in incidents:
        problem, resolution = create_chunks(incident)
        print("=" * 80)
        print(problem)
        print("-" * 80)
        print(resolution)

if __name__ == "__main__":
    main()
