from __future__ import annotations

from tortoise import fields
from tortoise.models import Model


class Todo(Model):
    tid = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    task = fields.TextField()
    complete = fields.BooleanField(default=False)
