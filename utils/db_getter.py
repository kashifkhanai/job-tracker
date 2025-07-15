from db import MongoDB
from settings import get_settings
#Get and return MongoDB database
def get_db():
    settings = get_settings()
    return MongoDB(settings).db
