from fastapi import FastAPI
from api.router import api_router
from settings import APISettings

def get_app() -> FastAPI:
    fast_app = FastAPI(title=APISettings().APP_NAME, version=APISettings().APP_VERSION, debug=APISettings().IS_DEBUG)
    fast_app.include_router(api_router, prefix=APISettings().API_PREFIX)

    return fast_app


app = get_app()



