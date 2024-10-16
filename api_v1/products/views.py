import asyncio
import logging

from fastapi import Depends, status
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from core.db import db_helper, Products
from .schemas import ProductCreate, Product, ProductUpdate, ProductUpdatePartial
from .crud import get_products, create_product, update_product, delete_product
from .dependencies import get_product_by_id

logger = logging.getLogger("fastapi_cache")
router = APIRouter(tags=["Products"])


@router.get(
    "/",
    response_model=list[Product],
)
@cache(expire=10)  # Will save data in cache 10 sec
async def get_products_view(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # products = await redis.lrange("products", 0, -1)
    # print(products)
    # if not products:
    #     products = await get_products(session=session)
    #     print(products)
    #     await redis.lpush(f"products:", *products)
    # products = await get_products(session=session)
    # print(type(products[0]))
    # asyncio.sleep(3)
    return await get_products(session=session)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_view(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await create_product(session=session, product_in=product_in)


@router.get(
    "/{product_id}/",
    response_model=Product,
)
async def get_product_view(
    product: Product = Depends(get_product_by_id),
):
    return product


@cache(expire=60)
@router.put(
    "/{product_id}/",
    response_model=Product,
)
async def update_product_view(
    product_update: ProductUpdate,
    product: Products = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Products:
    logger.info("Data returned from the function (not cached)")
    return await update_product(
        session=session,
        product_in=product,
        product_update=product_update,
    )


@router.patch(
    "/{product_id}/",
    response_model=Product,
)
async def update_product_partial_view(
    product_update: ProductUpdatePartial,
    product: Products = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Products:
    return await update_product(
        session=session,
        product_in=product,
        product_update=product_update,
        partial=True,
    )


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product_view(
    product: Products = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await delete_product(
        session=session,
        product=product,
    )
