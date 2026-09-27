from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.workflow_execution import ExecutionStatus


class WorkflowRunRequest(BaseModel):
    input_data: dict[str, Any] | None = None


class WorkflowExecutionResponse(BaseModel):
    id: int
    workflow_id: int
    user_id: int
    status: ExecutionStatus
    input_data: dict | None
    output_data: dict | None
    error_message: str | None
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)