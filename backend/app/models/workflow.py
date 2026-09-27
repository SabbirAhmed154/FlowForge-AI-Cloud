from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Workflow(Base):

    __tablename__ = "workflows"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(30),
        default="draft"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    steps = relationship(
        "WorkflowStep",
        back_populates="workflow",
        cascade="all, delete-orphan",
        order_by="WorkflowStep.step_order"
    )

    def __repr__(self):
        return f"<Workflow {self.name}>"


class WorkflowStep(Base):

    __tablename__ = "workflow_steps"

    __table_args__ = (
        UniqueConstraint(
            "workflow_id",
            "step_order",
            name="uq_workflow_step_order"
        ),
    )

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

    step_order = Column(
        Integer,
        nullable=False
    )

    title = Column(
        String(150),
        nullable=False
    )

    prompt = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    workflow = relationship(
        "Workflow",
        back_populates="steps"
    )