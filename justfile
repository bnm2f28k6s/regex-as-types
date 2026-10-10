# List available tasks.
default:
    @just --list

# Start the live-reloading preview at http://127.0.0.1:4001.
serve:
    ./bin/docgen serve

# Build the production site into site/.
build:
    ./bin/docgen build --release

# Build and verify that the binary and generated site are Git-ignored.
check: build
    git check-ignore bin/docgen site/index.html
