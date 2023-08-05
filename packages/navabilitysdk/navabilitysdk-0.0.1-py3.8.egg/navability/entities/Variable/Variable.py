import json
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Dict, List

from marshmallow import Schema, fields

from navability.entities.Variable.PPE import PPE, PPESchema
from navability.entities.Variable.VariableNodeData import (
    VariableNodeData,
    VariableNodeDataSchema,
)
from src.navability.common.versions import payload_version


class VariableSkeletonSchema(Schema):
    label = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=True)

    class Meta:
        ordered = True


class VariableSummarySchema(VariableSkeletonSchema):
    ppes = fields.Nested(PPESchema, many=True)
    timestamp = fields.Method("get_timestamp", required=True)
    variableType = fields.Str(required=True)
    _version = fields.Str(required=True)

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "+00"
        return ts


class VariableSchema(VariableSummarySchema):
    # dataEntry = fields.Str(required=True)
    # dataEntryType = fields.Str(required=True)
    solverData = fields.Nested(VariableNodeDataSchema, many=True)
    smallData = fields.Str(required=True)
    solvable = fields.Int(required=True)


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
    ppeDict = fields.Str(required=True)
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
            solverKey: schema.dump(vnd) for solverKey, vnd in obj.solverDataDict.items()
        }
        return json.dumps(vnds)

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec="milliseconds")
        if not obj.timestamp.tzinfo:
            ts += "+00"
        return ts


@dataclass()
class VariableSkeleton:
    schema: ClassVar[VariableSkeletonSchema] = VariableSkeletonSchema()
    label: str
    tags: List[str] = ["VARIABLE"]


@dataclass()
class VariableSummary(VariableSkeleton):
    schema: ClassVar[VariableSummarySchema] = VariableSummarySchema()
    variableType: str = "Pose2"
    ppeDict: Dict[str, PPE] = {}
    timestamp: datetime = datetime.utcnow()
    _version: str = payload_version


@dataclass()
class Variable(VariableSummary):
    schema: ClassVar[VariableSchema] = VariableSchema()
    packedSchema: ClassVar[PackedVariableSchema] = PackedVariableSchema()
    dataEntry: str = "{}"
    dataEntryType: str = "{}"
    solverDataDict: Dict[str, VariableNodeData] = {"default": VariableNodeData(type)}
    smallData: str = "{}"
    solvable: str = 1

    def __repr__(self):
        return f"<Variable(label={self.label})>"

    def dump(self):
        return Variable.schema.dump(self)

    def dumpPacked(self):
        return Variable.packedSchema.dump(self)

    def dumps(self):
        return Variable.schema.dumps(self)

    def dumpsPacked(self):
        return Variable.packedSchema.dumps(self)
