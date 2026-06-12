from sentence_transformers import util

from rag.embeddings import get_embedding


INTENTS = {

    "rag": [

        "retrieve information from documents",
        "answer using knowledge base",
        "search pdf documents",
        "find information in stored files",
        "retrieve context from vector database",

        "what is langgraph",
        "explain embeddings",
        "what is chromadb",
        "what is retrieval augmented generation",
        "explain rag",
        "explain vector database",
        "tell me about stored knowledge",
        "search my knowledge base",
        "find information in documents",
        "answer from uploaded documents"
    ],

    "tool": [

        "perform a calculation",
        "solve a math expression",
        "tell me the current time",
        "what time is it",
        "calculate a number",
        "use a utility tool"
    ],

    "direct": [

        "general conversation",
        "open ended discussion",
        "creative writing",
        "tell me a joke",
        "write a poem",
        "casual chat",
        "general knowledge question"
    ]
}


# Precompute intent embeddings once at startup
INTENT_EMBEDDINGS = {}

for route, examples in INTENTS.items():

    INTENT_EMBEDDINGS[route] = [

        get_embedding(example)

        for example in examples
    ]


def semantic_route(query: str):

    query_embedding = get_embedding(
        query
    )

    scores = {}

    for route in INTENTS:

        similarities = []

        for example_embedding in INTENT_EMBEDDINGS[route]:

            score = util.cos_sim(
                query_embedding,
                example_embedding
            ).item()

            similarities.append(
                score
            )

        top_scores = sorted(
            similarities,
            reverse=True
        )[:3]

        scores[route] = (
            sum(top_scores)
            / len(top_scores)
        )

    best_route = max(
        scores,
        key=scores.get
    )

    best_score = scores[
        best_route
    ]

    # Fallback to direct if confidence is low
    if best_score < 0.20:

        best_route = "direct"

    confidence = best_score

    print(
        f"\nSelected: {best_route}"
    )

    print(
        f"Confidence: {confidence:.3f}"
    )

    return best_route
