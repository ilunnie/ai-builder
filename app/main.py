from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import routers

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

for route in routers:
    app.include_router(route)