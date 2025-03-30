from ..core.interfaces import PromptServiceInterface
from ..utils.prompts import PROMPTS
  # Assuming prompts.py exists in the same directory

class PromptService(PromptServiceInterface):
    def get_prompt(self, prompt_type: str):
        return PROMPTS.get(prompt_type)

    def get_serializable_prompts(self) -> dict[str, str]:
        return {key: str(value) for key, value in PROMPTS.items()}