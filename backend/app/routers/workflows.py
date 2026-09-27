from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User

from app.models.workflow import (
    Workflow,
    WorkflowStep
)

from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowStepCreate,
    WorkflowStepUpdate,
    WorkflowStepResponse
)

from app.routes.auth import get_current_user


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


# ==========================================
# CREATE WORKFLOW
# ==========================================

@router.post(
    "/",
    response_model=WorkflowResponse
)
def create_workflow(
    data: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    workflow = Workflow(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        status="draft"
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return workflow


# ==========================================
# MY WORKFLOWS
# ==========================================

@router.get(
    "/",
    response_model=list[WorkflowResponse]
)
def get_my_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    workflows = (
        db.query(Workflow)
        .filter(
            Workflow.user_id
            == current_user.id
        )
        .order_by(
            Workflow.id.desc()
        )
        .all()
    )

    return workflows


# ==========================================
# WORKFLOW DETAIL
# ==========================================

@router.get(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def get_workflow(
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

    return workflow


# ==========================================
# UPDATE WORKFLOW
# ==========================================

@router.patch(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def update_workflow(
    workflow_id: int,
    data: WorkflowUpdate,
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


    update_data = data.model_dump(
        exclude_unset=True
    )


    for key, value in update_data.items():

        setattr(
            workflow,
            key,
            value
        )


    db.commit()
    db.refresh(workflow)

    return workflow


# ==========================================
# DELETE WORKFLOW
# ==========================================

@router.delete(
    "/{workflow_id}"
)
def delete_workflow(
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


    db.delete(workflow)

    db.commit()


    return {
        "message":
        "Workflow deleted successfully"
    }


# ==========================================
# ADD STEP
# ==========================================

@router.post(
    "/{workflow_id}/steps",
    response_model=WorkflowStepResponse
)
def add_workflow_step(
    workflow_id: int,
    data: WorkflowStepCreate,
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


    existing_step = (
        db.query(WorkflowStep)
        .filter(
            WorkflowStep.workflow_id
            == workflow_id,

            WorkflowStep.step_order
            == data.step_order
        )
        .first()
    )


    if existing_step:

        raise HTTPException(
            status_code=400,
            detail="Step order already exists"
        )


    step = WorkflowStep(
        workflow_id=workflow.id,
        step_order=data.step_order,
        title=data.title,
        prompt=data.prompt
    )


    db.add(step)

    db.commit()

    db.refresh(step)


    return step


# ==========================================
# UPDATE STEP
# ==========================================

@router.patch(
    "/{workflow_id}/steps/{step_id}",
    response_model=WorkflowStepResponse
)
def update_workflow_step(
    workflow_id: int,
    step_id: int,
    data: WorkflowStepUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    step = (
        db.query(WorkflowStep)
        .join(Workflow)
        .filter(
            WorkflowStep.id == step_id,
            WorkflowStep.workflow_id
            == workflow_id,
            Workflow.user_id
            == current_user.id
        )
        .first()
    )


    if not step:

        raise HTTPException(
            status_code=404,
            detail="Workflow step not found"
        )


    update_data = data.model_dump(
        exclude_unset=True
    )


    if "step_order" in update_data:

        duplicate = (
            db.query(WorkflowStep)
            .filter(
                WorkflowStep.workflow_id
                == workflow_id,

                WorkflowStep.step_order
                == update_data[
                    "step_order"
                ],

                WorkflowStep.id
                != step.id
            )
            .first()
        )


        if duplicate:

            raise HTTPException(
                status_code=400,
                detail="Step order already exists"
            )


    for key, value in update_data.items():

        setattr(
            step,
            key,
            value
        )


    db.commit()
    db.refresh(step)

    return step


# ==========================================
# DELETE STEP
# ==========================================

@router.delete(
    "/{workflow_id}/steps/{step_id}"
)
def delete_workflow_step(
    workflow_id: int,
    step_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    step = (
        db.query(WorkflowStep)
        .join(Workflow)
        .filter(
            WorkflowStep.id == step_id,
            WorkflowStep.workflow_id
            == workflow_id,
            Workflow.user_id
            == current_user.id
        )
        .first()
    )


    if not step:

        raise HTTPException(
            status_code=404,
            detail="Workflow step not found"
        )


    db.delete(step)

    db.commit()


    return {
        "message":
        "Workflow step deleted successfully"
    }