# 🎨 Web UI Guide

## Access Your Knowledge Base

**Web Interface:** http://localhost:8000/web/

The web UI provides a modern, intuitive interface for all knowledge base operations.

---

## Features

### 🔍 **Search Tab**
- Full-text search across all your knowledge
- Instant results with highlighted snippets
- Shows filename and matching content

**How to use:**
1. Type your search query
2. Press Enter or click Search
3. Click on results to see details

### 💾 **Save Artifact Tab**
- Create structured documents
- Add title, content, and tags
- Automatic YAML frontmatter
- Git auto-commit

**How to use:**
1. Enter a descriptive title
2. Write your content (markdown supported)
3. Add tags by typing and pressing Enter
4. Click "Save Artifact"
5. File is saved to `knowledge/` directory

**Example use cases:**
- Meeting notes
- Project documentation
- Research findings
- Personal journal entries

### 📥 **Ingest Text Tab**
- Import long-form content
- Automatic paragraph chunking
- Perfect for articles and emails

**How to use:**
1. Paste your text
2. Click "Ingest"
3. Text is auto-chunked by paragraphs
4. Saved with timestamp and "ingested" tag

**Example use cases:**
- Save web articles
- Archive important emails
- Import documentation
- Store chat transcripts

### 🤖 **AI Digest Tab**
- LLM-powered text analysis
- Get summary, signals, and actions
- Processing takes 5-10 seconds

**How to use:**
1. Paste text to analyze
2. Click "Analyze with AI"
3. Wait for LLM processing
4. Review structured output

**You get:**
- **Summary:** 2-3 sentence overview
- **Key Signals:** Important points extracted
- **Action Items:** What to do next

**Example use cases:**
- Summarize long documents
- Extract action items from meetings
- Understand complex articles quickly
- Identify key takeaways

---

## Quick Tips

**Search:**
- Search is case-insensitive
- Searches titles, tags, and content
- Use specific terms for better results

**Tags:**
- Use consistent naming (lowercase, hyphens)
- Add time tags: `2026`, `q1`, `march`
- Add project tags: `project-x`, `client-name`
- Add type tags: `meeting`, `idea`, `code`

**Content:**
- Markdown is supported
- Use headings (#, ##, ###)
- Use lists (- or 1.)
- Code blocks with triple backticks

**Performance:**
- Search is instant
- Save/Ingest takes <1 second
- Digest takes 5-10 seconds (LLM processing)

---

## Status Indicator

Top-right corner shows API connection status:
- **🟢 API Online** - Everything working
- **🔴 API Offline** - Check if backend is running

If offline:
```bash
docker-compose ps
docker-compose restart backend
```

---

## Example Workflow

### Daily Note-Taking
1. Go to **Save Artifact**
2. Title: "Daily Notes - 2026-03-25"
3. Content:
   ```
   ## Accomplishments
   - Completed feature X
   - Fixed bug Y

   ## Tomorrow
   - Review PR
   - Meeting at 10am
   ```
4. Tags: `daily-notes`, `2026`, `march`
5. Save ✅

### Research & Analysis
1. Find an interesting article online
2. Copy the text
3. Go to **Ingest Text**
4. Paste and click Ingest
5. Go to **AI Digest**
6. Paste same text
7. Get instant summary and action items

### Meeting Follow-up
1. After a meeting, paste transcript
2. Use **AI Digest** to extract:
   - What was discussed (summary)
   - Key decisions (signals)
   - What to do next (actions)
3. Copy the analysis
4. Go to **Save Artifact**
5. Create structured meeting notes
6. Tag with `meetings`, `team`, `2026-q1`

---

## Keyboard Shortcuts

- **Enter** in search → Search
- **Enter** when adding tag → Add tag
- **Tab** → Navigate between fields
- **Ctrl+S** in forms → Submit (browser default)

---

## Browser Compatibility

✅ Chrome/Edge (recommended)
✅ Firefox
✅ Safari
✅ Brave
✅ Any modern browser

---

## Mobile Access

The UI is responsive and works on mobile devices:
- Same URL: http://localhost:8000/web/
- Requires backend to be accessible on your network
- Consider using tailscale/cloudflare tunnel for remote access

---

## Customization

### Change Colors
Edit `web-ui/index.html` and modify CSS variables:
```css
:root {
    --primary: #2563eb;      /* Change to your color */
    --success: #10b981;
    --danger: #ef4444;
}
```

### Change API URL
If backend runs on different port/host:
```javascript
const API_BASE = 'http://your-host:8000';
```

---

## Troubleshooting

**Web UI doesn't load:**
- Check backend is running: `docker-compose ps`
- Restart: `docker-compose restart backend`
- Check logs: `docker-compose logs backend`

**"API Offline" message:**
- Backend might not be running
- Check: `curl http://localhost:8000/health`
- Should return: `{"status":"ok"}`

**Search returns nothing:**
- Make sure you've saved some content first
- Try broader search terms
- Check `knowledge/` has .md files

**Digest is very slow:**
- Normal for LLM processing (5-10s)
- CPU mode is slower than GPU
- Longer text takes more time

**Can't add tags:**
- Press Enter after typing tag name
- Don't click outside the input
- Tags appear as blue pills

---

## Next Steps

1. **Save your first artifact**
   - Go to Save Artifact tab
   - Create a test document
   - Add some tags

2. **Try AI Digest**
   - Paste some text
   - Get instant analysis
   - See the power of local LLM

3. **Search your knowledge**
   - After saving a few items
   - Search for keywords
   - Explore results

4. **Build a workflow**
   - Daily notes
   - Research archiving
   - Meeting summaries

---

## Advanced: Integration

The web UI is just a frontend. You can:

1. **Build mobile app**
   - Use same API endpoints
   - React Native / Flutter
   - Access from anywhere

2. **Create browser extension**
   - Save current page with one click
   - Right-click → Save to Knowledge Base

3. **Automate with scripts**
   - See `examples/` directory
   - Python/Bash scripts
   - Cron jobs for automation

4. **Custom dashboards**
   - Analytics on your knowledge
   - Tag clouds
   - Activity heatmaps

---

## API Documentation

The web UI uses these endpoints:
- `GET /health` - Status check
- `GET /search?q=query` - Search
- `POST /artifact/save` - Save document
- `POST /ingest` - Import text
- `POST /digest` - AI analysis

Full API docs: See `README.md`

---

## Need Help?

- **Documentation:** `README.md`, `QUICKSTART.md`
- **Examples:** `examples/` directory
- **Verification:** `VERIFICATION_PLAN.md`
- **GitHub:** Report issues

---

**Enjoy your personal AI-powered knowledge base! 🚀**
