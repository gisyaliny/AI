#!/usr/bin/env python3
"""
Run ghp-import via its Python API (equivalent to: ghp-import -n -p -f _build/html)
"""

import sys

def publish_docs(path: str = "_build/html"):
    try:
        import ghp_import as ghp  # package name uses underscore
    except ImportError:
        raise SystemExit(
            "ghp-import is not installed. Install it with:\n  pip install ghp-import"
        )

    # Some versions expose main() that reads sys.argv; others accept args.
    # We try both for compatibility.
    original_argv = sys.argv[:]
    try:
        sys.argv = ["ghp-import", "-n", "-p", "-f", path]
        try:
            ghp.main()  # most common: parses sys.argv
        except TypeError:
            # Fallback: call with explicit args if this build supports it
            ghp.main(["-n", "-p", "-f", path])
    finally:
        sys.argv = original_argv

if __name__ == "__main__":
    # change the path here if your built docs live elsewhere
    publish_docs("_build/html")
    print("✅ Published with ghp-import (module).")
