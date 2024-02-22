from typing import List

import asyncio, requests
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional

from app import app
from app.lib import Lib
from app.util import Util
from app.mapping import CodeStatus

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}, 401: {"description": "Unauthorized"},
               403: {"description": "Forbidden"}, 200: {"description": "Success"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginBody(BaseModel):
    username: str
    password: str


class PostBody(BaseModel):
    str_demo: str = Field("", example="字符类型")
    int_demo: Optional[int] = Field(0, example="整型")
    dict_demo: Optional[dict] = Field(None, example="字典")


@app.get("/test_get")
async def test_get():
    return Util.format_Resp(message="Successfully obtained")


@app.post("/test_post")
async def test_post(body: PostBody):
    return Util.format_Resp(data=dict(body), message="Added successfully")


@app.put("/test_put")
async def test_put(body: PostBody):
    return Util.format_Resp(data=dict(body), message="Modified successfully")


@app.delete("/test_delete")
async def test_delete(id: int):
    return Util.format_Resp(data=id, message="Delete successfully")
