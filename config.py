# config.py
from agents import AsyncOpenAI, ModelSettings
from typing import Literal
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global model configuration constants
BIG_MODEL = "qwen3-30b-a3b@q8_0"
SMALL_MODEL = "qwen3-1.7b"

# Type alias for model names - only these two values are allowed
Model = Literal["qwen3-30b-a3b@q8_0", "qwen3-1.7b"]

# Default model settings for all agents
default_model_settings = ModelSettings(
    temperature=0.6,
    top_p=0.95
)

# Model-specific settings
big_model_settings = ModelSettings(
    temperature=0.6,
    top_p=0.95
)

small_model_settings = ModelSettings(
    temperature=0.6,
    top_p=0.95
)

_external_client_instance = None


def get_external_client() -> AsyncOpenAI:
    global _external_client_instance
    if _external_client_instance is None:
        api_key_to_use = os.getenv("OPENAI_API_KEY")
        if api_key_to_use is None:
            api_key_to_use = os.getenv(
                "TEST_DUMMY_API_KEY", "dummy_for_local_if_no_env_set"
            )

        base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")

        _external_client_instance = AsyncOpenAI(
            base_url=base_url, api_key=api_key_to_use
        )
    return _external_client_instance
