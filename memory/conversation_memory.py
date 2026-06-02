
conversation_history = []

#function to save a message to the conversation history
def add_message(role: str, content: str):

    conversation_history.append(
        {
            "role": role,
            "content": content
            }
        )
#function to retrieve the conversation history
def get_history():

    return conversation_history[-10:]  # Return the last 10 messages for context

#function to clear the conversation history
def clear_history():

    conversation_history.clear()
