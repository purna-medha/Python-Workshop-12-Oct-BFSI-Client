"""Build independent lab projects; refuse to overwrite an existing destination."""
import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "reference"
START = re.compile(r"^(\s*)# ANSWER (m\d{2}) ([a-z_]+) BEGIN\s*$")
END = re.compile(r"^\s*# ANSWER (m\d{2}) ([a-z_]+) END\s*$")

BASE = {"__init__.py", "calculations.py", "models.py", "catalog.py", "orders.py",
        "cart.py", "memory.py", "runtime.py", "cli.py"}
API = {"api.py", "schemas.py", "server.py", "client.py", "call_api.py"}
SQLITE = {"storage.py", "schema.sql"}

DATACLASS_SCHEMAS = '''# M4: dataclass input; explicit constraints arrive in M5.
from dataclasses import dataclass


@dataclass
class RequestedItem:
    product_id: str
    quantity: int


@dataclass
class OrderRequest:
    items: list[RequestedItem]


@dataclass
class OrderResponse:
    order_id: str
    lines: list[dict]
    total_paise: int
'''


def comment_answers(source, module, suffix):
    lines = source.splitlines()
    result = []
    regions = []
    position = 0
    while position < len(lines):
        line = lines[position]
        match = START.match(line)
        if not match or match.group(2) != module:
            result.append(line)
            position += 1
            continue
        indent, _, name = match.groups()
        regions.append((name, len(result) + 1))
        result.append(line)
        position += 1
        while position < len(lines):
            ending = END.match(lines[position])
            if ending and ending.groups() == (module, name):
                break
            answer_line = lines[position]
            result.append(indent + "# " + answer_line[len(indent):] if answer_line else indent + "#")
            position += 1
        if position == len(lines):
            raise ValueError(f"Unclosed answer: {module} {name}")
        if suffix == ".py":
            fallback = {
                "quantity_contract": "quantity: int",
                "nonempty_contract": "items: list[RequestedItem]",
            }.get(name, f'raise NotImplementedError("{module.upper()}: complete {name}")')
            result.append(indent + fallback + "  # LAB-GUARD: remove when answering")
        result.append(lines[position])
        position += 1
    return "\n".join(result) + "\n", regions


def source_files(module):
    number = int(module[1:])
    if number <= 2:
        return [(ROOT / "day-one" / "shop.py", Path("shop.py"))]
    names = set(BASE)
    if number >= 4:
        names |= API
    if number >= 5:
        names.add("workflow.py")
    if number >= 6:
        names |= SQLITE
    files = [(REFERENCE / "nanozon" / name, Path("nanozon") / name)
             for name in sorted(names)]
    files.append((REFERENCE / "pyproject.toml", Path("pyproject.toml")))
    if number >= 5:
        files.append((REFERENCE / "data" / "orders.csv", Path("data/orders.csv")))
    if number >= 7:
        for name in ["conftest.py", "test_domain.py", "test_contracts.py"]:
            files.append((REFERENCE / "tests" / name, Path("tests") / name))
    if number >= 8:
        for name in ["test_integration.py", "test_client.py"]:
            files.append((REFERENCE / "tests" / name, Path("tests") / name))
    if number >= 9:
        files.extend([(REFERENCE / "tests/test_quality.py", Path("tests/test_quality.py")),
                      (REFERENCE / "ci/nano-zon.yml", Path("ci/nano-zon.yml"))])
    return files


