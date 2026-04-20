import anthropic
import base64
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class BedrockClient:
    def __init__(self, **kwargs):  # accepts old args, ignores them
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    def invoke_with_document(self, system_prompt, user_prompt, pdf_data, **kwargs):
        pdf_b64 = base64.standard_b64encode(pdf_data).decode("utf-8")
        message = self.client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=4000,
            system=system_prompt,
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