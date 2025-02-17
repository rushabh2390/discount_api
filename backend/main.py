
from fastapi import FastAPI, Response, HTTPException
from users.routers.users import router as user_router
from items.routers.items import router as item_router
from orders.routers.orders import router as order_router
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import logging
logging.basicConfig(level=logging.DEBUG)


# App Object
app = FastAPI()
app.include_router(user_router, tags=["users"])
app.include_router(item_router, tags=["items"])
app.include_router(order_router, tags=["orders"])
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

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return {"error": exc.detail}