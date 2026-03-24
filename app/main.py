from fastapi import FastAPI

from app.routes.artifact import router as artifact_router
from app.routes.knowledge import router as knowledge_router
from app.routes.search import router as search_router
from app.routes.digest import router as digest_router

app = FastAPI(title="Personal AI Box")

app.include_router(artifact_router)
app.include_router(knowledge_router)
app.include_router(search_router)
app.include_router(digest_router)


@app.get("/health")
def health():
    return {"status": "ok"}
