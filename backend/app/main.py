from fastapi import FastAPI, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from app.api.router import api_router
from database import init_db
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from random import choices
import os
from app.admin import init_admin
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import logging

load_dotenv()  # Load environment variables from .env file

max_age = 3600

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    await init_admin(app)
    yield  # Ensure the context manager yields control

app = FastAPI(lifespan=lifespan)  # Ensure the lifespan context manager is used

# Include the API router
app.include_router(api_router, prefix="/api/v1")

# CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    routes = [
        {"path": route.path, "name": route.name}
        for route in app.routes
        if not route.path.startswith("/openapi") and route.name not in ["swagger_ui_html", "swagger_ui_redirect", "redoc_html"]
    ]
    return {"routes": routes}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    favicon_path = os.path.join(os.path.dirname(__file__), "../static/favicon.svg")
    return FileResponse(favicon_path)

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    cookie_val = request.cookies.get("session")
    if cookie_val:
        request.scope['session'] = cookie_val
    else:
        request.scope['session'] = "".join(choices("asdasdqasdqqqq", k=128))
    response = await call_next(request)
    response.set_cookie("session", value=request.scope['session'],
                        max_age=max_age, httponly=True)
    return response

class PermissionFailedException(Exception):
    def __init__(self, permissions: list):
        self.permissions = permissions

def permission_failed_handler(request: Request, exc: PermissionFailedException):
    """shows an error page if the users authentication scope fails to meet the requirements"""
    return HTMLResponse(content=open("templates/permission_failed.html").read(), status_code=401)

app.add_exception_handler(PermissionFailedException, permission_failed_handler)

# Ensure the app instance is correctly defined
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Read the port from environment variables
    uvicorn.run(app, host="0.0.0.0", port=port)