from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.tasks.pipeline import start_pipeline
from backend.core.database import engine
from backend.models.campaign import Base

app = FastAPI(title="AI Sales Machine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    # Cria as tabelas automaticamente no primeiro deploy
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "running", "service": "AI Sales Machine API"}

@app.post("/create-campaign")
def create_campaign(data: dict):
    task = start_pipeline.delay(data)
    return {"task_id": task.id, "status": "queued"}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    from backend.tasks.celery_app import celery
    task = celery.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }
