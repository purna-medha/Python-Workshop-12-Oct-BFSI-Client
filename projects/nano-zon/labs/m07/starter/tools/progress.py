"""List incomplete answer regions without executing application code or tests."""
import argparse
from pathlib import Path
import re

START = re.compile(r"^\s*# ANSWER (m\d{2}) ([a-z_]+) BEGIN\s*$")
END = re.compile(r"^\s*# ANSWER (m\d{2}) ([a-z_]+) END\s*$")


def pending_answers(project_root):
    pending = []
    for path in sorted(project_root.rglob("*")):
        if path.suffix not in {".py", ".toml", ".yml"}:
            continue
        if any(part in {".venv", "__pycache__", ".git"} for part in path.parts):
            continue
        current = None
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = START.match(line)
            if match:
                current = (match.groups(), number, [])
            elif END.match(line) and current:
                identity, beginning, contents = current
                statements = [text.strip() for text in contents if text.strip()]
                disabled = any("# LAB-GUARD" in text for text in statements)
                disabled = disabled or all(text.startswith("#") for text in statements)
                if disabled:
                    pending.append((path.relative_to(project_root), beginning, *identity))
                current = None
            elif current:
                current[2].append(line)
    return pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-complete", action="store_true")
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    pending = pending_answers(root)
    for path, line, module, name in pending:
        print(f"{module} {name}: {path}:{line}")
    print(f"{len(pending)} pending answer region(s)")
    return 1 if arguments.require_complete and pending else 0


if __name__ == "__main__":
    raise SystemExit(main())
