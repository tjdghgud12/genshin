from fastapi import FastAPI
from api import router


test = "dasdsa"

app = FastAPI()



app.include_router(router, prefix="/api")
