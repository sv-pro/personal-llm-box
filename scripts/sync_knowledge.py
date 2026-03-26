#!/usr/bin/env python3
"""
Sync ./knowledge/*.md files into an Open WebUI knowledge base.

Usage:
    python scripts/sync_knowledge.py --url http://localhost:3000 --token <api-token> --kb-name "Personal Knowledge"

The script is idempotent: it checks which filenames are already present in
the knowledge base and only uploads new or modified files.
"""

import argparse
import io
import sys
import time
import zipfile
from pathlib import Path

import requests

DEFAULT_SOURCE_DIR = Path(__file__).parent.parent / "knowledge"
POLL_INTERVAL = 1   # seconds between status checks
POLL_TIMEOUT  = 60  # seconds before giving up on a file


def get_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def list_knowledge_bases(base_url: str, token: str) -> list[dict]:
    r = requests.get(f"{base_url}/api/v1/knowledge/", headers=get_headers(token))
    r.raise_for_status()
    data = r.json()
    # API may return a list directly or a dict with an "items" key
    return data if isinstance(data, list) else data.get("items", [])


def create_knowledge_base(base_url: str, token: str, name: str) -> str:
    r = requests.post(
        f"{base_url}/api/v1/knowledge/create",
        headers=get_headers(token),
        json={"name": name, "description": "Synced from personal-llm-box knowledge/"},
    )
    r.raise_for_status()
    kb_id = r.json()["id"]
    print(f"  Created knowledge base '{name}' (id: {kb_id})")
    return kb_id


def get_or_create_kb(base_url: str, token: str, name: str) -> str:
    for kb in list_knowledge_bases(base_url, token):
        if kb["name"] == name:
            print(f"  Found existing knowledge base '{name}' (id: {kb['id']})")
            return kb["id"]
    return create_knowledge_base(base_url, token, name)


def existing_filenames(base_url: str, token: str, kb_id: str) -> set[str]:
    r = requests.get(f"{base_url}/api/v1/knowledge/{kb_id}/export", headers=get_headers(token))
    r.raise_for_status()
    if not r.content:
        return set()
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        # entries look like "2026-03-25-foo.md.txt" — strip the trailing .txt
        return {Path(name).stem for name in zf.namelist()}


def upload_file(base_url: str, token: str, filepath: Path) -> str:
    with filepath.open("rb") as fh:
        r = requests.post(
            f"{base_url}/api/v1/files/",
            headers=get_headers(token),
            files={"file": (filepath.name, fh, "text/markdown")},
        )
    r.raise_for_status()
    return r.json()["id"]


def wait_for_processing(base_url: str, token: str, file_id: str, filename: str) -> bool:
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        r = requests.get(
            f"{base_url}/api/v1/files/{file_id}/data/content",
            headers=get_headers(token),
        )
        if r.status_code == 200:
            return True
        time.sleep(POLL_INTERVAL)
    print(f"    Timeout waiting for {filename} to process", file=sys.stderr)
    return False


def add_file_to_kb(base_url: str, token: str, kb_id: str, file_id: str) -> None:
    r = requests.post(
        f"{base_url}/api/v1/knowledge/{kb_id}/file/add",
        headers=get_headers(token),
        json={"file_id": file_id},
    )
    r.raise_for_status()


def sync(base_url: str, token: str, kb_name: str, dry_run: bool, source_dir: Path) -> None:
    md_files = sorted(source_dir.rglob("*.md"))
    if not md_files:
        print(f"No markdown files found in {source_dir}/")
        return

    print(f"Found {len(md_files)} markdown files in {source_dir}/")

    kb_id = get_or_create_kb(base_url, token, kb_name)
    already_synced = existing_filenames(base_url, token, kb_id)
    print(f"  {len(already_synced)} files already in knowledge base")

    to_upload = [f for f in md_files if f.name not in already_synced]
    if not to_upload:
        print("Nothing to sync — all files already present.")
        return

    print(f"  {len(to_upload)} new files to upload")

    for filepath in to_upload:
        print(f"  Uploading {filepath.name} ...", end=" ", flush=True)
        if dry_run:
            print("(dry run)")
            continue

        file_id = upload_file(base_url, token, filepath)
        if wait_for_processing(base_url, token, file_id, filepath.name):
            add_file_to_kb(base_url, token, kb_id, file_id)
            print("done")
        else:
            print("FAILED (processing timeout)")

    print("Sync complete.")


def main():
    parser = argparse.ArgumentParser(description="Sync knowledge/ into Open WebUI knowledge base")
    parser.add_argument("--url",     default="http://localhost:3000",  help="Open WebUI base URL")
    parser.add_argument("--token",   required=True,                    help="Open WebUI API token")
    parser.add_argument("--kb-name", default="Personal Knowledge",     help="Knowledge base name")
    parser.add_argument("--dir",     default=DEFAULT_SOURCE_DIR,       help="Directory of .md files to sync", type=Path)
    parser.add_argument("--dry-run", action="store_true",              help="List files without uploading")
    args = parser.parse_args()

    sync(args.url, args.token, args.kb_name, args.dry_run, args.dir)


if __name__ == "__main__":
    main()
