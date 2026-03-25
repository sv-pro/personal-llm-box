#!/bin/bash
# Example: Web article clipper
# Requires: curl, html2text (install: apt-get install html2text)

API_URL="http://localhost:8000"

if [ -z "$1" ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

URL="$1"
echo "📰 Clipping article from: $URL"

# Fetch and convert to text
if command -v html2text &> /dev/null; then
    CONTENT=$(curl -s "$URL" | html2text)
else
    echo "⚠️  html2text not found. Using raw HTML."
    CONTENT=$(curl -s "$URL")
fi

# Extract title from first line or use URL
TITLE=$(echo "$CONTENT" | head -1 | sed 's/^[#* ]*//' | cut -c1-60)
if [ -z "$TITLE" ]; then
    TITLE="Web Clip - $(date +%Y-%m-%d)"
fi

# Add source URL to content
FULL_CONTENT="Source: $URL

$CONTENT"

# Save to knowledge base
curl -X POST "${API_URL}/ingest" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": $(echo "$FULL_CONTENT" | jq -Rs .)
  }" | jq .

echo "✅ Article clipped and saved!"
