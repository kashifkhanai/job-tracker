from db import MongoDB
from settings import get_settings

def get_db():
    settings = get_settings()
    return MongoDB(settings).db
