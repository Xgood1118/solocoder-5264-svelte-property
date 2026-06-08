from fastapi import APIRouter

from .properties import router as properties_router
from .tenants import router as tenants_router
from .contracts import router as contracts_router
from .bills import router as bills_router
from .repairs import router as repairs_router
from .renewals import router as renewals_router
from .checkout import router as checkout_router

api_router = APIRouter(prefix="/api")

api_router.include_router(properties_router)
api_router.include_router(tenants_router)
api_router.include_router(contracts_router)
api_router.include_router(bills_router)
api_router.include_router(repairs_router)
api_router.include_router(renewals_router)
api_router.include_router(checkout_router)

__all__ = ["api_router"]
