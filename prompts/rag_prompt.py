def build_rag_prompt(
    conversation: str,
    context: str,
    query: str
):

    return f"""
Conversation History:

{conversation}

Context:

{context}

Question:

{query}

Answer using the
provided context.

If the answer is not
contained in the
context, say so.

Do not hallucinate.
"""
