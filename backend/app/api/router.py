from fastapi import APIRouter

from app.api.routes import (
    alert,
    audit_log,
    budget,
    budget_ledger,
    firm,
    invoice,
    line_item,
    matter,
    user,
)

api_router = APIRouter()

api_router.include_router(firm.router)
api_router.include_router(matter.router)
api_router.include_router(user.router)
api_router.include_router(invoice.router)
api_router.include_router(line_item.router)
api_router.include_router(budget.router)
api_router.include_router(budget_ledger.router)
api_router.include_router(alert.router)
api_router.include_router(audit_log.router)

