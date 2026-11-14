
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Platform(str, Enum):
    POWER_AUTOMATE = "power_automate"
    PYTHON = "python"
    N8N = "n8n"
    API = "api"
    OTHER = "other"


class ErrorCategory(str, Enum):
    TRANSIENT = "TRANSIENT"
    DATA_ERROR = "DATA_ERROR"
    AUTH_ERROR = "AUTH_ERROR"
    UNKNOWN = "UNKNOWN"


class RecommendedAction(str, Enum):
    RETRY_CANDIDATE = "RETRY_CANDIDATE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    STOP_AND_INVESTIGATE = "STOP_AND_INVESTIGATE"


class FailureEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1)
    platform: Platform
    workflow_name: str = Field(min_length=1)
    execution_id: str = Field(min_length=1)
    status: str
    error_code: str = Field(min_length=1)
    error_message: str = Field(min_length=1)

    @field_validator(
        "event_id",
        "workflow_name",
        "execution_id",
        "error_code",
        "error_message",
    )
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be blank")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value.strip().lower() != "failed":
            raise ValueError("Only failed executions are accepted")
        return "failed"


class DiagnosisResult(BaseModel):
    event_id: str
    workflow_name: str
    platform: Platform
    execution_id: str
    error_code: str
    category: ErrorCategory
    recommended_action: RecommendedAction
    explanation: str
    recovery_executed: bool = False
    diagnosed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
