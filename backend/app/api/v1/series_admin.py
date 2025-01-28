from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database.database import get_db
from app.services import game_types_service, series_service
from app.models.schemas import SeriesCreate

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/series/add", response_class=HTMLResponse)
async def add_series(request: Request, db: AsyncSession = Depends(get_db)):
    game_types = await game_types_service.list_game_types(db)
    return templates.TemplateResponse("add_series.html", {"request": request, "game_types": game_types})

@router.get("/series/edit/{series_id}", response_class=HTMLResponse)
async def edit_series(request: Request, series_id: int, db: AsyncSession = Depends(get_db)):
    series = await series_service.get_series(db, series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    game_types = await game_types_service.list_game_types(db)
    return templates.TemplateResponse("edit_series.html", {"request": request, "series": series, "game_types": game_types})

@router.post("/series/edit/{series_id}", response_class=HTMLResponse)
async def update_series(
    request: Request,
    series_id: int,
    name: str = Form(...),
    season_type: str = Form(...),
    year: int = Form(...),
    status: str = Form("upcoming"),
    registration_open: bool = Form(True),
    game_type_id: int = Form(...),
    is_cup_league: bool = Form(False),
    db: AsyncSession = Depends(get_db)
):
    series_data = SeriesCreate(
        name=name,
        season_type=season_type,
        year=year,
        status=status,
        registration_open=registration_open,
        game_type_id=game_type_id,
        is_cup_league=is_cup_league
    )
    try:
        updated_series = await series_service.update_series(db, series_id, series_data)
        if not updated_series:
            raise HTTPException(status_code=404, detail="Series not found")
        return templates.TemplateResponse("edit_series.html", {
            "request": request, 
            "series": updated_series, 
            "game_types": await game_types_service.list_game_types(db), 
            "success": True
        })
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Series with the same name and year already exists")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
