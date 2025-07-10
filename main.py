from fastapi import FastAPI
from db import MongoDB
from settings import get_settings

app = FastAPI()

@app.get("/")
async def read_root():
    settings = get_settings()
    db = MongoDB(settings)
    collections = await db.list_collection_names()
    return {"message": "Connected to MongoDB!", "collections": collections}
