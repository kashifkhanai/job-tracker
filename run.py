import webbrowser
import threading
import time
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse  # ✅ Add this
from main import get_app

app = get_app()

# Mount frontend folder to serve static files
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")


# ✅ Redirect root ("/") to the register page
@app.get("/")
def root_redirect():
    return RedirectResponse(url="/static/register.html")


# ✅ Optional: Open browser automatically (only on local, not in Docker)
def open_browser():
    time.sleep(1)
    webbrowser.open_new("http://127.0.0.1:8000")


if __name__ == "__main__":
    if os.environ.get("DOCKER") != "true":  # Only open browser outside Docker
        threading.Thread(target=open_browser).start()

    import uvicorn
    uvicorn.run(
        "run:app",
        host="127.0.0.1",
        port=8000
    )
