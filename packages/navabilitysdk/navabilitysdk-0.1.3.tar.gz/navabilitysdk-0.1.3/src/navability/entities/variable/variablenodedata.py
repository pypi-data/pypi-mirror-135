from dataclasses import dataclass, field
from typing import List

import numpy
from marshmallow import EXCLUDE, Schema, fields, post_load

from navability.common.versions import payload_version


@dataclass()
class VariableNodeData:
    variableType: str
    vecval: List[float] = field(default_factory=lambda: list(numpy.zeros(3 * 100)))
    dimval: int = 3
    vecbw: List[float] = field(default_factory=lambda: list(numpy.zeros(3)))
    dimbw: int = 3
    BayesNetOutVertIDs: List[int] = field(default_factory=list)
    dimIDs: List[int] = field(default_factory=lambda: [0, 1, 2])
    dims: int = 3
    eliminated: bool = False
    BayesNetVertID: str = "_null"
    separator: List[int] = field(default_factory=list)
    initialized: bool = False
    infoPerCoord: List[int] = field(default_factory=lambda: list(numpy.zeros(3)))
    ismargin: bool = False
    dontmargin: bool = False
    solveInProgress: int = 0
    solvedCount: int = 0
    solveKey: str = "default"
    _version: str = payload_version

    def __repr__(self):
        return f"<VariableNodeData(solveKey={self.solveKey})>"

    def dump(self):
        return VariableNodeDataSchema().dump(self)

    def dumps(self):
        return VariableNodeDataSchema().dumps(self)

    @staticmethod
    def load(data):
        return VariableNodeDataSchema().load(data)


class VariableNodeDataSchema(Schema):
    vecval = fields.List(fields.Float(), required=True)  # numpy.zeros(3*100) # 300
    dimval = fields.Integer(required=True)  # 3
    vecbw = fields.List(fields.Float(), required=True)  # numpy.zeros(3)
    dimbw = fields.Integer(required=True)  # 3
    BayesNetOutVertIDs = fields.List(fields.Integer(), required=True)  # []
    dimIDs = fields.List(fields.Integer(), required=True)  # [0,1,2]
    dims = fields.Integer(required=True)  # 3
    eliminated = fields.Boolean(required=True)  # False
    BayesNetVertID = fields.Str(required=True)  # "_null"
    separator = fields.List(fields.Integer(), required=True)  # []
    variableType = fields.Str(required=True)  # type
    initialized = fields.Boolean(required=True)  # False
    infoPerCoord = fields.List(fields.Float(), required=True)  # numpy.zeros(3)
    ismargin = fields.Boolean(required=True)  # False
    dontmargin = fields.Boolean(required=True)  # False
    solveInProgress = fields.Integer(required=True)  # 0
    solvedCount = fields.Integer(required=True)  # 0
    solveKey = fields.Str(required=True)  # solveKey
    _version: fields.Str(data_key="_version", required=False)

    class Meta:
        ordered = True
        unknown = EXCLUDE  # Note: This is because of _version, remote and fix later.

    @post_load
    def marshal(self, data, **kwargs):
        return VariableNodeData(**data)
