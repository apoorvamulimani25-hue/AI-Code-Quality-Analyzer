import json
from datetime import datetime


def generate_report(results):
    report = {
        "project": "AI-Assisted Code Quality Analysis",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }

    with open(
        "quality_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4)

    return report