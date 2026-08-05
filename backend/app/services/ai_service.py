"""AI-powered invoice extraction using LangChain + Groq structured outputs."""

from __future__ import annotations

import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.core.config import settings
from app.schemas.schemas import ParsedInvoice

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    """You are an expert AI legal billing auditor and data extraction specialist. Your task is to extract structured invoice data from raw legal PDF text.

CRITICAL INSTRUCTIONS:
1. Return ONLY valid JSON matching the requested schema. Do not wrap the JSON in conversational text or markdown code blocks unless requested, but ensure it is strictly parseable.
2. HANDLING MISSING DATA: 
   - If a specific field or metadata attribute is not found in the text, explicitly set its value to `null` (for strings/numbers/objects).
   - For lists (such as `line_items`, `timekeeper_entries`, or `expenses`), if no entries exist, return an empty array `[]` instead of `null` or omitting the field.
3. DATA FORMATTING RULES:
   - `invoice_total`, `hours`, `rate`, and `line_total` must be numeric values (integers or floats) where available. If unparseable or missing, use `null`.
   - Dates should be formatted as string values (e.g., "YYYY-MM-DD") if available."""
)

_HUMAN_TEMPLATE = "Extract invoice data from the following text:\n\n{text}"


def get_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0,
    )


async def extract_invoice_with_ai(raw_text: str) -> ParsedInvoice:
    """Use an LLM with structured output to parse invoice fields from raw text."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(ParsedInvoice, method="json_mode")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _SYSTEM_PROMPT),
            ("human", _HUMAN_TEMPLATE),
        ]
    )

    chain = prompt | structured_llm
    result: ParsedInvoice = await chain.ainvoke({"text": raw_text[:12000]})
    return result
