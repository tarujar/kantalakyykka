from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.schemas import PlayerCreate
from ..models.models import Player

async def create_player(db: AsyncSession, player: PlayerCreate) -> Player:
    db_player = Player(**player.model_dump())
    db.add(db_player)
    await db.commit()
    await db.refresh(db_player)
    return db_player

async def get_player(db: AsyncSession, player_id: int) -> Player:
    result = await db.execute(select(Player).filter(Player.id == player_id))
    return result.scalars().first()

async def list_players(db: AsyncSession) -> list[Player]:
    result = await db.execute(select(Player))
    return result.scalars().all()

async def update_player(db: AsyncSession, player_id: int, player: PlayerCreate) -> Player:
    result = await db.execute(select(Player).filter(Player.id == player_id))
    db_player = result.scalars().first()
    if db_player:
        for key, value in player.dict().items():
            setattr(db_player, key, value)
        await db.commit()
        await db.refresh(db_player)
    return db_player

async def delete_player(db: AsyncSession, player_id: int) -> bool:
    result = await db.execute(select(Player).filter(Player.id == player_id))
    db_player = result.scalars().first()
    if db_player:
        await db.delete(db_player)
        await db.commit()
        return True
    return False
