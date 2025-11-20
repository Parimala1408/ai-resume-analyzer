import json
from pathlib import Path

RESUME = Path("resume.txt")
KEYS = Path("keywords.txt")
REPORT_JSON = Path("report.json")
REPORT_MD = Path("report.md")

def load_resume():
    if not RESUME.exists():
        raise FileNotFoundError("resume.txt not found")
    return RESUME.read_text(encoding="utf-8")

def load_keywords():
    if not KEYS.exists():
        raise FileNotFoundError("keywords.txt not found")
    return [k.strip() for k in KEYS.read_text().splitlines() if k.strip()]

def analyze(text, keywords):
    found = []
    missing = []
    lower = text.lower()

    for kw in keywords:
        if kw.lower() in lower:
            found.append(kw)
        else:
            missing.append(kw)

    score = round((len(found) / len(keywords)) * 100, 2)

    return {
        "score": score,
        "found": found,
        "missing": missing
    }

def save_reports(result):
    REPORT_JSON.write_text(json.dumps(result, indent=2))

    md = (
        f"# Resume Keyword Analysis\n\n"
        f"**Score:** {result['score']}%\n\n"
        f"## ✔ Skills Found ({len(result['found'])})\n"
    )

    for s in result["found"]:
        md += f"- {s}\n"

    md += f"\n## ❌ Skills Missing ({len(result['missing'])})\n"

    for s in result["missing"]:
        md += f"- {s}\n"

    REPORT_MD.write_text(md)

if __name__ == "__main__":
    text = load_resume()
    keywords = load_keywords()
    result = analyze(text, keywords)
    save_reports(result)
    print("Report generated: report.json and report.md")
