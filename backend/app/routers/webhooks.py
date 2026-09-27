from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core.workflow_engine import execute_step
from app.database import SessionLocal
from app.models.workflow import Workflow, WorkflowStep
from app.models.workflow_execution import (
    ExecutionStatus,
    WorkflowExecution,
)


router = APIRouter(
    prefix="/api/webhooks",
    tags=["Webhooks"],
)


@router.post("/{webhook_token}")
def run_webhook(
    webhook_token: str,
    payload: dict | None = None,
):
    db: Session = SessionLocal()

    try:
        workflow = (
            db.query(Workflow)
            .filter(
                Workflow.webhook_token == webhook_token
            )
            .first()
        )

        if workflow is None:
            raise HTTPException(
                status_code=404,
                detail="Webhook not found",
            )

        if not workflow.is_active:
            raise HTTPException(
                status_code=400,
                detail="Workflow is inactive",
            )

        steps = (
            db.query(WorkflowStep)
            .filter(
                WorkflowStep.workflow_id == workflow.id
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
            user_id=workflow.user_id,
            status=ExecutionStatus.RUNNING,
            input_data=payload or {},
        )

        db.add(execution)
        db.commit()
        db.refresh(execution)

        results = []

        try:
            for step in steps:
                result = execute_step(
                    action_type=step.action_type.value,
                    config_json=step.config_json,
                )

                results.append(
                    {
                        "step_id": step.id,
                        "step_order": step.step_order,
                        "step_name": step.name,
                        "action_type": step.action_type.value,
                        "result": result,
                    }
                )

            execution.status = ExecutionStatus.SUCCESS
            execution.output_data = {
                "steps": results
            }

        except Exception as exc:
            execution.status = ExecutionStatus.FAILED
            execution.output_data = {
                "steps": results
            }
            execution.error_message = str(exc)

        execution.completed_at = (
            datetime.now(timezone.utc)
        )

        db.commit()
        db.refresh(execution)

        return {
            "execution_id": execution.id,
            "status": execution.status.value,
        }

    finally:
        db.close()