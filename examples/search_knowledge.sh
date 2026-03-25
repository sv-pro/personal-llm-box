#!/bin/bash
# Example: Interactive knowledge search

API_URL="http://localhost:8000"

echo "🔍 Knowledge Base Search"
echo "========================"
echo ""

while true; do
    read -p "Search query (or 'quit'): " QUERY

    if [ "$QUERY" = "quit" ]; then
        break
    fi

    if [ -z "$QUERY" ]; then
        continue
    fi

    # URL-encode the query
    ENCODED_QUERY=$(echo "$QUERY" | jq -sRr @uri)

    # Search
    RESULTS=$(curl -s "${API_URL}/search?q=${ENCODED_QUERY}")

    # Parse and display
    echo ""
    echo "$RESULTS" | jq -r '
        if .results | length > 0 then
            "Found \(.results | length) result(s):\n" +
            (.results[] | "
📄 \(.filename)
   \(.snippet)
")
        else
            "No results found."
        end
    '
    echo ""
done
