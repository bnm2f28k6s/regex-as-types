#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
# Build the pinned release natively; no global Cargo installation or Rosetta needed.
command -v nix >/dev/null
command -v git >/dev/null
mkdir -p .cache bin
src="$(mktemp -d "$PWD/.cache/docgen-source.XXXXXX")"
trap 'rm -rf "$src"' EXIT HUP INT TERM
git clone --depth 1 --branch 0.3.3 https://github.com/thecodrr/docgen.git "$src"
test "$(git -C "$src" rev-parse HEAD)" = b2d0cfc77110b524f5e5ab547bd8eb5b1dbd28fb
nix shell github:NixOS/nixpkgs/7a0f122f5090cf4c2ade2a13a0e229d4e19ba71f#cargo github:NixOS/nixpkgs/7a0f122f5090cf4c2ade2a13a0e229d4e19ba71f#rustc --command cargo build --release --locked --manifest-path "$src/Cargo.toml"
"$src/target/release/docgen" --version
cp "$src/target/release/docgen" bin/docgen
./bin/docgen --version
