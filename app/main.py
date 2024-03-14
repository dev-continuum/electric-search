import time

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app import app_settings, get_logger
from app.search.route import router as search_router

settings = app_settings()

origins = ["*"]

logger = get_logger(name="app.main")

app = FastAPI(
    title=settings.app_name,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def authenticate(request: Request, call_nxt):
    req_start_time = time.time()
    response = await call_nxt(request)
    req_elapsed_time = time.time() - req_start_time
    response.headers["x-elapsed-time"] = str(req_elapsed_time)
    return response


# Registering API Routers.
app.include_router(search_router)


@app.on_event("startup")
def on_start():
    logger.info("Starting API.")


@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
