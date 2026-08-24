import logging

from llm.operational import request_id


logger = logging.getLogger(__name__)


def log_request(route: str, operation: str, outcome: str, duration: float) -> None:
    """Log bounded operational fields without prompts or session content."""
    logger.info(
        "Application request completed request_id=%s route=%s operation=%s "
        "outcome=%s duration_seconds=%.6f",
        request_id(), route, operation, outcome, duration,
    )
