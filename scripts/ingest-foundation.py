from pathlib import Path
import json
import re
import subprocess

PDF = Path("foundation/source/Script 3.pdf")
OUT = Path("foundation/extracted")
MANIFEST = Path("foundation/manifests")

OUT.mkdir(parents=True, exist_ok=True)
MANIFEST.mkdir(parents=True, exist_ok=True)

text_file = OUT / "Script (3).txt"

subprocess.run(
    [
        "pdftotext",
        "-layout",
        str(PDF),
        str(text_file)
    ],
    check=True
)

text = text_file.read_text(
    encoding="utf-8",
    errors="replace"
)

# Detect explicit Tab headings.
pattern = re.compile(
    r"(?im)^\s*Tab\s+(\d+)\s*$"
)

matches = list(pattern.finditer(text))

tabs = []

for index, match in enumerate(matches):

    number = int(match.group(1))

    start = match.end()

    end = (
        matches[index + 1].start()
        if index + 1 < len(matches)
        else len(text)
    )

    content = text[start:end].strip()

    filename = OUT / f"tab-{number:03d}.txt"

    filename.write_text(
        content,
        encoding="utf-8"
    )

    tabs.append({
        "tab": number,
        "source": str(filename),
        "characters": len(content),
        "status": "INGESTED",
        "execution": "NOT_YET_CLASSIFIED"
    })

manifest = {
    "foundation": "Script 3.pdf",
    "sourcePages": 242,
    "tabsDetected": len(tabs),
    "tabs": tabs
}

(MANIFEST / "foundation-tabs.json").write_text(
    json.dumps(
        manifest,
        indent=2
    ) + "\n",
    encoding="utf-8"
)

print(
    f"Foundation ingested: {len(tabs)} tabs detected."
)

for tab in tabs:
    print(
        f"TAB {tab['tab']:03d} | "
        f"{tab['status']} | "
        f"{tab['characters']} characters"
    )
