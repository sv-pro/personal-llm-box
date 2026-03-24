from fastapi import APIRouter
from pydantic import BaseModel

from app.services.storage import save_markdown

router = APIRouter()


class ArtifactRequest(BaseModel):
    title: str
    content: str
    tags: list[str] = []


@router.post("/artifact/save")
def save_artifact(req: ArtifactRequest):
    filename = save_markdown(req.title, req.content, req.tags)
    return {"status": "saved", "filename": filename}
