#!/bin/bash
# Stamps sw.js with a version so installed apps pick up the new build.
cd "$(dirname "$0")/.."
v=$(date -u +%Y%m%d-%H%M%S)
sed -i '' "s/^const VERSION = \"[^\"]*\";/const VERSION = \"$v\";/" sw.js
echo "sw.js version $v"
