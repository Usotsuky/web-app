from fastapi import HTTPException, status, Depends
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from .schemas import ProductCreate, Product
from .crud import get_products, get_product, create_product


router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products_view(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_products(session=session)


@router.post("/", response_model=Product)
async def create_product_view(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product_view(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    product = await get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found"
    )
