from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
import sys
from pathlib import Path
from starlette import status
from fastapi.middleware.cors import CORSMiddleware


if __name__ == "__main__" and __package__ is None:
    print("Please run: python -m app.main")
    exit()

sys.path.append(str(Path(__file__).resolve().parent))

from core.db import Base, engine
from utils.response import Response
from api.v1.router import Router as V1_Router

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000", "http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins       ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(V1_Router, prefix="/api/v1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        error_messages = []
        for error in exc.errors():
            field = ".".join(error["loc"])
            field = field.replace("body.", "")
            if "field required" in error["msg"]:
                message = f"The '{field}' field is required"
            else:
                message = error["msg"]
            error_messages.append({"field": field, "message": message})

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "data validation failed", "errors": error_messages},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Response Failed", "errors": str(e)},
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
