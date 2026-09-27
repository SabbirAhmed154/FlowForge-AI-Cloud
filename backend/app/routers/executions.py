from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.workflow_engine import execute_step
from app.database import get_db
from app.models.user import User, UserRole
from app.models.workflow import (
    Workflow,
    WorkflowStep,
)
from app.models.workflow_execution import (
    ExecutionStatus,
    WorkflowExecution,
)
from app.schemas.workflow_execution import (
    WorkflowExecutionResponse,
    WorkflowRunRequest,
)


router = APIRouter(
    prefix="/api/workflows",
    tags=["Workflow Executions"],
)


def get_owned_workflow(
    workflow_id: int,
    current_user: User,
    db: Session,
):
    workflow = db.get(
        Workflow,
        workflow_id,
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    if (
        current_user.role != UserRole.ADMIN
        and workflow.user_id
        != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return workflow


@router.post(
    "/{workflow_id}/run",
    response_model=WorkflowExecutionResponse,
)
def run_workflow(
    workflow_id: int,
    data: WorkflowRunRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    workflow = get_owned_workflow(
        workflow_id,
        current_user,
        db,
    )

    if not workflow.is_active:
        raise HTTPException(
            status_code=400,
            detail="Workflow is inactive",
        )

    steps = (
        db.query(WorkflowStep)
        .filter(
            WorkflowStep.workflow_id
            == workflow.id
        )
        .order_by(
            WorkflowStep.step_order.asc()
        )
        .all()
    )

    if not steps:
        raise HTTPException(
            status_code=400,
            detail="Workflow has no steps",
        )

    execution = WorkflowExecution(
        workflow_id=workflow.id,
        user_id=current_user.id,
        status=ExecutionStatus.RUNNING,
        input_data=data.input_data,
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    step_results = []

    try:
        for step in steps:
            result = execute_step(
                action_type=step.action_type.value,
                config_json=step.config_json,
            )

            step_results.append(
                {
                    "step_id": step.id,
                    "step_order": step.step_order,
                    "step_name": step.name,
                    "action_type": (
                        step.action_type.value
                    ),
                    "result": result,
                }
            )

        execution.status = (
            ExecutionStatus.SUCCESS
        )

        execution.output_data = {
            "steps": step_results
        }

        execution.completed_at = (
            datetime.now(timezone.utc)
        )

    except Exception as exc:
        execution.status = (
            ExecutionStatus.FAILED
        )

        execution.output_data = {
            "steps": step_results
        }

        execution.error_message = str(
            exc
        )

        execution.completed_at = (
            datetime.now(timezone.utc)
        )

    db.commit()
    db.refresh(execution)

    return execution


@router.get(
    "/{workflow_id}/executions",
    response_model=list[
        WorkflowExecutionResponse
    ],
)
def list_workflow_executions(
    workflow_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    workflow = get_owned_workflow(
        workflow_id,
        current_user,
        db,
    )

    return (
        db.query(WorkflowExecution)
        .filter(
            WorkflowExecution.workflow_id
            == workflow.id
        )
        .order_by(
            WorkflowExecution.started_at.desc()
        )
        .all()
    )


@router.get(
    "/{workflow_id}/executions/{execution_id}",
    response_model=WorkflowExecutionResponse,
)
def get_workflow_execution(
    workflow_id: int,
    execution_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    workflow = get_owned_workflow(
        workflow_id,
        current_user,
        db,
    )

    execution = db.get(
        WorkflowExecution,
        execution_id,
    )

    if (
        execution is None
        or execution.workflow_id
        != workflow.id
    ):
        raise HTTPException(
            status_code=404,
            detail="Execution not found",
        )

    return execution