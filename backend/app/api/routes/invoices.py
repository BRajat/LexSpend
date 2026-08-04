"""Invoice routes, including the PDF parse endpoint."""

from __future__ import annotations

import logging

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.schemas import ParsePDFResponse, ParsedInvoice
from app.services.ai_service import extract_invoice_with_ai
from app.services.pdf_service import extract_text_from_pdf

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post(
    "/parse-pdf",
    response_model=ParsePDFResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload a PDF invoice and extract structured data using AI",
)
async def parse_pdf_invoice(
    file: UploadFile = File(..., description="PDF invoice file"),
) -> ParsePDFResponse:
    """
    Accept a PDF invoice upload, extract its text, and use an LLM to return
    structured invoice data (invoice number, date, vendor, line items, etc.).
    """
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are accepted.",
        )

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        raw_text = extract_text_from_pdf(pdf_bytes)
    except Exception as exc:
        logger.exception("PDF text extraction failed")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not extract text from PDF: {exc}",
        ) from exc

    if not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No readable text found in the PDF.",
        )

    try:
        parsed: ParsedInvoice = await extract_invoice_with_ai(raw_text)
    except Exception as exc:
        logger.exception("AI extraction failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI extraction failed: {exc}",
        ) from exc

    return ParsePDFResponse(
        parsed=parsed,
        raw_text_preview=raw_text[:500],
    )
