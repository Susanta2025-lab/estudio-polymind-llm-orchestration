from typing import List, TypedDict


class GraphState(TypedDict, total=False):

    query: str

    route: str

    model_role: str

    model: str

    context: str

    answer: str

    sources: List[dict]

    session_id: str
