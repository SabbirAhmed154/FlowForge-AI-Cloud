from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.database import (
    Base,
    engine
)

from app.models import (
    User,
    Workflow,
    WorkflowStep,
    WorkflowRun,
    StepRun
)

from app.routes.auth import (
    router as auth_router
)

from app.routes.workflows import (
    router as workflow_router
)

from app.routes.workflow_runs import (
    router as workflow_run_router
)

from app.routes.dashboard import (
    router as dashboard_router
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="FlowForge AI Cloud",
    version="1.0.0"
)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

app.include_router(workflow_router)

app.include_router(workflow_run_router)

app.include_router(dashboard_router)


@app.get("/")
def home():

    return {
        "message":
        "FlowForge AI Cloud API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }