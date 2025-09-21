from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from ..db import meta
from ..storage import fs_store
from ..ingest import worker
from ..chat import handler
import uvicorn
from contextlib import asynccontextmanager
import time
from fastapi import Request
from .. import observability
from ..ingest import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB and other startup tasks here
    meta.init_db()
    # start background ingestion scheduler
    sched = scheduler.get_default_scheduler()
    sched.start()
    yield
    # Place for graceful shutdown tasks if needed
    sched.stop()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    req_id = f"req-{int(time.time() * 1000)}"
    observability.record_request(req_id, {"method": request.method, "path": request.url.path})
    with observability.default_tracer.start_span(request.url.path):
        resp = await call_next(request)
    observability.record_response(req_id, {"status_code": resp.status_code})
    return resp


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    path = fs_store.save_upload(file.filename, content)
    task_id = meta.create_task(file.filename, upload_path=path)
    # For dev convenience, process synchronously
    worker.process_task(task_id)
    return JSONResponse({"task_id": task_id})


@app.get("/ingest/{task_id}")
def ingest_status(task_id: str):
    t = meta.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="task not found")
    return JSONResponse(t)


@app.post("/chat")
def chat(payload: dict):
    session_id = payload.get("session_id")
    query = payload.get("query")
    top_k = payload.get("top_k", 3)
    result = handler.orchestrate_query(session_id or "", query or "", top_k)
    return JSONResponse(result)


if __name__ == "__main__":
    uvicorn.run("backend.src.api.main:app", host="0.0.0.0", port=8000, reload=True)
