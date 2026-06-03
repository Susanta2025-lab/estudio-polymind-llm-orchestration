from typing import TypedDict


class GraphState(TypedDict):

    query: str

    route: str

    model: str

    context: str

    answer: str

    sources: list

    session_id: str
