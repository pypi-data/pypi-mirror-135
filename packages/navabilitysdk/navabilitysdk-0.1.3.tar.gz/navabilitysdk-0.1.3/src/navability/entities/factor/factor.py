import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from marshmallow import EXCLUDE, Schema, fields, post_load

from navability.common.timestamps import TS_FORMAT
from navability.common.versions import payload_version


@dataclass()
class FactorSkeleton:
    label: str
    variableOrderSymbols: List[str]
    tags: List[str]

    def __repr__(self):
        return (
            f"<FactorSkeleton(label={self.label},"
            f"variableOrderSymbols={self.variableOrderSymbols},tags={self.tags})>"
        )

    def dump(self):
        return FactorSkeletonSchema().dump(self)

    def dumps(self):
        return FactorSkeletonSchema().dumps(self)

    @staticmethod
    def load(data):
        return FactorSkeletonSchema().load(data)


class FactorSkeletonSchema(Schema):
    label = fields.Str(required=True)
    variableOrderSymbols = fields.List(
        fields.Str(), data_key="_variableOrderSymbols", required=True
    )
    tags = fields.List(fields.Str(), required=True)

    class Meta:
        ordered = True

    @post_load
    def marshal(self, data, **kwargs):
        return FactorSkeleton(**data)


@dataclass()
class FactorSummary:
    label = str
    variableOrderSymbols: List[str]
    tags: List[str] = field(default_factory=lambda: ["FACTOR"])
    timestamp: datetime = datetime.utcnow()
    _version: str = payload_version

    def __repr__(self):
        return (
            f"<FactorSkeleton(label={self.label},"
            f"variableOrderSymbols={self.variableOrderSymbols},tags={self.tags})>"
        )

    def dump(self):
        return FactorSummarySchema().dump(self)

    def dumps(self):
        return FactorSummarySchema().dumps(self)

    @staticmethod
    def load(data):
        return FactorSummarySchema().load(data)


class FactorSummarySchema(Schema):
    label = fields.Str(required=True)
    variableOrderSymbols: fields.Str(data_key="_variableOrderSymbols", many=True)
    tags = fields.List(fields.Str(), required=True)
    timestamp = fields.Method("get_timestamp", "set_timestamp", required=True)
    _version = fields.Str(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE  # Note: This is because of _version, remote and fix later.

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "Z"
        return ts

    def set_timestamp(self, obj):
        # Have to be defensive here because it could be simply serialized
        # or it can be GQL data with formatted
        tsraw = obj if type(obj) == str else obj["formatted"]
        return datetime.strptime(tsraw, TS_FORMAT)

    @post_load
    def marshal(self, data, **kwargs):
        return FactorSummary(**data)


@dataclass()
class FactorData:
    fnc: Dict  # InferenceType  # {"datastr":"FullNormal(\\ndim: 3\\nμ: [10.0, 0.0, 1.0471975511965976]\\nΣ: [0.010000000000000002 0.0 0.0; 0.0 0.010000000000000002 0.0; 0.0 0.0 0.010000000000000002]\\n)\\n"}  # noqa: E501, B950
    eliminated: bool = False
    potentialused: bool = False
    edgeIDs: List[int] = field(default_factory=lambda: [])
    multihypo: List[int] = field(default_factory=lambda: [])
    certainhypo: List[int] = field(default_factory=lambda: [1, 2])
    nullhypo: float = 0
    solveInProgress: int = 0
    inflation: float = 5

    def dumps(self):
        return FactorDataSchema().dumps(self)

    def dump(self):
        return FactorDataSchema().dump(self)


class FactorDataSchema(Schema):
    eliminated = fields.Bool(required=True)
    potentialused = fields.Bool(required=True)
    edgeIDs = fields.List(fields.Int(), required=True)
    fnc = fields.Dict(
        required=True
    )  # fields.Method("get_fnc", "set_fnc", required=True)
    multihypo = fields.List(fields.Int(), required=True)
    certainhypo = fields.List(fields.Int(), required=True)
    nullhypo = fields.Float(required=True)
    solveInProgress = fields.Int(required=True)
    inflation = fields.Float(required=True)

    class Meta:
        ordered = True

    # def get_fnc(self, obj):
    #     # TODO: Switch this out to a real embedded object, no need for strings.
    #     return obj.fnc.dump()

    # def set_fnc(self, ob):
    #     raise Exception("Deserialization not supported yet.")

    @post_load
    def marshal(self, data, **kwargs):
        return FactorData(**data)


@dataclass()
class Factor:
    label: str
    fnctype: str
    variableOrderSymbols: List[str]
    data: FactorData  # '{"eliminated":false,"potentialused":false,"edgeIDs":[],"fnc":{"datastr":"FullNormal(\\ndim: 3\\nμ: [10.0, 0.0, 1.0471975511965976]\\nΣ: [0.010000000000000002 0.0 0.0; 0.0 0.010000000000000002 0.0; 0.0 0.0 0.010000000000000002]\\n)\\n"},"multihypo":[],"certainhypo":[1,2],"nullhypo":0.0,"solveInProgress":0,"inflation":5.0}'  # noqa: E501, B950
    tags: List[str] = field(default_factory=lambda: ["FACTOR"])
    timestamp: str = datetime.utcnow()
    nstime: int = 0
    solvable: str = 1
    _version: str = payload_version

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(label={self.label},"
            f"variables={self.variableOrderSymbols})>"
        )

    def dump(self):
        return FactorSchema().dump(self)

    def dumps(self):
        return FactorSchema().dumps(self)

    @staticmethod
    def load(data):
        return FactorSchema().load(data)


class FactorSchema(Schema):
    label = fields.Str(required=True)
    _version = fields.Str(required=True)
    _variableOrderSymbols = fields.Method("get_variableOrderSymbols", required=True)
    data = fields.Method("get_data", "set_data", required=True)
    tags = fields.List(fields.Str(), required=True)
    timestamp = fields.Method("get_timestamp", "set_timestamp", required=True)
    nstime = fields.Str(default="0")
    fnctype = fields.Str(required=True)
    solvable = fields.Int(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE  # Note: This is because of _version, remote and fix later.

    def get_variableOrderSymbols(self, obj):
        # TODO: Switch this out to a real embedded object, no need for strings.
        return json.dumps(obj.variableOrderSymbols)

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "Z"
        return ts

    def set_timestamp(self, obj):
        # Have to be defensive here because it could be simply serialized
        # or it can be GQL data with formatted
        tsraw = obj if type(obj) == str else obj["formatted"]
        return datetime.strptime(tsraw, TS_FORMAT)

    def get_data(self, obj):
        return obj.data.dumps()

    def set_data(self, ob):
        raise Exception("Deserialization not supported yet.")

    @post_load
    def marshal(self, data, **kwargs):
        return Factor(**data)
