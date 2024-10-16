import aioredis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial, Product
from core.db import Products


async def get_products(session: AsyncSession) -> list[Products]:
    stmt = select(Products).order_by(Products.id.desc())
    results: Result = await session.execute(stmt)
    products = results.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Products | None:
    return await session.get(Products, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Products:
    product = Products(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def delete_product(
    session: AsyncSession,
    product: Products,
) -> None:
    await session.delete(product)
    await session.commit()


async def update_product(
    session,
    product_in: Products,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Products:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product_in, name, value)
    await session.commit()
    return product_in
