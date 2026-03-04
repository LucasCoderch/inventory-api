from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.products import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await ProductService.list(db)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductService.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await ProductService.create(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="SKU already exists")


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, payload: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await ProductService.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        return await ProductService.update(db, product, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="SKU already exists")


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductService.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await ProductService.delete(db, product)
    return None
