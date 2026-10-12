# Repeatable checks need consistent dependencies, inputs, commands, and useful
# failure output. A shared runner makes local execution match the automation.
# Preserve reports even when tests fail; retain the failing exit status.
#
# pyproject.toml supplies discovery/configuration; this runner invokes pytest.

from pathlib import Path
import subprocess
import sys


def main():
    project_root = Path(__file__).resolve().parents[1]
    reports = project_root / "reports"
    reports.mkdir(exist_ok=True)
    command = [
        sys.executable, "-m", "pytest", "m07", "m08", "m09",
        "--cov=m03", "--cov=m05.http_client", "--cov=m06",
        "--cov=m09.pricing", "--cov-branch", "--cov-report=term-missing",
        "--cov-report=xml:reports/coverage.xml",
        "--junitxml=reports/tests.xml",
    ]
    result = subprocess.run(command, cwd=project_root, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
# Run: uv run --extra dev python -m m09.s03_repeatable_checks
# No live server is required. Fixtures and HTTP substitutes control test inputs.
