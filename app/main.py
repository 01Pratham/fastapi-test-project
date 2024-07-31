from fastapi import FastAPI
import uvicorn

from core.db import Base, engine

from api.v1.router import Router as V1_Router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(V1_Router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
