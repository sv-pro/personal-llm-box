from fastapi import APIRouter
from pathlib import Path
import os
import re
from datetime import datetime

router = APIRouter()

KNOWLEDGE_DIR = Path(os.getenv("KNOWLEDGE_DIR", "/knowledge"))


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown file"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    yaml_text = match.group(1)

    # Parse title
    title_match = re.search(r'title:\s*"([^"]*)"', yaml_text)
    if title_match:
        frontmatter['title'] = title_match.group(1)

    # Parse tags
    tags_match = re.search(r'tags:\s*\[(.*?)\]', yaml_text)
    if tags_match:
        tags_str = tags_match.group(1)
        frontmatter['tags'] = [t.strip(' "') for t in tags_str.split(',') if t.strip()]
    else:
        frontmatter['tags'] = []

    # Parse created_at
    created_match = re.search(r'created_at:\s*["\']?([^"\'\n]+)["\']?', yaml_text)
    if created_match:
        frontmatter['created_at'] = created_match.group(1).strip()

    return frontmatter


def get_preview(content: str, max_length: int = 200) -> str:
    """Get a preview of the content (after frontmatter)"""
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # Remove markdown formatting for preview
    content = re.sub(r'[#*`]', '', content)
    content = content.strip()

    if len(content) > max_length:
        return content[:max_length] + '...'
    return content


@router.get("/catalogue")
def list_files():
    """List all markdown files with metadata"""
    if not KNOWLEDGE_DIR.exists():
        return {"files": []}

    files = []
    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md"), reverse=True):
        if md_file.name == '.gitkeep':
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)
            preview = get_preview(content)

            # Get file stats
            stat = md_file.stat()

            files.append({
                'filename': md_file.name,
                'title': frontmatter.get('title', md_file.stem),
                'tags': frontmatter.get('tags', []),
                'created_at': frontmatter.get('created_at', ''),
                'preview': preview,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except Exception as e:
            # Skip files that can't be read
            continue

    return {"files": files, "total": len(files)}
