import enum
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    JSON,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ActionType(str, enum.Enum):
    HTTP_REQUEST = "HTTP_REQUEST"
    AI_TEXT = "AI_TEXT"
    WEBHOOK = "WEBHOOK"
    DELAY = "DELAY"


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    workflow_id: Mapped[int] = mapped_column(
        ForeignKey(
            "workflows.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    action_type: Mapped[ActionType] = mapped_column(
        Enum(ActionType),
        nullable=False,
    )

    step_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    action_config: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )