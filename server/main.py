from fastapi import FastAPI
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

app.include_router(router, prefix="/api")
