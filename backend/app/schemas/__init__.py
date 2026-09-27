from datetime import datetime

from pydantic import BaseModel


class RecentWorkflow(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime


class RecentRun(BaseModel):
    id: int
    workflow_id: int
    workflow_name: str
    status: str
    started_at: datetime


class DashboardResponse(BaseModel):
    total_workflows: int
    total_runs: int
    completed_runs: int
    failed_runs: int
    running_runs: int

    recent_workflows: list[RecentWorkflow]
    recent_runs: list[RecentRun]