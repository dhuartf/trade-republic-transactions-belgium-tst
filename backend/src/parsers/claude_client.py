import anthropic
import base64
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__) 

class ClaudeClient:
    DEFAULT_MAX_TOKENS = 4000
    DEFAULT_TEMPERATURE = 0.0
    DEFAULT_MODEL = "claude-haiku-4-5"  # Change to "claude-sonnet-3-5" if you want to use that model instead
    

    def __init__(
        self,
        max_tokens: int = DEFAULT_MAX_TOKENS, 
        temperature: float = DEFAULT_TEMPERATURE, 
        model: str = DEFAULT_MODEL
    ):  # accepts old args, ignores them
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = model
        logger.info(
            f"Initialized ClaudeClient with model={model}, max_tokens={max_tokens}, temperature={temperature}"
        )
        

    def _supports_caching(self) -> bool:
        CACHE_SUPPORTED_MODELS = {"claude-haiku", "claude-sonnet", "claude-opus"}
        return any(name in self.model for name in CACHE_SUPPORTED_MODELS)
    
    def invoke_with_document(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        pdf_data: bytes, 
        enable_caching: bool = True
    ) -> str:
        """
        Invoke claude model with a PDF document and prompts.

        Args:
            system_prompt: System-level instructions (will be cached if enabled)
            user_prompt: User message text
            pdf_data: PDF file content as bytes
            enable_caching: Whether to enable prompt caching for system prompt

        Returns:
            The text response from the model

        Raises:
            ValueError: If the response format is invalid
            Exception: For other API errors
        """
        logger.debug(f"Invoking Claude model {self.model} with PDF document")


        # Build system prompt with optional caching
        if enable_caching:
            system = [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        else:
            system = system_prompt  # plain string, no caching

        try:
            pdf_b64 = base64.standard_b64encode(pdf_data).decode("utf-8")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_b64
                            }
                        },
                        {"type": "text", "text": user_prompt}
                    ]
                }]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error invoking Claude model: {e}")
            raise