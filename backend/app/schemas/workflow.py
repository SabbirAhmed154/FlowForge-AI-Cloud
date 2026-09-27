from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict
)


class WorkflowStepCreate(BaseModel):

    step_order: int
    title: str
    prompt: str


class WorkflowStepUpdate(BaseModel):

    step_order: int | None = None
    title: str | None = None
    prompt: str | None = None


class WorkflowStepResponse(BaseModel):

    id: int
    workflow_id: int
    step_order: int
    title: str
    prompt: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class WorkflowCreate(BaseModel):

    name: str
    description: str | None = None


class WorkflowUpdate(BaseModel):

    name: str | None = None
    description: str | None = None
    status: str | None = None


class WorkflowResponse(BaseModel):

    id: int
    user_id: int
    name: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None

    steps: list[WorkflowStepResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )