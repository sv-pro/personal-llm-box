from fastapi import APIRouter, Query

from app.services.storage import list_markdown_files

router = APIRouter()


@router.get("/search")
def search(q: str = Query(..., min_length=1)):
    results = []
    query_lower = q.lower()
    for filepath in list_markdown_files():
        text = filepath.read_text(encoding="utf-8")
        if query_lower in text.lower():
            lines = text.splitlines()
            matching = [ln for ln in lines if query_lower in ln.lower()]
            snippet = " … ".join(matching[:3])
            results.append({"filename": filepath.name, "snippet": snippet})
    return {"query": q, "results": results}
