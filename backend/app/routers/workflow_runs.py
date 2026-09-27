from datetime import (
    datetime,
    timezone
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User

from app.models.workflow import (
    Workflow
)

from app.models.workflow_run import (
    WorkflowRun,
    StepRun
)

from app.schemas.workflow_run import (
    WorkflowRunCreate,
    WorkflowRunResponse,
    StepRunResponse
)

from app.routes.auth import (
    get_current_user
)

from app.services.ai_service import (
    run_ai_step
)


router = APIRouter(
    prefix="/workflows",
    tags=["Workflow Runs"]
)


@router.post(
    "/{workflow_id}/run",
    response_model=WorkflowRunResponse
)
def run_workflow(
    workflow_id: int,
    data: WorkflowRunCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    workflow = (
        db.query(Workflow)
        .filter(
            Workflow.id == workflow_id,
            Workflow.user_id
            == current_user.id
        )
        .first()
    )

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )


    if not workflow.steps:

        raise HTTPException(
            status_code=400,
            detail="Workflow has no steps"
        )


    run = WorkflowRun(
        workflow_id=workflow.id,
        user_id=current_user.id,
        input_text=data.input_text,
        status="running"
    )


    db.add(run)

    db.commit()

    db.refresh(run)


    current_input = data.input_text


    try:

        for step in workflow.steps:

            step_run = StepRun(
                run_id=run.id,
                workflow_step_id=step.id,
                step_order=step.step_order,
                step_title=step.title,
                input_text=current_input,
                status="running"
            )


            db.add(step_run)

            db.commit()

            db.refresh(step_run)


            output = run_ai_step(
                step_title=step.title,
                step_prompt=step.prompt,
                input_text=current_input
            )


            step_run.output_text = output

            step_run.status = "completed"

            db.commit()


            current_input = output


        run.final_output = current_input

        run.status = "completed"

        run.completed_at = datetime.now(
            timezone.utc
        )


        workflow.status = "completed"


        db.commit()

        db.refresh(run)


        return run


    except Exception as error:

        run.status = "failed"

        run.error_message = str(error)

        run.completed_at = datetime.now(
            timezone.utc
        )


        workflow.status = "failed"


        db.commit()


        raise HTTPException(
            status_code=500,
            detail=f"Workflow failed: {error}"
        )


@router.get(
    "/{workflow_id}/runs",
    response_model=list[
        WorkflowRunResponse
    ]
)
def workflow_run_history(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    workflow = (
        db.query(Workflow)
        .filter(
            Workflow.id == workflow_id,
            Workflow.user_id
            == current_user.id
        )
        .first()
    )


    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )


    runs = (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.workflow_id
            == workflow_id,
            WorkflowRun.user_id
            == current_user.id
        )
        .order_by(
            WorkflowRun.id.desc()
        )
        .all()
    )


    return runs


@router.get(
    "/runs/{run_id}/steps",
    response_model=list[
        StepRunResponse
    ]
)
def run_step_history(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    run = (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.id == run_id,
            WorkflowRun.user_id
            == current_user.id
        )
        .first()
    )


    if not run:

        raise HTTPException(
            status_code=404,
            detail="Workflow run not found"
        )


    steps = (
        db.query(StepRun)
        .filter(
            StepRun.run_id == run.id
        )
        .order_by(
            StepRun.step_order
        )
        .all()
    )


    return steps