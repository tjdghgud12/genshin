import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
from contextlib import asynccontextmanager
from services.ambrApi import initAmbrApi, closeAmbrApi


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await initAmbrApi()
        print("✅ AmbrAPI Initialized")
        yield
    finally:
        await closeAmbrApi()
        print("🛑 AmbrAPI Closed")


app = FastAPI(lifespan=lifespan)

origins = [
    url
    for url in [
        os.getenv("DEV_FRONTEND_URL"),
        os.getenv("FRONTEND_URL"),
    ]
    if url is not None
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
