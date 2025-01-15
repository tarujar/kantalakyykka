from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..models import GameType as GameTypeModel, GameTypeCreate

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
