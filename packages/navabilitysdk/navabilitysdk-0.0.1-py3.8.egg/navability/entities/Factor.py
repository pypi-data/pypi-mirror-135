import json
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, List

from marshmallow import Schema, fields

from src.navability.common.versions import payload_version


class FactorSchema(Schema):
    label = fields.Str(required=True)
    _variableOrderSymbols = fields.Method("get_variableOrderSymbols", required=True)
    data = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=True)
    timestamp = fields.Method("get_timestamp", required=True)
    nstime = fields.Str(required=True)
    fnctype = fields.Str(required=True)
    solvable = fields.Int(required=True)
    _version = fields.Str(required=True)

    class Meta:
        ordered = True

    def get_variableOrderSymbols(self, obj):
        # TODO: Switch this out to a real embedded object, no need for strings.
        return json.dumps(obj.variableOrderSymbols)

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "+00"
        return ts


@dataclass()
class Factor:
    schema: ClassVar[FactorSchema] = FactorSchema()
    label: str
    fnctype: str
    variableOrderSymbols: List[str]
    tags: List[str] = ["FACTOR"]
    data: str = '{"eliminated":false,"potentialused":false,"edgeIDs":[],"fnc":{"datastr":"FullNormal(\\ndim: 3\\nμ: [10.0, 0.0, 1.0471975511965976]\\nΣ: [0.010000000000000002 0.0 0.0; 0.0 0.010000000000000002 0.0; 0.0 0.0 0.010000000000000002]\\n)\\n"},"multihypo":[],"certainhypo":[1,2],"nullhypo":0.0,"solveInProgress":0,"inflation":5.0}'  # noqa: E501, B950
    timestamp: str = datetime.utcnow()
    # nstime: str = "0"
    solvable: str = 1
    _version: str = payload_version

    def __repr__(self):
        return f"<Factor(label={self.label})>"

    def dump(self):
        return Factor.schema.dump(self)

    def dumps(self):
        return Factor.schema.dumps(self)


@dataclass()
class FactorPrior(Factor):
    data: str = '{"eliminated":false,"potentialused":false,"edgeIDs":[],"fnc":{"datastr":"FullNormal(\\ndim: 3\\nμ: [10.0, 0.0, 1.0471975511965976]\\nΣ: [0.010000000000000002 0.0 0.0; 0.0 0.010000000000000002 0.0; 0.0 0.0 0.010000000000000002]\\n)\\n"},"multihypo":[],"certainhypo":[1,2],"nullhypo":0.0,"solveInProgress":0,"inflation":5.0}'  # noqa: E501, B950
