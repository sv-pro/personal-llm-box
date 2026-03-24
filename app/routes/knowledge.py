from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.storage import save_markdown
from app.utils.markdown import split_into_chunks

router = APIRouter()


class IngestRequest(BaseModel):
    text: str


@router.post("/ingest")
def ingest(req: IngestRequest):
    chunks = split_into_chunks(req.text)
    title = f"ingested-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    content = "\n\n".join(chunks)
    filename = save_markdown(title, content, ["ingested"])
    return {"status": "ingested", "filename": filename, "chunks": len(chunks)}
