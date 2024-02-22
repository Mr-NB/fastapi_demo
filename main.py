import os

import aiohttp as aiohttp
import uvicorn
import aioredis
import logging, logging.config, os
from tortoise.contrib.fastapi import register_tortoise

from app import app
from app.routes import router


@app.on_event("startup")
async def startup_event():
    time_zone = os.getenv("TIMEZONE", "Asia/Shanghai")
    coon = aiohttp.TCPConnector(ssl=False)
    session = aiohttp.ClientSession(connector=coon, trust_env=True)
    app.Session = session
    # redis
    # app.redis = await aioredis.create_redis_pool(os.getenv("REDIS", 'redis://ip:port'), encoding="utf-8")

    # mysql orm
    # register_tortoise(
    #     app, generate_schemas=True, config={
    #         'connections': {
    #             'default': os.getenv("MYSQL", "mysql://username:password@ip:port/db")
    #         },
    #         'apps': {
    #             "models": {'models': ['app.models.model'],
    #                        'default_connection': 'default'}
    #
    #         },
    #         'use_tz': False,
    #         'timezone': time_zone
    #     }
    #
    # )


@app.on_event("shutdown")
async def shutdown_event():
    await app.Session.close()
    # await app.redis.wait_closed()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
