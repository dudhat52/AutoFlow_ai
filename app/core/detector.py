
from app.models.incident import FailureEvent


def detect_failure(event: FailureEvent) -> str:
    """
    Extract and normalize an error code
    from a validated failure event.
    """

    return event.error_code.strip().upper()
