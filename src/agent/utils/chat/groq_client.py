from groq import Groq
from src.agent.configs import GROQ_API_KEY, MODEL_NAME


class GroqClient:
    def __init__(self, api_key: str = GROQ_API_KEY):
        self.client = Groq(api_key=api_key)

    def create_completions(self, messages: list[dict], model: str = MODEL_NAME, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content.strip()