from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import api_router
from settings import APISettings

from fastapi.staticfiles import StaticFiles
import os


def get_app() -> FastAPI:
    fast_app = FastAPI(
        title=APISettings().APP_NAME,
        version=APISettings().APP_VERSION,
        debug=APISettings().IS_DEBUG
    )

    # Include all API routes
    fast_app.include_router(api_router, prefix=APISettings().API_PREFIX)

    # Add CORS middleware to allow frontend access
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fast_app

# Create FastAPI app instance
app = get_app()


# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
