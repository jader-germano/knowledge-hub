#!/bin/bash
set -euo pipefail

# Session Start Hook for Knowledge Hub
# This is a documentation-only project with no build dependencies

echo '{"async": false}'

# Verify git is available
if ! command -v git &> /dev/null; then
  echo "Warning: git is not available"
  exit 1
fi

# All dependencies are already available in this documentation project
echo "✅ Session environment ready for Knowledge Hub"
exit 0
