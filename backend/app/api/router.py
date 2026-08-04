from fastapi import APIRouter

from app.api.routes import invoices

api_router = APIRouter()
api_router.include_router(invoices.router)
