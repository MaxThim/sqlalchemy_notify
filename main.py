from fastapi import FastAPI
from contextlib import asynccontextmanager
from simple_object.router import router as simple_object_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    yield
    print("shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(simple_object_router)