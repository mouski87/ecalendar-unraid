from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_db
from ..models import Category
from ..schemas import CategoryCreate, CategoryRead

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Category).order_by(Category.name))
    return [CategoryRead.model_validate(c) for c in r.scalars().all()]


@router.post("", response_model=CategoryRead, status_code=201)
async def create_category(schema: CategoryCreate, db: AsyncSession = Depends(get_db)):
    cat = Category(**schema.model_dump())
    db.add(cat)
    await db.flush()
    await db.refresh(cat)
    return CategoryRead.model_validate(cat)


@router.get("/{cat_id}", response_model=CategoryRead)
async def get_category(cat_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Category).where(Category.id == cat_id))
    cat = r.scalar_one_or_none()
    if not cat:
        raise HTTPException(404, "Category not found")
    return CategoryRead.model_validate(cat)


@router.delete("/{cat_id}", status_code=204)
async def delete_category(cat_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Category).where(Category.id == cat_id))
    cat = r.scalar_one_or_none()
    if not cat:
        raise HTTPException(404, "Category not found")
    await db.delete(cat)
    return None
