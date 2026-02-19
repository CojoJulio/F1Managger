from fastapi import FastAPI
from api import race
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="F1 Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(race.router, prefix="/race")
