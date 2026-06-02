from llm.models import AVAILABLE_MODELS

# This function selects the appropriate model based on the query content.
def select_model(query: str):

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

        return AVAILABLE_MODELS["coding"]

    if any(word in query for word in summarize_keywords):

        return AVAILABLE_MODELS["summarization"]

    if any(word in query for word in fast_keywords):

        return AVAILABLE_MODELS["fast"]

    return AVAILABLE_MODELS["general"]
