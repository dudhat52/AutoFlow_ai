
from app.models.incident import ErrorCategory


ERROR_CATEGORIES = {
    "FILE_LOCKED": ErrorCategory.TRANSIENT,
    "API_TIMEOUT": ErrorCategory.TRANSIENT,
    "SERVICE_UNAVAILABLE": ErrorCategory.TRANSIENT,
    "RATE_LIMITED": ErrorCategory.TRANSIENT,

    "MISSING_COLUMN": ErrorCategory.DATA_ERROR,
    "INVALID_FORMAT": ErrorCategory.DATA_ERROR,
    "INVALID_RECORD": ErrorCategory.DATA_ERROR,

    "AUTH_FAILED": ErrorCategory.AUTH_ERROR,
    "TOKEN_EXPIRED": ErrorCategory.AUTH_ERROR,
    "ACCESS_DENIED": ErrorCategory.AUTH_ERROR,
}


def classify_error(error_code: str) -> ErrorCategory:
    normalized = error_code.strip().upper()

    return ERROR_CATEGORIES.get(
        normalized,
        ErrorCategory.UNKNOWN,
    )
