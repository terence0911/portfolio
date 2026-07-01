#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
HTML="file://${ROOT}/cv.html"
OUT="${1:-/Users/terenceliu/Downloads/TerenceLiuCV.pdf}"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT" \
  "$HTML"

echo "Wrote $OUT"
