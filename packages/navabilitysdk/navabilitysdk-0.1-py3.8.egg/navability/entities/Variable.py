from typing import List
from datetime import datetime
from pprint import pprint
from marshmallow import Schema, fields, INCLUDE
import numpy
import json

class VariableNodeDataSchema(Schema):
    vecval = fields.List(fields.Float(), required=True) # numpy.zeros(3*100) # 300 
    dimval = fields.Integer(required=True) # 3
    vecbw = fields.List(fields.Float(), required=True) # numpy.zeros(3)
    dimbw = fields.Integer(required=True) # 3
    BayesNetOutVertIDs = fields.List(fields.Integer(), required=True) # []
    dimIDs = fields.List(fields.Integer(), required=True) # [0,1,2]
    dims = fields.Integer(required=True) # 3
    eliminated = fields.Boolean(required=True) # False
    BayesNetVertID = fields.Str(required=True) # "_null"
    separator = fields.List(fields.Integer(), required=True) # []
    variableType = fields.Str(required=True) # type
    initialized = fields.Boolean(required=True) # False
    infoPerCoord = fields.List(fields.Float(), required=True) # numpy.zeros(3)
    ismargin = fields.Boolean(required=True) # False
    dontmargin = fields.Boolean(required=True) # False
    solveInProgress = fields.Integer(required=True) # 0
    solvedCount = fields.Integer(required=True) # 0
    solveKey = fields.Str(required=True) # solveKey

    class Meta:
        ordered = True

class VariableNodeData:
    schema: VariableNodeDataSchema = VariableNodeDataSchema()

    def __init__(self,
            type:str,
            solveKey:str = "default" 
            ):
        self.vecval = list(numpy.zeros(3*100)) # 300 
        self.dimval = 3
        self.vecbw = list(numpy.zeros(3))
        self.dimbw = 3
        self.BayesNetOutVertIDs = []
        self.dimIDs = [0,1,2]
        self.dims = 3
        self.eliminated = False
        self.BayesNetVertID = "_null"
        self.separator = []
        self.variableType = type
        self.initialized = False
        self.infoPerCoord = list(numpy.zeros(3))
        self.ismargin = False
        self.dontmargin = False
        self.solveInProgress = 0
        self.solvedCount = 0
        self.solveKey = solveKey

    def __repr__(self):
        return f"<VariableNodeData(solveKey={self.solveKey})>"

    def dump(self):
        return VariableNodeData.schema.dump(self)

    def dumps(self):
        return VariableNodeData.schema.dumps(self)

    
class VariableSchema(Schema):
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
        vnds = {solverKey:schema.dump(vnd) for solverKey,vnd in obj.solverDataDict.items()}
        return json.dumps(vnds)

    def get_timestamp(self, obj):
        # Return a robust timestamp
        ts = obj.timestamp.isoformat(timespec='milliseconds')
        if not obj.timestamp.tzinfo:
          ts+="+00"
        return ts


class Variable:
    schema: VariableSchema = VariableSchema()

    def __init__(self, 
            label: str, 
            type: str, 
            tags: List[str] = ["VARIABLE"], 
            timestamp: datetime = datetime.utcnow()):
        self.label = label
        self.dataEntry = "{}"
        self.nstime = "0"
        self.variableType = type
        self.dataEntryType = "{}"
        self.ppeDict = "{}"
        self.solverDataDict = {
            "default": VariableNodeData(type)
         } 
        self.smallData = "{}"
        self.solvable = 1
        self.tags = tags
        self.timestamp = timestamp
        self._version = "0.16.2"      

    def __repr__(self):
        return f"<Variable(label={self.label})>"

    def dump(self):
        return Variable.schema.dump(self)

    def dumps(self):
        return Variable.schema.dumps(self)
