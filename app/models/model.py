import asyncio
from uuid import uuid4
from time import time

from tortoise import fields
from tortoise.functions import Count

from app.models import BaseModel
from tortoise.models import Model

from app.util import Util
from app.mapping import CodeStatus


class TestModel(BaseModel):
    '''
    测试表
    '''

    class Meta:
        table = "test"

    age = fields.IntField()
    description = fields.CharField(200, default="")
    name = fields.CharField(40, default="")
