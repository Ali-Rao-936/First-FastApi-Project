from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.models import chat_message, product, user  # noqa: F401 — registers models with Base.metadata
from app.routes.agent import router as agent_router
from app.routes.auth import router as auth_router
from app.routes.products import router as products_router

app = FastAPI(title="FastAPI Practice")

Base.metadata.create_all(bind=engine)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
        headers=getattr(exc, "headers", None),
    )


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(agent_router, prefix="/agent", tags=["Agent"])


@app.get("/")
def greet():
    return {"message": "Hello, World!"}
