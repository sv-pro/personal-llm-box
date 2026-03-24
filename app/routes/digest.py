import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ollama import generate_text

router = APIRouter()


class DigestRequest(BaseModel):
    text: str


_PROMPT_TEMPLATE = """You are a helpful assistant. Given the following text, produce a structured analysis.

Text:
{text}

Respond with a JSON object with exactly these keys:
- "summary": a short summary (1-3 sentences)
- "signals": a list of key signals or facts (strings)
- "actions": a list of suggested actions (strings)

Return only valid JSON, no extra text."""


@router.post("/digest")
def digest(req: DigestRequest):
    prompt = _PROMPT_TEMPLATE.format(text=req.text)
    try:
        raw = generate_text(prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Ollama error: {exc}") from exc

    # Extract JSON from the response (model may wrap in markdown code fences)
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        # drop opening fence line (e.g. ```json) and closing fence line
        start = 1
        end = len(lines) - 1 if lines[-1].startswith("```") else len(lines)
        raw = "\n".join(lines[start:end])

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        preview = raw[:200] + ("…" if len(raw) > 200 else "")
        raise HTTPException(status_code=500, detail=f"Could not parse LLM response as JSON: {preview}")

    return {
        "summary": data.get("summary", ""),
        "signals": data.get("signals", []),
        "actions": data.get("actions", []),
    }
