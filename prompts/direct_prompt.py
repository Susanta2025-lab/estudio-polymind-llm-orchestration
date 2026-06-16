def build_direct_prompt(
    conversation: str,
    query: str
):

    return f"""
Conversation History:

{conversation}

User:

{query}

Answer naturally and
use the conversation
history when helpful.
"""
