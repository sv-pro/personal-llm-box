import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

KNOWLEDGE_DIR = Path(os.getenv("KNOWLEDGE_DIR", "/knowledge"))


def _ensure_git_repo() -> None:
    if not (KNOWLEDGE_DIR / ".git").exists():
        subprocess.run(["git", "init", str(KNOWLEDGE_DIR)], check=True)
        subprocess.run(
            ["git", "config", "user.email", "box@local"],
            cwd=str(KNOWLEDGE_DIR),
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Personal AI Box"],
            cwd=str(KNOWLEDGE_DIR),
            check=True,
        )


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:60]


def save_markdown(title: str, content: str, tags: list[str]) -> str:
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_git_repo()

    created_at = datetime.now(timezone.utc).isoformat()
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = _slugify(title)
    filename = f"{date_str}-{slug}.md"
    filepath = KNOWLEDGE_DIR / filename

    safe_title = title.replace('"', '\\"')
    tags_yaml = ", ".join(f'"{t}"' for t in tags)
    header = f'---\ntitle: "{safe_title}"\ntags: [{tags_yaml}]\ncreated_at: {created_at}\n---\n\n'
    filepath.write_text(header + content, encoding="utf-8")

    _git_commit(filename)
    return filename


def _git_commit(filename: str) -> None:
    subprocess.run(["git", "add", filename], cwd=str(KNOWLEDGE_DIR), check=True)
    result = subprocess.run(
        ["git", "commit", "-m", f"add {filename}"],
        cwd=str(KNOWLEDGE_DIR),
        capture_output=True,
    )
    # exit code 1 means "nothing to commit" — treat as success
    if result.returncode not in (0, 1):
        result.check_returncode()


def list_markdown_files() -> list[Path]:
    if not KNOWLEDGE_DIR.exists():
        return []
    return sorted(KNOWLEDGE_DIR.glob("*.md"))