def build(module, destination):
    if destination.exists():
        raise FileExistsError(f"Keep existing work: destination already exists: {destination}")
    sources = source_files(module)
    prepared = []
    locations = []
    for source_path, relative in sources:
        source = source_path.read_text(encoding="utf-8")
        if relative == Path("nanozon/runtime.py"):
            if int(module[1:]) <= 5:
                source = ('# Supplied checkpoint storage; SQLite arrives in M6.\n'
                          'from .memory import MemoryStore\n\n\n'
                          'def open_store():\n    return MemoryStore()\n')
            elif module == "m06":
                source = source.replace('"NANOZON_STORAGE", "sqlite"', '"NANOZON_STORAGE", "memory"')
        if relative == Path("nanozon/schemas.py") and module == "m04":
            source = DATACLASS_SCHEMAS
        if relative == Path("nanozon/client.py") and module == "m04":
            # M4 decodes JSON; explicit response validation is introduced in M5.
            source = source.replace("from pydantic import TypeAdapter\n", "")
            source = source.replace("from .schemas import OrderResponse, ProductResponse\n", "")
            source = source.replace("list[ProductResponse]", "list[dict]")
            source = source.replace("-> OrderResponse", "-> dict")
            source = source.replace("TypeAdapter(list[dict]).validate_python(response.json())",
                                    "response.json()")
            source = source.replace("OrderResponse.model_validate(response.json())", "response.json()")
        if relative == Path("nanozon/call_api.py") and module == "m04":
            source = source.replace("order.total_paise", 'order["total_paise"]')
            source = source.replace("order.order_id", 'order["order_id"]')
        source, regions = comment_answers(source, module, relative.suffix)
        prepared.append((relative, source))
        locations.extend((relative, line, name) for name, line in regions)
    destination.mkdir(parents=True)
    for relative, source in prepared:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source, encoding="utf-8")
    tools = destination / "tools"
    tools.mkdir()
    shutil.copyfile(ROOT / "tools/progress.py", tools / "progress.py")
    shutil.copyfile(REFERENCE / ".gitignore", destination / ".gitignore")
    map_lines = [f"# {module.upper()} — answer locations", "",
                 "Complete the commented answer inside each marker pair. Remove its LAB-GUARD line.", "",
                 "| File | Region |", "|---|---|"]
    for relative, line, name in locations:
        map_lines.append(f"| [{relative}:{line}]({relative.as_posix()}) | `{name}` |")
    map_lines += ["", "Check pending locations: `python tools/progress.py`.",
                  "This reports incomplete regions; it does not establish that your answer is correct."]
    (destination / "ANSWER-MAP.md").write_text("\n".join(map_lines) + "\n", encoding="utf-8")
    readme = [f"# Nano-Zon — {module.upper()} starter", "",
              "This checkpoint supplies the preceding modules. Only this lab's answer regions are disabled.", "",
              "See [ANSWER-MAP.md](ANSWER-MAP.md) for exact locations and the parent lab guide for tasks.", "",
              "Read the commented answer, write or uncomment it, and remove the LAB-GUARD line.",
              "Declaration guards are temporary unconstrained fields; function guards raise a readable pending error.", "",
              "Start the shop: `python shop.py`." if int(module[1:]) <= 2 else
              "Start the shop: `python -m nanozon.cli`."]
    if int(module[1:]) <= 3:
        readme += ["", "This checkpoint's shop uses only the Python standard library."]
    if 3 <= int(module[1:]) <= 6:
        readme += ["", "Memory storage keeps earlier shopping behavior available."]
    if module == "m06":
        readme += ["After completing storage, set `NANOZON_STORAGE=sqlite` to enable persistence."]
    if int(module[1:]) >= 4:
        readme += ["", "Install dependencies: `uv sync`.",
                   "Run API: `uv run uvicorn nanozon.server:app --port 8000`."]
    if int(module[1:]) >= 7:
        readme += ["", "Install testing dependencies: `uv sync --extra dev`.",
                   "Run tests: `uv run --extra dev pytest -q`."]
    (destination / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(f"{module}: {len(locations)} answer regions -> {destination}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lab", choices=[f"m{n:02d}" for n in range(1, 10)])
    parser.add_argument("--output", type=Path, help="New destination for a single lab")
    args = parser.parse_args()
    if args.output and not args.lab:
        parser.error("--output requires --lab")
    modules = [args.lab] if args.lab else [f"m{n:02d}" for n in range(1, 10)]
    destinations = [(module, args.output if args.output else ROOT / "labs" / module / "starter")
                    for module in modules]
    for _, destination in destinations:
        if destination.exists():
            parser.error(f"Destination exists; use --lab and a new --output: {destination}")
    for module, destination in destinations:
        build(module, destination)


if __name__ == "__main__":
    main()
