from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

TEXT_EXTS = {
    ".py", ".c", ".h", ".cpp", ".hpp", ".js", ".ts", ".tsx", ".jsx",
    ".md", ".txt", ".json", ".yml", ".yaml", ".sh", ".html", ".css"
}

COMMENT_PATTERNS = [
    re.compile(r"//.*LEGACY"),
    re.compile(r"/\*[\s\S]*?LEGACY[\s\S]*?\*/"),
    re.compile(r"#.*LEGACY"),
    re.compile(r"<!--[\s\S]*?LEGACY[\s\S]*?-->"),
]

def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS

def has_legacy_word(text: str) -> bool:
    return "legacy" in text

def has_legacy_in_comment(text: str) -> bool:
    return any(p.search(text) for p in COMMENT_PATTERNS)

def main():
    violations = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "node_modules" in path.parts:
            continue
        if path.name == "legacy_caps_audit.py":
            continue
        if not is_text_file(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if has_legacy_word(text) and not has_legacy_in_comment(text):
            violations.append(path.relative_to(ROOT))

    if violations:
        print("Violations found:")
        for v in violations:
            print(v)
        sys.exit(1)

    print("No violations found.")
    sys.exit(0)

if __name__ == "__main__":
    main()