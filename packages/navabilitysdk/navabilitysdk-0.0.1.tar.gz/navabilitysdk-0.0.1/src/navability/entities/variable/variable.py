import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List

from marshmallow import EXCLUDE, Schema, fields, post_load

from navability.common.timestamps import TS_FORMAT
from navability.common.versions import payload_version
from navability.entities.variable.ppe import PPE, PPESchema
from navability.entities.variable.variablenodedata import (
    VariableNodeData,
    VariableNodeDataSchema,
)


class VariableType(Enum):
    POINT2 = "RoME.Point2"
    POSE2 = "RoME.Pose2"


@dataclass()
class VariableSkeleton:
    label: str
    tags: List[str] = field(default_factory=lambda: ["VARIABLE"])

    def __repr__(self):
        return f"<VariableSkeleton(label={self.label})>"

    def dump(self):
        return VariableSkeletonSchema().dump(self)

    def dumps(self):
        return VariableSkeletonSchema().dumps(self)

    @staticmethod
    def load(data):
        return VariableSkeletonSchema().load(data)


class VariableSkeletonSchema(Schema):
    label = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE  # Note: This is because of _version, remote and fix later.

    @post_load
    def load(self, data, **kwargs):
        return VariableSkeleton(**data)


@dataclass()
class VariableSummary(VariableSkeleton):
    variableType: VariableType = VariableType.POSE2
    ppes: Dict[str, PPE] = field(default_factory=lambda: {})
    timestamp: datetime = datetime.utcnow()
    _version: str = payload_version
    _id: int = None

    def __repr__(self):
        return f"<VariableSummary(label={self.label},variableType={self.variableType})>"

    def dump(self):
        return VariableSummarySchema().dump(self)

    def dumps(self):
        return VariableSummarySchema().dumps(self)

    @staticmethod
    def load(data):
        return VariableSummarySchema().load(data)


class VariableSummarySchema(Schema):
    label = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=True)
    ppes = fields.Nested(PPESchema, many=True)
    timestamp = fields.Method("get_timestamp", "set_timestamp", required=True)
    variableType = fields.Str(required=True)
    _version = fields.Str(required=True)
    _id: fields.Integer(data_key="_id", required=False)

    class Meta:
        ordered = True
        unknown = EXCLUDE  # Note: This is because of _version, remote and fix later.

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "+00"
        return ts

    def set_timestamp(self, obj):
        return datetime.strptime(obj["formatted"], TS_FORMAT)

    @post_load
    def load(self, data, **kwargs):
        return VariableSummary(**data)


@dataclass()
class Variable(VariableSummary):
    dataEntry: str = "{}"
    dataEntryType: str = "{}"
    solverData: Dict[str, VariableNodeData] = field(default_factory=lambda: {})
    smallData: str = "{}"
    solvable: str = 1

    def __post_init__(self):
        if self.solverData == {}:
            self.solverData["default"] = VariableNodeData(self.variableType)

    def __repr__(self):
        return f"<Variable(label={self.label},variableType={self.variableType})>"

    def dump(self):
        return VariableSchema().dump(self)

    def dumpPacked(self):
        return PackedVariableSchema().dump(self)

    def dumps(self):
        return VariableSchema().dumps(self)

    def dumpsPacked(self):
        return PackedVariableSchema().dumps(self)

    @staticmethod
    def load(data):
        return VariableSchema().load(data)


class VariableSchema(Schema):
    label = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=True)
    ppes = fields.Nested(PPESchema, many=True)
    timestamp = fields.Method("get_timestamp", "set_timestamp", required=True)
    variableType = fields.Str(required=True)
    _version = fields.Str(required=True)
    _id: fields.Integer(data_key="_id", required=False)
    # dataEntry = fields.Str(required=True)
    # dataEntryType = fields.Str(required=True)
    solverData = fields.Nested(VariableNodeDataSchema, many=True)
    smallData = fields.Str(required=True)
    solvable = fields.Int(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE  # Note: This is because of _id, remote and fix later.

    @post_load
    def marshal(self, data, **kwargs):
        return Variable(**data)

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "+00"
        return ts

    def set_timestamp(self, obj):
        return datetime.strptime(obj["formatted"], TS_FORMAT)


class PackedVariableSchema(Schema):
    """
    A special schema for the addVariable call, which is used to
    form a packed variable struct.
    """

    label = fields.Str(required=True)
    dataEntry = fields.Str(required=True)
    nstime = fields.Str(required=True)
    variableType = fields.Str(required=True)
    dataEntryType = fields.Str(required=True)
    ppeDict = fields.Str(attribute="ppes", required=True)
    solverDataDict = fields.Method("get_solver_data_dict", required=True)
    smallData = fields.Str(required=True)
    solvable = fields.Int(required=True)
    tags = fields.List(fields.Str(), required=True)
    timestamp = fields.Method("get_timestamp", required=True)
    _version = fields.Str(required=True)

    class Meta:
        ordered = True

    def get_solver_data_dict(self, obj):
        # TODO: Switch this out to a real embedded object, no need for strings.
        schema = VariableNodeDataSchema()
        vnds = {
            solverKey: schema.dump(vnd) for solverKey, vnd in obj.solverData.items()
        }
        return json.dumps(vnds)

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "+00"
        return ts
