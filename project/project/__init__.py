import asyncio
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

from uvicorn import run


app = FastAPI()

logging.basicConfig(
    filename="debug.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


@app.get("/", response_model=dict)
async def index():
    await asyncio.sleep(0.5)
    return {"Hello": "World"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):

    start_time = time.perf_counter_ns()
    response = await call_next(request)
    process_time = time.perf_counter_ns() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logging.info(
        f"Request {request.method} {request.url} took {process_time// 1_000_000} miliseconds"
    )
    return response


def main():
    run(app, host="localhost", port=7000)
