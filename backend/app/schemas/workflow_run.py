from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict
)


class WorkflowRunCreate(BaseModel):

    input_text: str


class StepRunResponse(BaseModel):

    id: int

    workflow_step_id: int

    step_order: int

    step_title: str

    input_text: str | None

    output_text: str | None

    status: str

    model_config = ConfigDict(
        from_attributes=True
    )


class WorkflowRunResponse(BaseModel):

    id: int

    workflow_id: int

    user_id: int

    input_text: str

    final_output: str | None

    status: str

    error_message: str | None

    started_at: datetime

    completed_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )