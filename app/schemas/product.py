from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: Optional[str] = Field(default=None, min_length=1, max_length=64)
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
