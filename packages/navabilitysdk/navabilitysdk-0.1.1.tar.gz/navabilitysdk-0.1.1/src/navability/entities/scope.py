from dataclasses import dataclass, field
from typing import List

from marshmallow import Schema, fields, post_load


@dataclass()
class Scope:
    environmentIds: List[str] = field(default_factory=lambda: [])
    userIds: List[str] = field(default_factory=lambda: [])
    robotIds: List[str] = field(default_factory=lambda: [])
    sessionIds: List[str] = field(default_factory=lambda: [])

    def dump(self):
        return ScopeSchema().dump(self)

    def dumps(self):
        return ScopeSchema().dumps(self)

    @staticmethod
    def load(data: str):
        return ScopeSchema().load(data)


class ScopeSchema(Schema):
    environmentIds = fields.String(many=True, default=[])
    userIds = fields.String(many=True, default=[])
    robotIds = fields.String(many=True, default=[])
    sessionIds = fields.String(many=True, default=[])

    class Meta:
        ordered = True

    @post_load
    def marshal(self, data, **kwargs):
        return Scope(**data)
