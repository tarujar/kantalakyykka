from fastapi import FastAPI, Request, Depends
from fastapi_admin.app import FastAPIAdmin
from fastapi.responses import FileResponse, HTMLResponse
from fastapi_admin.depends import get_resources
from fastapi_admin.models import AbstractAdmin

from fastapi_admin.providers.login import UsernamePasswordProvider
from sqlalchemy.future import select
from database.database import SessionLocal
from redis import Redis
from app.models import User
from app.admin_models import (
    UserAdmin, GameTypeAdmin, PlayerAdmin, SeriesAdmin, SeriesRegistrationAdmin,
    TeamHistoryAdmin, GameAdmin, SingleThrowAdmin, SingleRoundThrowAdmin, Home
)
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

admin_app = FastAPIAdmin()
templates = Jinja2Templates(directory="templates")

class CustomUsernamePasswordProvider(UsernamePasswordProvider):
    async def get_admin_user(self, username: str, password: str):
        async with SessionLocal() as session:
            query = await session.execute(
                select(User).where(User.username == username)
            )
            user = query.scalar_one_or_none()
            if user and self.verify_password(password, user.hashed_password):
                return user
            return None

    async def create_admin_user(self, username: str, password: str, email: str):
        async with SessionLocal() as session:
            hashed_password = self.hash_password(password)
            new_user = User(username=username, email=email, hashed_password=hashed_password)
            session.add(new_user)
            await session.commit()
            return new_user

    async def register(self, app: FastAPIAdmin):
        # Override the register method to avoid using Tortoise ORM signals
        pass

async def init_admin(app: FastAPI):
    print("Initializing admin app...")
    redis = Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0))
    )  # Add Redis instance
    print(redis.ping()) 

    await admin_app.configure(
        logo_url="http://localhost:8000/favicon.ico",
        template_folders=[(os.path.join(os.path.dirname(__file__), "../templates"))],
        #template_folders=None,
        #providers=[
        #    CustomUsernamePasswordProvider(
        #        admin_model=User,  # Use the compatible User model
        #        login_logo_url="http://localhost:8000/favicon.ico"
        #    ),
        #],
        redis=redis,  # Pass Redis instance
    )

    class SimpleAdmin(AbstractAdmin):
        label="Simple"
        resource_name = "Simple"
        resource_label = "Simple Resource"

    admin_app.register(SimpleAdmin)

    # Register admin models and links
    admin_app.register(Home)
    admin_app.register(UserAdmin)
    admin_app.register(GameTypeAdmin)
    admin_app.register(PlayerAdmin)
    admin_app.register(SeriesAdmin)
    admin_app.register(SeriesRegistrationAdmin)
    admin_app.register(TeamHistoryAdmin)
    admin_app.register(GameAdmin)
    admin_app.register(SingleThrowAdmin)
    admin_app.register(SingleRoundThrowAdmin)
    
    print("Admin app initialized and mounted at /admin")
    app.mount("/admin", admin_app, name="admin")

    # Log the registered routes
    for route in app.routes:
        print(f"Registered route: {route.path}")

    # Log the admin app configuration
    print(f"Admin app configuration: {admin_app.openapi()}")
    print("Admin-sovelluksen reitit:")
    for route in admin_app.router.routes:
        print(f"Path: {route.path}, Name: {route.name}")
    print("Registered admin models:")
    for resource in admin_app.resources:
        print(f"Resource: {resource.label}")

