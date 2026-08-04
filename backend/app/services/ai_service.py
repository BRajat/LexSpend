"""AI-powered invoice extraction using LangChain + OpenAI structured outputs."""

from __future__ import annotations

import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.schemas import ParsedInvoice

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are a legal billing expert. Extract structured invoice data from the "
    "provided raw PDF text. Return only the JSON matching the requested schema. "
    "If a field is not found, use null."
)

_HUMAN_TEMPLATE = "Extract invoice data from the following text:\n\n{text}"


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )


async def extract_invoice_with_ai(raw_text: str) -> ParsedInvoice:
    """Use an LLM with structured output to parse invoice fields from raw text."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(ParsedInvoice)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _SYSTEM_PROMPT),
            ("human", _HUMAN_TEMPLATE),
        ]
    )

    chain = prompt | structured_llm
    result: ParsedInvoice = await chain.ainvoke({"text": raw_text[:12000]})
    return result
