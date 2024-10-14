from fastapi import Depends, status
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from .schemas import ProductCreate, Product, ProductUpdate, ProductUpdatePartial
from .crud import get_products, create_product, update_product, delete_product
from .dependencies import get_product_by_id


router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product],)
async def get_products_view(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_products(session=session)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED,)
async def create_product_view(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product,)
async def get_product_view(
    product: Product = Depends(get_product_by_id),
):
    return product

@router.put("/{product_id}/", response_model=Product,)
async def update_product_view(
        product_update: ProductUpdate,
        product: Product = Depends(get_product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await update_product(
        session=session,
        product_in=product,
        product_update=product_update,
    )

@router.patch("/{product_id}/", response_model=Product,)
async def update_product_partial_view(
        product_update: ProductUpdatePartial,
        product: Product = Depends(get_product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await update_product(
        session=session,
        product_in=product,
        product_update=product_update,
        partial=True,
    )

@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_product_view(
        product: Product = Depends(get_product_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await delete_product(
        session=session,
        product=product,
    )