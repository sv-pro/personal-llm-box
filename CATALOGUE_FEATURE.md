# 📚 Catalogue Feature

## Overview

The Catalogue tab provides a comprehensive view of your entire knowledge base without requiring search queries.

**Access:** http://localhost:8000/web/ → Click "📚 Catalogue" tab (default)

---

## Features

### 📊 Quick Stats Dashboard
At the top, see:
- **Total Items** - Number of files in your knowledge base
- **Unique Tags** - How many different tags you're using
- **Total Size** - Combined size of all your knowledge

### 🔧 Filtering & Sorting

**Sort Options:**
- **Newest First** (default) - Most recent items at top
- **Oldest First** - Chronological order from beginning
- **Title A-Z** - Alphabetical by title

**Tag Filter:**
- Dropdown shows all tags in use
- Select a tag to show only items with that tag
- "All Tags" shows everything

### 📄 Catalogue Items

Each item shows:
- **Title** - From YAML frontmatter or filename
- **Filename** - Actual file name in `knowledge/`
- **Date** - When it was created
- **Tags** - Visual tag pills (click-friendly)
- **Preview** - First ~200 characters of content
- **File Size** - In bytes, KB, or MB

### 🔄 Auto-Refresh

The catalogue automatically refreshes when you:
- Save a new artifact
- Ingest new text
- Click the "🔄 Refresh" button

---

## Usage Examples

### Browse All Knowledge
1. Open web UI
2. Catalogue tab loads automatically
3. Scroll through all your items
4. Click on any item to view (coming soon: full viewer)

### Find Items by Tag
1. Click the tag filter dropdown
2. Select a tag (e.g., "meetings")
3. View only items with that tag
4. Switch back to "All Tags" to see everything

### View Recent Activity
1. Set sort to "Newest First"
2. See what you've saved recently
3. Quick overview of your latest work

### Check Knowledge Base Size
1. Look at stats at top
2. See total items and storage used
3. Monitor your knowledge growth

---

## API Endpoint

**GET /catalogue**

Returns all markdown files with metadata:

```json
{
  "files": [
    {
      "filename": "2026-03-25-my-note.md",
      "title": "My Note",
      "tags": ["tag1", "tag2"],
      "created_at": "2026-03-25T10:30:00+00:00",
      "preview": "First 200 chars of content...",
      "size": 1234,
      "modified": "2026-03-25T10:30:00"
    }
  ],
  "total": 1
}
```

---

## Technical Details

### Frontmatter Parsing
- Extracts title, tags, and created_at from YAML
- Falls back to filename if title missing
- Handles various YAML formats gracefully

### Preview Generation
- Removes frontmatter section
- Strips markdown formatting
- Takes first 200 characters
- Adds "..." if truncated

### File Sorting
- Date sorting uses `created_at` or `modified`
- Title sorting is case-insensitive
- Reverse chronological by default

### Performance
- Fast even with hundreds of files
- Loads on-demand (not cached)
- Lightweight response format

---

## Future Enhancements

Possible improvements:
- **Full file viewer** - Modal/panel to view entire content
- **Edit in place** - Update files directly from UI
- **Delete files** - Remove items from catalogue
- **Tag management** - Rename/merge tags
- **Export selection** - Download multiple files
- **Grid view** - Alternative layout option
- **Search within catalogue** - Filter by title/preview
- **Date range filter** - Show items from specific period

---

## Comparison: Catalogue vs Search

| Feature | Catalogue | Search |
|---------|-----------|--------|
| Use case | Browse everything | Find specific content |
| Shows | All files (paginated) | Matching results only |
| Filtering | By tag | By text match |
| Sorting | Date/Title | Relevance |
| Preview | Always shown | Snippet with match |
| Performance | Fast for <1000 files | Instant for any size |

**Best Practice:** Use Catalogue to explore, Search to find.

---

## Tips

**Organization:**
- Use consistent tags for better filtering
- Add date tags: `2026`, `q1`, `march`
- Add category tags: `work`, `personal`, `learning`

**Workflow:**
1. Start day with Catalogue view
2. Review recent items
3. Check what needs follow-up
4. Use Search for specific queries

**Maintenance:**
- Periodically review "Oldest First"
- Check for items that need updates
- Consolidate related items
- Clean up unused tags

---

## Keyboard Shortcuts

When catalogue is focused:
- **Tab** - Navigate between controls
- **Arrow keys** - Scroll through items
- **Enter** - Open selected item (coming soon)

---

## Mobile Experience

The catalogue is fully responsive:
- Items stack vertically
- Stats reorganize into grid
- Touch-friendly item selection
- Swipe to scroll

---

## Examples

### Daily Review
```
1. Open Catalogue
2. Sort: Newest First
3. Review today's items
4. Check yesterday's todos
```

### Topic Research
```
1. Filter by tag: "research"
2. Sort: Title A-Z
3. Review all research items
4. Find gaps in knowledge
```

### Cleanup Session
```
1. Sort: Oldest First
2. Review old items
3. Update outdated content
4. Archive completed items
```

---

## Troubleshooting

**"No knowledge base items yet"**
- Save your first artifact
- Or ingest some text
- Catalogue will update automatically

**Items not showing**
- Check tag filter (reset to "All Tags")
- Click Refresh button
- Check `knowledge/` directory has .md files

**Wrong item count**
- Some files may have parse errors
- Check file format (YAML frontmatter)
- Non-.md files are ignored

**Preview looks weird**
- Markdown formatting is stripped for preview
- Click item to see full formatted content (coming soon)

---

## Integration

The catalogue data is available via API for:
- Custom dashboards
- Analytics tools
- Backup scripts
- Mobile apps

Example API usage:
```bash
# Get all files
curl http://localhost:8000/catalogue | jq .

# Count items
curl -s http://localhost:8000/catalogue | jq '.total'

# List all tags
curl -s http://localhost:8000/catalogue | \
  jq -r '.files[].tags[]' | sort -u
```

---

**Enjoy browsing your knowledge! 📚**
