from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.routes.artifact import router as artifact_router
from app.routes.knowledge import router as knowledge_router
from app.routes.search import router as search_router
from app.routes.digest import router as digest_router
from app.routes.catalogue import router as catalogue_router

app = FastAPI(title="Personal AI Box")

# Enable CORS for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount web UI if it exists
web_ui_path = Path(__file__).parent.parent / "web-ui"
if web_ui_path.exists():
    app.mount("/web", StaticFiles(directory=str(web_ui_path), html=True), name="web-ui")

app.include_router(artifact_router)
app.include_router(knowledge_router)
app.include_router(search_router)
app.include_router(digest_router)
app.include_router(catalogue_router)


@app.get("/health")
def health():
    return {"status": "ok"}
