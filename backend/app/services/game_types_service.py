from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..models.models import GameType as GameTypeModel  # Update this import
from ..models.schemas import GameTypeCreate

async def create_game_type(db: AsyncSession, game_type: GameTypeCreate) -> GameTypeModel:
    db_game_type = GameTypeModel(**game_type.model_dump())
    db.add(db_game_type)
    await db.commit()
    await db.refresh(db_game_type)
    return db_game_type

async def get_game_type(db: AsyncSession, game_type_id: int) -> GameTypeModel:
    result = await db.execute(
        select(GameTypeModel).filter(GameTypeModel.id == game_type_id)
    )
    return result.scalar_one_or_none()

async def list_game_types(db: AsyncSession) -> List[GameTypeModel]:
    result = await db.execute(select(GameTypeModel))
    return result.scalars().all()

async def update_game_type(db: AsyncSession, game_type_id: int, game_type: GameTypeCreate) -> GameTypeModel:
    db_game_type = await get_game_type(db, game_type_id)
    if db_game_type is None:
        return None
    for key, value in game_type.model_dump().items():
        setattr(db_game_type, key, value)
    await db.commit()
    await db.refresh(db_game_type)
    return db_game_type

async def delete_game_type(db: AsyncSession, game_type_id: int) -> bool:
    db_game_type = await get_game_type(db, game_type_id)
    if db_game_type is None:
        return False
    await db.delete(db_game_type)
    await db.commit()
    return True
