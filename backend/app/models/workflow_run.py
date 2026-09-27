from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database import Base


class WorkflowRun(Base):

    __tablename__ = "workflow_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    input_text = Column(
        Text,
        nullable=False
    )

    final_output = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(30),
        default="running"
    )

    error_message = Column(
        Text,
        nullable=True
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


class StepRun(Base):

    __tablename__ = "step_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id"),
        nullable=False
    )

    workflow_step_id = Column(
        Integer,
        ForeignKey("workflow_steps.id"),
        nullable=False
    )

    step_order = Column(
        Integer,
        nullable=False
    )

    step_title = Column(
        String(150),
        nullable=False
    )

    input_text = Column(
        Text,
        nullable=True
    )

    output_text = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(30),
        default="running"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )