#!/bin/bash
# Example: Daily note-taking workflow

API_URL="http://localhost:8000"
DATE=$(date +%Y-%m-%d)

# Get input from user
read -p "What did you accomplish today? " ACCOMPLISHMENTS
read -p "What are tomorrow's priorities? " PRIORITIES
read -p "Any blockers? " BLOCKERS

# Build content
CONTENT="## Accomplishments
${ACCOMPLISHMENTS}

## Tomorrow's Priorities
${PRIORITIES}

## Blockers
${BLOCKERS}"

# Save to knowledge base
curl -X POST "${API_URL}/artifact/save" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Daily Notes - ${DATE}\",
    \"content\": $(echo "$CONTENT" | jq -Rs .),
    \"tags\": [\"daily-notes\", \"$(date +%Y)\", \"$(date +%B)\"]
  }"

echo ""
echo "✓ Daily notes saved!"
