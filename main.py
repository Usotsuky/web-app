from fastapi import FastAPI, Path
from enum import Enum
from typing import Annotated
import uvicorn

from core.config import settings
from users.views import router as users_router
from contextlib import asynccontextmanager
from core.db import Base, db_helper
from api_v1 import router as router_v1


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"hello": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: Annotated[int, Path(ge=0)]):
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def read_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


if "__main__" == __name__:
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
