from fastapi import APIRouter
from api import auth_routes,admin_routes,job_routes

api_router = APIRouter()

# Register routes with tags and prefixes
api_router.include_router(router=auth_routes.router, tags=["Authentication"], prefix="")
api_router.include_router(router=admin_routes.router, tags=["Adminstration"], prefix="")
api_router.include_router(router=job_routes.router,tags=["User"],prefix="")


