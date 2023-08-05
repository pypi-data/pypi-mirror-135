from dataclasses import dataclass
from typing import ClassVar, List

import numpy
from marshmallow import Schema, fields


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

    class Meta:
        ordered = True


@dataclass()
class VariableNodeData:
    variableType: str
    schema: ClassVar[VariableNodeDataSchema] = VariableNodeDataSchema()
    vecval: List[float] = list(numpy.zeros(3 * 100))
    dimval: int = 3
    vecbw: List[float] = list(numpy.zeros(3))
    dimbw: int = 3
    BayesNetOutVertIDs: List[int] = []
    dimIDs: List[int] = [0, 1, 2]
    dims: int = 3
    eliminated: bool = False
    BayesNetVertID: str = "_null"
    separator: List[int] = []
    initialized: bool = False
    infoPerCoord: List[int] = list(numpy.zeros(3))
    ismargin: bool = False
    dontmargin: bool = False
    solveInProgress: int = 0
    solvedCount: int = 0
    solveKey: str = "default"

    def __repr__(self):
        return f"<VariableNodeData(solveKey={self.solveKey})>"

    def dump(self):
        return VariableNodeData.schema.dump(self)

    def dumps(self):
        return VariableNodeData.schema.dumps(self)
