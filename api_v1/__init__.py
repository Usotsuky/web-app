from fastapi import APIRouter
from .products.views import router as product_route

router = APIRouter()
router.include_router(product_route, prefix="/products")
