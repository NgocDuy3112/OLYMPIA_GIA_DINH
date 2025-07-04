from groq_client import GroqClient
from assistant.schema.v0.message import Message



def completions_create(client: GroqClient, messages: list[dict], model: str) -> str:
    """
    Sends a request to the client's `completions.create` method to interact with the language model.

    Args:
        client (Groq): The Groq client object
        messages (list[dict]): A list of message objects containing chat history for the model.
        model (str): The model to use for generating tool calls and responses.

    Returns:
        str: The content of the model's response.
    """
    response = client.chat.completions.create(messages, model=model)
    return str(response.choices[0].message.content)


def build_prompt_structure(message: Message, tag: str = "") -> dict:
    """
    Builds a structured prompt that includes the role and content.

    Args:
        prompt (str): The actual content of the prompt.
        role (str): The role of the speaker (e.g., user, assistant).

    Returns:
        dict: A dictionary representing the structured prompt.
    """
    
    prompt = f"<{tag}>{message.content}</{tag}>" if tag else message.content
    return {"role": message.role, "content": prompt}


def update_chat_history(history: list, message: Message):
    """
    Updates the chat history by appending the latest response.

    Args:
        history (list): The list representing the current chat history.
        msg (str): The message to append.
        role (str): The role type (e.g. 'user', 'assistant', 'system')
    """
    history.append(build_prompt_structure(prompt=message.content, role=message.role))