# List available tasks.
default:
    @just --list

# Start the live-reloading preview at http://127.0.0.1:4001/regex-as-types/.
serve:
    ./bin/docgen serve

# Build the production site into site/.
build:
    ./bin/docgen build --release

# Test the offline checker and validate installer shell syntax.
test:
    sh -n scripts/install-docgen.sh
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v

# Test, build, and check rendered output, ignores, and unstaged/staged whitespace.
check: test build
    python3 scripts/check-site.py
    git check-ignore bin/docgen site/index.html
    git diff --check
    git diff --cached --check
