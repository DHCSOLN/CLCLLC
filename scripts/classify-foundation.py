from pathlib import Path
import json
import re

SOURCE = Path("foundation/extracted")
OUTPUT = Path(
    "foundation/manifests/foundation-work.json"
)

records = []

for file in sorted(
    SOURCE.glob("tab-*.txt")
):

    text = file.read_text(
        encoding="utf-8",
        errors="replace"
    )

    classifications = []

    checks = {
        "AWS": [
            "AWS::",
            "CloudFormation",
            "CodePipeline",
            "CodeBuild",
            "Lambda",
            "API Gateway",
            "IAM",
            "StackSet"
        ],

        "GITHUB": [
            "GitHub",
            ".github/",
            "workflow",
            "actions/"
        ],

        "JAVA": [
            "pom.xml",
            "mvn ",
            "<artifactId>",
            "<groupId>"
        ],

        "NODE": [
            "node ",
            "npm ",
            "package.json",
            ".mjs",
            ".ts"
        ],

        "DOCKER": [
            "Dockerfile",
            "docker build",
            "FROM "
        ],

        "SHELL": [
            "#!/usr/bin/env bash",
            "aws ",
            "curl ",
            "chmod "
        ],

        "FRONTEND": [
            "<html",
            "frontend/",
            "styles.css",
            "app.js"
        ]
    }

    for category, indicators in checks.items():

        if any(
            indicator.lower() in text.lower()
            for indicator in indicators
        ):
            classifications.append(category)

    command_candidates = []

    for line in text.splitlines():

        stripped = line.strip()

        if re.match(
            r"^(mvn|npm|node|docker|aws|curl|chmod)\s+",
            stripped
        ):
            command_candidates.append(stripped)

    records.append({
        "source": str(file),
        "classifications": classifications,
        "commandCandidates": command_candidates,

        # Critical control:
        # extraction never equals authorization.
        "approvedForExecution": False
    })

OUTPUT.write_text(
    json.dumps(
        {"work": records},
        indent=2
    ) + "\n",
    encoding="utf-8"
)

print(
    f"Classified {len(records)} foundation tabs."
)
