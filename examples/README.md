# Usage Examples

This directory contains practical examples of how to work with your personal knowledge base.

## Quick Examples

### 1. Daily Note Taking
```bash
./examples/save_daily_notes.sh
```
Interactive script that prompts for daily accomplishments, priorities, and blockers.

### 2. Meeting Analysis
```bash
# Analyze a meeting transcript
./examples/analyze_meeting.py meeting.txt
```
Reads transcript, uses LLM to extract summary/signals/actions, saves structured notes.

### 3. Interactive Search
```bash
./examples/search_knowledge.sh
```
Interactive search prompt - keep searching until you quit.

### 4. Web Article Clipper
```bash
./examples/web_clipper.sh https://example.com/article
```
Fetches web page, converts to text, saves to knowledge base.

**Requires:** `html2text` - install with `sudo apt-get install html2text`

---

## Common Workflows

### Capture thoughts quickly
```bash
echo "My random idea about X" | \
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d @- | jq .
```

### Save code snippets
```bash
curl -X POST http://localhost:8000/artifact/save \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python async example",
    "content": "```python\nasync def fetch(): ...\n```",
    "tags": ["code", "python", "async"]
  }'
```

### Weekly review
```bash
# Find all notes from this week
cd knowledge
git log --since="1 week ago" --oneline

# Search by tag pattern
grep -l "tags.*weekly" *.md
```

### Export knowledge
```bash
# Combine all files
cat knowledge/*.md > my-knowledge-export.md

# Or create a git bundle
cd knowledge
git bundle create ../knowledge-backup.bundle --all
```

---

## Python API Client Example

```python
import requests

class KnowledgeBase:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def save(self, title, content, tags):
        """Save an artifact"""
        response = requests.post(
            f"{self.base_url}/artifact/save",
            json={"title": title, "content": content, "tags": tags}
        )
        return response.json()

    def search(self, query):
        """Search knowledge base"""
        response = requests.get(
            f"{self.base_url}/search",
            params={"q": query}
        )
        return response.json()

    def digest(self, text):
        """Get LLM analysis"""
        response = requests.post(
            f"{self.base_url}/digest",
            json={"text": text}
        )
        return response.json()

# Usage
kb = KnowledgeBase()
kb.save("My Note", "Content here", ["tag1", "tag2"])
results = kb.search("important")
analysis = kb.digest("Long text to analyze...")
```

---

## Automation Ideas

### 1. Email to Knowledge Base
```bash
# In a cron job or email filter
cat email.txt | python analyze_meeting.py -
```

### 2. Periodic Digests
```bash
# Weekly digest of all new notes
cd knowledge
git log --since="1 week ago" --format="%H" | \
while read commit; do
    git show $commit:*.md 2>/dev/null
done | curl -X POST http://localhost:8000/digest ...
```

### 3. Browser Bookmarklet
Create a bookmarklet that sends current page to your knowledge base:
```javascript
javascript:(function(){
  fetch('http://localhost:8000/ingest', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      text: 'Title: ' + document.title + '\nURL: ' + location.href + '\n\n' + document.body.innerText
    })
  }).then(() => alert('Saved!'));
})();
```

### 4. Slack Integration
```python
# In your Slack bot
from slack_sdk import WebClient

@app.event("message")
def handle_message(event):
    if event.get("text", "").startswith("!save"):
        content = event["text"][6:]  # Remove "!save "
        kb.save(f"Slack: {event['user']}", content, ["slack"])
```

---

## Tips

**Tagging Strategy:**
- Use consistent tags: `meetings`, `ideas`, `code`, `research`
- Add time tags: `2026`, `2026-q1`, `march`
- Add project tags: `project-x`, `client-y`

**Search Tips:**
- Search is case-insensitive
- Searches titles, tags, and content
- Use specific terms for better results

**Git Workflow:**
- Every save auto-commits
- Use `git log` in `knowledge/` to see history
- Restore old versions with `git checkout <commit> <file>`

**Performance:**
- Search is fast (full-text grep)
- Digest takes ~5-10s (LLM processing)
- Consider batching digest operations

---

## Advanced: Build a TUI

Want a terminal UI? Try building with Python's `rich` or `textual`:

```python
from textual.app import App
from textual.widgets import Input, TextArea

class KnowledgeApp(App):
    def on_mount(self):
        self.search_input = Input(placeholder="Search...")
        # ... build your TUI
```

---

## Integration Examples

### VSCode Extension
Create a VSCode extension that:
- Saves selected text with Ctrl+Shift+K
- Searches knowledge base from command palette
- Shows results in sidebar

### Alfred/Raycast Workflow
Create a workflow that:
- Quick-saves clipboard content
- Searches knowledge with hotkey
- Shows recent notes

### Mobile App
Build a simple mobile app that:
- Uses the REST API
- Syncs via git (clone/pull/push)
- Offline-first with local SQLite cache

---

## Need More Examples?

Check the main documentation:
- `README.md` - Full API reference
- `docs/quickstart.md` - Getting started guide
- `docs/verification-plan.md` - All endpoint examples

Or explore the `app/routes/` directory to see what each endpoint does.
