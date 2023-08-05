from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, List

from marshmallow import Schema, fields


class PPESchema(Schema):
    solveKey = fields.Str(required=True)
    suggested = fields.List(fields.Float(), required=True)
    max = fields.List(fields.Float(), required=True)
    mean = fields.List(fields.Float(), required=True)
    lastUpdatedTimestamp = fields.Method("get_lastupdated", required=True)

    class Meta:
        ordered = True

    def get_lastupdated(self, obj):
        # Return a robust timestamp
        ts = obj.lastUpdatedTimestamp.isoformat(timespec="milliseconds")
        if not obj.lastUpdatedTimestamp.tzinfo:
            ts += "+00"
        return ts


@dataclass()
class PPE:
    solveKey: str
    suggested: List[float]
    max: List[float]
    mean: List[float]
    schema: ClassVar[PPESchema] = PPESchema()
    lastUpdatedTimestamp: datetime = datetime.utcnow()

    def __repr__(self):
        return f"<PPE(solveKey={self.solveKey}, suggested={self.suggested})>"

    def dump(self):
        return PPE.schema.dump(self)

    def dumps(self):
        return PPE.schema.dumps(self)
