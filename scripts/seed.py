"""
Seed script: borra datos de prueba e inserta productos reales desde el CSV de Kaggle.
Uso: .venv/Scripts/python scripts/seed.py
"""

import asyncio
import csv
import sys
from pathlib import Path

# Permite importar desde app/
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import delete, text

from app.db.models import Order, OrderItem, Product
from app.db.session import AsyncSessionLocal

DATASET_PATH = Path.home() / ".cache/kagglehub/datasets/thedevastator/online-retail-transaction-data/versions/1/online_retail.csv"


def load_products_from_csv() -> list[dict]:
    """Lee el CSV y devuelve un producto único por StockCode."""
    seen: dict[str, dict] = {}

    with open(DATASET_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row["StockCode"].strip()
            description = row["Description"].strip()
            price_raw = row["UnitPrice"].strip()

            # Ignorar filas sin SKU, descripción vacía o precio inválido
            if not sku or not description:
                continue
            try:
                price = float(price_raw)
            except ValueError:
                continue
            if price <= 0:
                continue

            # Solo guardar la primera aparición de cada SKU
            if sku not in seen:
                seen[sku] = {
                    "sku": sku,
                    "name": description[:255],
                    "description": None,
                    "price": round(price, 2),
                    "stock": 100,  # stock inicial por defecto
                }

    return list(seen.values())


async def seed():
    products = load_products_from_csv()
    print(f"Productos únicos encontrados en CSV: {len(products)}")

    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. Borrar en orden para respetar FK
            print("Borrando order_items...")
            await session.execute(delete(OrderItem))

            print("Borrando orders...")
            await session.execute(delete(Order))

            print("Borrando products...")
            await session.execute(delete(Product))

            # Resetear secuencia de IDs
            await session.execute(text("ALTER SEQUENCE products_id_seq RESTART WITH 1"))

        # 2. Insertar productos en lotes de 500
        print("Insertando productos reales...")
        batch_size = 500
        total = 0

        async with session.begin():
            for i in range(0, len(products), batch_size):
                batch = products[i : i + batch_size]
                session.add_all([Product(**p) for p in batch])
                total += len(batch)
                print(f"  {total}/{len(products)} insertados...")

    print(f"\nSeed completado: {total} productos cargados.")


if __name__ == "__main__":
    asyncio.run(seed())