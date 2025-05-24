from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger

from app.logger_conf import setup_logging
from app.router_users import router as router_users
from app.user.service import UserService



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting app")
    setup_logging()
    await UserService.add_users()
    yield
    logger.warning("Shutdown app")


app = FastAPI(
    lifespan=lifespan,
    title="Random user Service",
    description="Сервис для сбора случайных пользователей",
    version="0.1.0",
)

app.include_router(
    router=router_users,
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
