#!/usr/bin/env bash
# Build the planted/clean OCR qualification fixture repository at $1.
set -euo pipefail
dir="$1"; src="$(cd "$(dirname "$0")/../fixtures" && pwd)"
rm -rf "$dir"; mkdir -p "$dir/src"; cd "$dir"
git init -q -b main
git config user.email fixture@localhost; git config user.name fixture; git config commit.gpgsign false
cp "$src/base.ts" src/receipt-store.ts; git add -A; git commit -qm "base: receipt store"
git checkout -qb change-a; cp "$src/planted.ts" src/receipt-store.ts; git commit -qam "feat: bounded receipt store helpers"
git checkout -q main; git checkout -qb change-b; cp "$src/clean.ts" src/receipt-store.ts; git commit -qam "feat: bounded receipt store helpers"
git checkout -q main
