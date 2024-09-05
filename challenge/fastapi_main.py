import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from challenge.background_tasks.iss_position_updater import IssPositionUpdater
from challenge.routers import iss_router
from challenge.utils.fastapi.fastapi_utils import set_up_db, get_lifespan_db, limiter, \
    get_config_utils

logger = logging.getLogger(__name__)
config_utils = get_config_utils()


# Here in case we want to cancel it at some point
# iss_updater_task = None

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI, db=get_lifespan_db()):
    """
    It starts the schedule that saves the latest IssPosition at configured intervals
    :param fastapi_app: the FastAPI app
    :param db: the DB
    """
    iss_position_updater = IssPositionUpdater(db=db, config_utils=config_utils)
    iss_updater_task = asyncio.create_task(iss_position_updater.run_iss_update_position_schedule())
    logger.debug("Started ISS Update Position Schedule")
    yield
    iss_updater_task.cancel()


def set_up_fastapi():
    set_up_db()
    fastapi_app = FastAPI(lifespan=lifespan)
    fastapi_app.include_router(iss_router.router)
    limiter.enabled = config_utils.get_limits_enabled()
    fastapi_app.state.limiter = limiter
    fastapi_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    return fastapi_app


app = set_up_fastapi()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@limiter.limit("10/minute")
async def read_main(request: Request):
    return {"message": "Welcome to the ISS Tracker challenge!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
