from fastapi import APIRouter
from api import routes,admin_routes

api_router = APIRouter()

# Register routes with tags and prefixes
api_router.include_router(router=routes.router, tags=["Authentication"], prefix="")
api_router.include_router(router=admin_routes.router, tags=["Adminstration"], prefix="")


