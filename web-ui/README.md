# Web UI for Personal AI Box

A clean, modern web interface for your knowledge base.

## Features

- **🔍 Search** - Full-text search across all your knowledge
- **💾 Save Artifacts** - Create structured documents with tags
- **📥 Ingest Text** - Import long-form content (auto-chunked)
- **🤖 AI Digest** - Get LLM-powered summaries and action items
- **🟢 Live API Status** - Real-time connection monitoring

## Quick Start

### Option 1: Through FastAPI Backend (Recommended)

The web UI is automatically served by the backend:

```bash
# Start the backend
docker-compose up -d backend

# Access the web UI
http://localhost:8000/web
```

### Option 2: Standalone (Python HTTP Server)

```bash
# From the web-ui directory
cd web-ui
python3 -m http.server 8080

# Access the web UI
http://localhost:8080
```

### Option 3: Direct File Access

Simply open `index.html` in your browser:
```bash
# Linux/Mac
open web-ui/index.html

# Or just double-click the file
```

**Note:** When using direct file access, you may encounter CORS issues. Use Option 1 or 2 instead.

## Usage

### Search Knowledge
1. Go to the Search tab
2. Enter your search query
3. Press Enter or click Search
4. Results show filename and matching snippets

### Save an Artifact
1. Go to Save Artifact tab
2. Enter a title (e.g., "Meeting Notes - Team Sync")
3. Write your content (supports markdown)
4. Add tags by typing and pressing Enter
5. Click Save Artifact
6. File is saved with YAML frontmatter and git-committed

### Ingest Text
1. Go to Ingest Text tab
2. Paste your content (article, email, document)
3. Click Ingest
4. Text is automatically chunked by paragraphs
5. Saved with timestamp and "ingested" tag

### AI Digest
1. Go to AI Digest tab
2. Paste text to analyze
3. Click "Analyze with AI"
4. Wait 5-10 seconds for LLM processing
5. Get structured output:
   - Summary
   - Key signals (important points)
   - Action items

## Configuration

The web UI connects to the API at `http://localhost:8000` by default.

To change the API URL, edit the `API_BASE` constant in `index.html`:

```javascript
const API_BASE = 'http://localhost:8000';  // Change this
```

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Brave

## Keyboard Shortcuts

- **Enter** in search box → Search
- **Enter** when adding tags → Add tag
- **Ctrl+S** in forms → Submit (browser default)

## Styling

The UI uses a clean, modern design with:
- Responsive layout (works on mobile)
- Light theme optimized for readability
- Color-coded status indicators
- Smooth animations and transitions

## Development

The web UI is a single-page application built with:
- Vanilla JavaScript (no frameworks)
- Modern CSS with CSS variables
- Fetch API for backend communication
- No build process required

To customize:
1. Edit `index.html` directly
2. Reload browser to see changes
3. All CSS is inline in the `<style>` tag
4. All JS is inline in the `<script>` tag

## Troubleshooting

### "API Offline" Status
- Check if backend is running: `docker-compose ps`
- Check if port 8000 is accessible: `curl http://localhost:8000/health`
- Restart backend: `docker-compose restart backend`

### CORS Errors
- Use the FastAPI-served version at `http://localhost:8000/web`
- The backend has CORS enabled for all origins

### Search Returns No Results
- Make sure you've saved some artifacts first
- Try broader search terms
- Check the `knowledge/` directory has .md files

### AI Digest is Slow
- Normal! LLM processing takes 5-10 seconds
- Depends on your hardware (GPU vs CPU)
- Longer text takes more time

### Blank Page
- Check browser console for errors (F12)
- Make sure JavaScript is enabled
- Try a different browser

## API Endpoints Used

The web UI calls these backend endpoints:

- `GET /health` - API status check
- `GET /search?q=query` - Full-text search
- `POST /artifact/save` - Save structured document
- `POST /ingest` - Import and chunk text
- `POST /digest` - LLM analysis

See `README.md` in project root for full API documentation.

## Future Enhancements

Possible improvements:
- File upload support
- Export knowledge base (ZIP/PDF)
- Dark mode toggle
- Recent files list
- Tag cloud/filter
- Markdown preview
- Bulk operations
- Settings panel
