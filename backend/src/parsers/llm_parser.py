"""
LLM-based transaction parser using AWS Bedrock.

This module provides the main interface for parsing financial transactions
from PDF documents using Large Language Models (LLMs) via AWS Bedrock.

Supports multimodal input (direct PDF processing) and prompt caching for efficiency.
"""

import logging
from typing import List

from ..models.transaction import Transaction
from .claude_client import ClaudeClient
from .prompts import get_system_prompt, get_user_prompt
from .response_parser import ResponseParser

logger = logging.getLogger(__name__)


class LLMParser:
    """
    Uses Claude API to parse transaction data from PDF documents.

    This class provides a high-level interface for extracting structured
    transaction data from PDF files using LLMs with multimodal capabilities.

    The system prompt is cached to reduce costs and latency on repeated calls.
    """

    def __init__(self, **kwargs):
        self.claude_client = ClaudeClient()
        self.enable_caching = True

    def parse_transactions(self, pdf_data: bytes) -> List[Transaction]:
        """
        Parse transactions from PDF document using Claude with multimodal input.

        Args:
            pdf_data: PDF file content as bytes

        Returns:
            List of Transaction objects parsed from the PDF

        Raises:
            ValueError: If the response cannot be parsed
            Exception: For other errors during parsing
        """
        try:
            logger.info(f"Parsing PDF document ({len(pdf_data)} bytes) with multimodal input")

            # Get system and user prompts
            system_prompt = get_system_prompt()
            user_prompt = get_user_prompt()

            # Call the LLM with PDF document
            response = self.claude_client.invoke_with_document(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                pdf_data=pdf_data,
                enable_caching=self.enable_caching,
            )

            # Parse the response into Transaction objects
            transactions = ResponseParser.parse_transactions(response)

            logger.info(f"Successfully parsed {len(transactions)} transactions")
            return transactions

        except Exception as e:
            logger.error(f"Error parsing transactions with LLM: {e}")
            raise
