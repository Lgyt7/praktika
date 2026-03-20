from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import auth_router, tracks_router, playlists_router

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IndieSound API")

# Настройка CORS для Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В проде заменить на http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(tracks_router.router)
app.include_router(playlists_router.router)
