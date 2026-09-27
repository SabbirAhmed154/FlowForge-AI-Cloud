from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.models.workflow import Workflow
from app.models.workflow_run import WorkflowRun

from app.schemas.dashboard import (
    DashboardResponse
)

from app.routes.auth import (
    get_current_user
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/",
    response_model=DashboardResponse
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    # -----------------------------------
    # TOTAL WORKFLOWS
    # -----------------------------------

    total_workflows = (
        db.query(Workflow)
        .filter(
            Workflow.user_id
            == current_user.id
        )
        .count()
    )


    # -----------------------------------
    # TOTAL RUNS
    # -----------------------------------

    total_runs = (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.user_id
            == current_user.id
        )
        .count()
    )


    # -----------------------------------
    # COMPLETED RUNS
    # -----------------------------------

    completed_runs = (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.user_id
            == current_user.id,
            WorkflowRun.status
            == "completed"
        )
        .count()
    )


    # -----------------------------------
    # FAILED RUNS
    # -----------------------------------

    failed_runs = (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.user_id
            == current_user.id,
            WorkflowRun.status
            == "failed"
        )
        .count()
    )


    # -----------------------------------
    # RUNNING RUNS
    # -----------------------------------

    running_runs = (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.user_id
            == current_user.id,
            WorkflowRun.status
            == "running"
        )
        .count()
    )


    # -----------------------------------
    # RECENT WORKFLOWS
    # -----------------------------------

    workflows = (
        db.query(Workflow)
        .filter(
            Workflow.user_id
            == current_user.id
        )
        .order_by(
            Workflow.id.desc()
        )
        .limit(5)
        .all()
    )


    recent_workflows = []

    for workflow in workflows:

        recent_workflows.append({
            "id": workflow.id,
            "name": workflow.name,
            "status": workflow.status,
            "created_at": workflow.created_at
        })


    # -----------------------------------
    # RECENT RUNS
    # -----------------------------------

    runs = (
        db.query(
            WorkflowRun,
            Workflow
        )
        .join(
            Workflow,
            WorkflowRun.workflow_id
            == Workflow.id
        )
        .filter(
            WorkflowRun.user_id
            == current_user.id
        )
        .order_by(
            WorkflowRun.id.desc()
        )
        .limit(5)
        .all()
    )


    recent_runs = []

    for run, workflow in runs:

        recent_runs.append({
            "id": run.id,
            "workflow_id": run.workflow_id,
            "workflow_name": workflow.name,
            "status": run.status,
            "started_at": run.started_at
        })


    return {
        "total_workflows": total_workflows,
        "total_runs": total_runs,
        "completed_runs": completed_runs,
        "failed_runs": failed_runs,
        "running_runs": running_runs,
        "recent_workflows": recent_workflows,
        "recent_runs": recent_runs
    }