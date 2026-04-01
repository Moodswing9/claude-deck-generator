"""
healthcheck.py - Project health checker

Verifies that the pptx-generator project is in a good state.

Usage:
    python healthcheck.py
"""

import importlib
import os
import subprocess
import sys


REQUIRED_PACKAGES = ["anthropic", "pptx", "streamlit", "requests"]  # pptx = python-pptx
REQUIRED_FILES = ["generate.py", "app.py", "requirements.txt", "test_generate.py", "CLAUDE.md"]

PASS = "\033[92m PASS\033[0m"
FAIL = "\033[91m FAIL\033[0m"
WARN = "\033[93m WARN\033[0m"


def check(label: str, ok: bool, detail: str = "", warn: bool = False):
    status = WARN if (warn and not ok) else (PASS if ok else FAIL)
    line = f"[{status} ] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def run():
    failures = 0

    print("\n=== pptx-generator health check ===\n")

    # 1. Required files present
    print("-- Files --")
    for f in REQUIRED_FILES:
        ok = check(f"  {f} exists", os.path.isfile(f))
        if not ok:
            failures += 1

    # 2. Dependencies importable
    print("\n-- Dependencies --")
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
            check(f"  {pkg}", True)
        except ImportError as e:
            check(f"  {pkg}", False, str(e))
            failures += 1

    # 3. API key set
    print("\n-- Environment --")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if api_key.startswith("sk-ant-"):
        check("  ANTHROPIC_API_KEY", True, f"{api_key[:12]}...")
    elif api_key:
        check("  ANTHROPIC_API_KEY", False, "set but doesn't look like a valid key")
        failures += 1
    else:
        check("  ANTHROPIC_API_KEY", False, "not set", warn=True)
        failures += 1

    unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if unsplash_key:
        check("  UNSPLASH_ACCESS_KEY", True, f"{unsplash_key[:8]}... (images enabled)")
    else:
        check("  UNSPLASH_ACCESS_KEY", True, "not set (optional — images disabled)", warn=False)

    # 4. Git status
    print("\n-- Git --")
    try:
        result = subprocess.run(
            ["git", "fetch", "--quiet"],
            capture_output=True, text=True
        )
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        )
        uncommitted = [l for l in status.stdout.splitlines() if not l.startswith("??")]
        check("  No uncommitted changes", len(uncommitted) == 0,
              f"{len(uncommitted)} file(s) modified" if uncommitted else "")

        ahead = subprocess.run(
            ["git", "log", "--oneline", "origin/main..main"],
            capture_output=True, text=True
        )
        unpushed = ahead.stdout.strip().splitlines()
        ok = check("  In sync with origin/main", len(unpushed) == 0,
                   f"{len(unpushed)} unpushed commit(s)" if unpushed else "")
        if not ok:
            failures += 1

    except FileNotFoundError:
        check("  Git", False, "git not found in PATH")
        failures += 1

    # 5. Tests
    print("\n-- Tests --")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test_generate.py", "-q", "--tb=no"],
        capture_output=True, text=True
    )
    passed = "passed" in result.stdout
    summary = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr.strip()
    ok = check("  pytest", passed, summary)
    if not ok:
        failures += 1

    # 6. generate.py importable
    print("\n-- App --")
    try:
        import generate  # noqa
        check("  generate.py imports cleanly", True)
    except Exception as e:
        check("  generate.py imports cleanly", False, str(e))
        failures += 1

    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import logging
            logging.disable(logging.CRITICAL)
            import app  # noqa
            logging.disable(logging.NOTSET)
        check("  app.py imports cleanly", True)
    except Exception as e:
        check("  app.py imports cleanly", False, str(e))
        failures += 1

    # Summary
    print(f"\n{'='*36}")
    if failures == 0:
        print("\033[92mAll checks passed.\033[0m")
    else:
        print(f"\033[91m{failures} check(s) failed.\033[0m")
    print()

    return failures


if __name__ == "__main__":
    sys.exit(run())
