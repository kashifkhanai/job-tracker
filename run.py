# run.py
import webbrowser
import threading
import time
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from main import get_app

app = get_app()

# Mount frontend folder
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Auto open register page
def open_browser():
    time.sleep(1)
    webbrowser.open_new("http://127.0.0.1:8000/register.html")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()

    import uvicorn
    uvicorn.run(
        "run:app",  # 🟢 This is the fix
        host="127.0.0.1",
        port=8000,
        reload=True
    )
