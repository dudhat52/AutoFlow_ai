
from app.models.incident import (
    ErrorCategory,
    RecommendedAction,
)


RECOVERY_POLICIES = {
    ErrorCategory.TRANSIENT: (
        RecommendedAction.RETRY_CANDIDATE,
        "The failure may be temporary. "
        "Verify retry safety before repeating the operation.",
    ),

    ErrorCategory.DATA_ERROR: (
        RecommendedAction.HUMAN_REVIEW,
        "Input data is invalid or incomplete. "
        "Review the source before processing again.",
    ),

    ErrorCategory.AUTH_ERROR: (
        RecommendedAction.STOP_AND_INVESTIGATE,
        "Authentication or authorization failed. "
        "Check access permissions and credentials.",
    ),

    ErrorCategory.UNKNOWN: (
        RecommendedAction.HUMAN_REVIEW,
        "Unrecognized error. Manual investigation is required.",
    ),
}


def get_recommendation(
    category: ErrorCategory,
) -> tuple[RecommendedAction, str]:

    return RECOVERY_POLICIES.get(
        category,
        RECOVERY_POLICIES[ErrorCategory.UNKNOWN],
    )
