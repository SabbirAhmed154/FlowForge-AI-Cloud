from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.workflow_engine import execute_step
from app.database import SessionLocal
from app.models.workflow import (
    TriggerType,
    Workflow,
    WorkflowStep,
)
from app.models.workflow_execution import (
    ExecutionStatus,
    WorkflowExecution,
)


scheduler = BackgroundScheduler()


def run_scheduled_workflow(
    workflow_id: int,
):
    db = SessionLocal()

    try:
        workflow = db.get(
            Workflow,
            workflow_id,
        )

        if workflow is None:
            return

        if not workflow.is_active:
            return

        if workflow.trigger_type != TriggerType.SCHEDULE:
            return

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
            return

        execution = WorkflowExecution(
            workflow_id=workflow.id,
            user_id=workflow.user_id,
            status=ExecutionStatus.RUNNING,
            input_data={
                "trigger": "SCHEDULE"
            },
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
                        "result": result,
                    }
                )

            execution.status = (
                ExecutionStatus.SUCCESS
            )

            execution.output_data = {
                "steps": results
            }

        except Exception as exc:
            execution.status = (
                ExecutionStatus.FAILED
            )

            execution.output_data = {
                "steps": results
            }

            execution.error_message = str(
                exc
            )

        execution.completed_at = (
            datetime.now(timezone.utc)
        )

        db.commit()

    finally:
        db.close()


def schedule_workflow_job(
    workflow: Workflow,
):
    job_id = f"workflow_{workflow.id}"

    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass

    if (
        workflow.trigger_type
        != TriggerType.SCHEDULE
    ):
        return

    if not workflow.is_active:
        return

    if not workflow.schedule_cron:
        return

    trigger = CronTrigger.from_crontab(
        workflow.schedule_cron
    )

    scheduler.add_job(
        run_scheduled_workflow,
        trigger=trigger,
        args=[workflow.id],
        id=job_id,
        replace_existing=True,
    )


def remove_workflow_job(
    workflow_id: int,
):
    job_id = f"workflow_{workflow_id}"

    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass


def load_scheduled_workflows():
    db = SessionLocal()

    try:
        workflows = (
            db.query(Workflow)
            .filter(
                Workflow.trigger_type
                == TriggerType.SCHEDULE,
                Workflow.is_active.is_(True),
            )
            .all()
        )

        for workflow in workflows:
            schedule_workflow_job(
                workflow
            )

    finally:
        db.close()