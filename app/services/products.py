from __future__ import annotations

import builtins

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    async def list(db: AsyncSession) -> builtins.list[Product]:
        res = await db.execute(select(Product).order_by(Product.id))
        return list(res.scalars().all())

    @staticmethod
    async def get(db: AsyncSession, product_id: int) -> Product | None:
        res = await db.execute(select(Product).where(Product.id == product_id))
        return res.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        db.add(product)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(product)
        return product

    @staticmethod
    async def update(db: AsyncSession, product: Product, data: ProductUpdate) -> Product:
        payload = data.model_dump(exclude_unset=True)
        for k, v in payload.items():
            setattr(product, k, v)

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise

        await db.refresh(product)
        return product

    @staticmethod
    async def delete(db: AsyncSession, product: Product) -> None:
        await db.delete(product)
        await db.commit()
