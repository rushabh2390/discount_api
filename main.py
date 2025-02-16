
from fastapi import FastAPI, Response
from users.routers.users import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import logging
logging.basicConfig(level=logging.DEBUG)


# App Object
app = FastAPI()
app.include_router(user_router, tags=["users"])
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=200)
async def read_root():
    return Response("server is up and running")
