from llm.inference import ModelRole
from llm.models import AVAILABLE_MODELS

# This function selects the appropriate model based on the query content.
def select_model_role(query: str) -> ModelRole:

    query = query.lower()

    coding_keywords = [
        "python",
        "code",
        "programming",
        "debug",
        "algorithm"
    ]

    summarize_keywords = [
        "summarize",
        "summary",
        "shorten"
    ]

    fast_keywords = [
        "quick",
        "fast"
    ]

    if any(word in query for word in coding_keywords):

        return ModelRole.CODING

    if any(word in query for word in summarize_keywords):

        return ModelRole.SUMMARIZATION

    if any(word in query for word in fast_keywords):

        return ModelRole.FAST

    return ModelRole.GENERAL


def select_model(query: str) -> str:
    """Backward-compatible Ollama model lookup for experiment consumers."""
    return AVAILABLE_MODELS[select_model_role(query).value]
