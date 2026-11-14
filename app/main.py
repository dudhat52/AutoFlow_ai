
from fastapi import FastAPI

from app.models.incident import FailureEvent, DiagnosisResult
from app.core.detector import detect_failure
from app.core.classifier import classify_error
from app.core.policies import get_recommendation


app = FastAPI(
    title="AutoFlow AI",
    description="Automation Failure Detection and Diagnosis API",
    version="0.1.0",
)


def diagnose_failure(event: FailureEvent) -> DiagnosisResult:
    error_code = detect_failure(event)

    category = classify_error(error_code)

    action, explanation = get_recommendation(category)

    return DiagnosisResult(
        event_id=event.event_id,
        workflow_name=event.workflow_name,
        platform=event.platform,
        execution_id=event.execution_id,
        error_code=error_code,
        category=category,
        recommended_action=action,
        explanation=explanation,
        recovery_executed=False,
    )


@app.get("/")
def home():
    return {
        "application": "AutoFlow AI",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/api/v1/incidents",
    response_model=DiagnosisResult,
)
def analyze_incident(event: FailureEvent):
    return diagnose_failure(event)
