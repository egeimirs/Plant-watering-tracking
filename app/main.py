import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, plants, waterings, stats

app = FastAPI(title="PlantCare — учёт полива растений", version="1.0.0")
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("PLANTCARE_SECRET", "plantcare-dev-key-change-before-deploy"), same_site="lax", https_only=False)
app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(waterings.router)
app.include_router(stats.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get("/login")
def login_page():
    return FileResponse("static/login.html")

@app.get("/register")
def register_page():
    return FileResponse("static/register.html")
