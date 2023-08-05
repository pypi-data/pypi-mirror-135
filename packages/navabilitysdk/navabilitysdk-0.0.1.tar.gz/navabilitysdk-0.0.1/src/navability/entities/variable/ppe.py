from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, List

from marshmallow import EXCLUDE, Schema, fields

from navability.common.timestamps import TS_FORMAT


class PPESchema(Schema):
    solveKey = fields.Str(required=True)
    suggested = fields.List(fields.Float(), required=True)
    max = fields.List(fields.Float(), required=True)
    mean = fields.List(fields.Float(), required=True)
    lastUpdatedTimestamp = fields.Method(
        "get_lastupdated", attribute="lastUpdatedTimestamp", required=True
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE  # Note: This is because of _version, remote and fix later.

    def get_lastupdated(self, obj):
        # Return a robust timestamp
        print(obj)
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
    lastUpdatedTimestamp = fields.Method(
        "get_last_updated", "set_last_updated", required=True
    )

    def __repr__(self):
        return f"<PPE(solveKey={self.solveKey}, suggested={self.suggested})>"

    def get_last_updated(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "+00"
        return ts

    def set_timestamp(self, obj):
        return datetime.strptime(obj["formatted"], TS_FORMAT)

    def dump(self):
        return PPE.schema.dump(self)

    def dumps(self):
        return PPE.schema.dumps(self)
