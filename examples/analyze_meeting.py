#!/usr/bin/env python3
"""
Example: Meeting notes processor
Usage: python analyze_meeting.py meeting-transcript.txt
"""

import sys
import json
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

def process_meeting(transcript_file):
    """Process meeting transcript: digest + save"""

    # Read transcript
    with open(transcript_file, 'r') as f:
        transcript = f.read()

    print(f"📄 Processing: {transcript_file}")
    print("🤖 Analyzing with LLM...")

    # Get AI analysis
    response = requests.post(
        f"{API_URL}/digest",
        json={"text": transcript}
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return

    analysis = response.json()

    # Build structured content
    content = f"""## Summary
{analysis['summary']}

## Key Points
"""
    for signal in analysis['signals']:
        content += f"- {signal}\n"

    content += "\n## Action Items\n"
    for action in analysis['actions']:
        content += f"- [ ] {action}\n"

    content += f"\n## Full Transcript\n{transcript}"

    # Save to knowledge base
    title = f"Meeting Notes - {datetime.now().strftime('%Y-%m-%d')}"

    save_response = requests.post(
        f"{API_URL}/artifact/save",
        json={
            "title": title,
            "content": content,
            "tags": ["meetings", "analyzed", datetime.now().strftime("%Y-%m")]
        }
    )

    if save_response.status_code == 200:
        result = save_response.json()
        print(f"✅ Saved as: {result['filename']}")
        print("\n📊 Analysis:")
        print(f"Summary: {analysis['summary']}")
        print(f"Signals: {len(analysis['signals'])}")
        print(f"Actions: {len(analysis['actions'])}")
    else:
        print(f"❌ Save failed: {save_response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_meeting.py <transcript-file>")
        sys.exit(1)

    process_meeting(sys.argv[1])
