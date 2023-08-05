from typing import List
from datetime import datetime
from pprint import pprint
from marshmallow import Schema, fields, INCLUDE
import numpy
import json


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
        ts = obj.timestamp.isoformat(timespec='milliseconds')
        if not obj.timestamp.tzinfo:
          ts+="+00"
        return ts

{
  "label":"x0f1",
  "_version":"0.16.2",
  "_variableOrderSymbols":"[\"x0\"]",
  "data":"{\"eliminated\":false,\"potentialused\":false,\"edgeIDs\":[],\"fnc\":{\"str\":\"FullNormal(\\ndim: 3\\nμ: [0.0, 0.0, 0.0]\\nΣ: [0.01 0.0 0.0; 0.0 0.01 0.0; 0.0 0.0 0.01]\\n)\\n\"},\"multihypo\":[],\"certainhypo\":[1],\"nullhypo\":0.0,\"solveInProgress\":0,\"inflation\":5.0}",
  "tags":"[\"FACTOR\"]",
  "timestamp":"2021-11-08T11:24:53.780-06:00",
  "nstime":"0",
  "fnctype":"PriorPose2",
  "solvable":1}


class Factor:
    schema: FactorSchema = FactorSchema()

    def __init__(self, 
            label: str, 
            fncType: str, 
            variableOrderSymbols: List[str], 
            tags: List[str] = ["FACTOR"], 
            # Why is this datastr and the prior is str?
            data: str = "{\"eliminated\":false,\"potentialused\":false,\"edgeIDs\":[],\"fnc\":{\"datastr\":\"FullNormal(\\ndim: 3\\nμ: [10.0, 0.0, 1.0471975511965976]\\nΣ: [0.010000000000000002 0.0 0.0; 0.0 0.010000000000000002 0.0; 0.0 0.0 0.010000000000000002]\\n)\\n\"},\"multihypo\":[],\"certainhypo\":[1,2],\"nullhypo\":0.0,\"solveInProgress\":0,\"inflation\":5.0}",
            timestamp: str = datetime.utcnow()):
        self.label = label
        self.variableOrderSymbols = variableOrderSymbols
        self.data = data
        self.tags = tags
        self.timestamp = timestamp
        self.nstime = "0"
        self.fnctype = fncType
        self.solvable = 1
        self._version ="0.16.2"

    def __repr__(self):
        return f"<Factor(label={self.label})>"

    def dump(self):
        return Factor.schema.dump(self)

    def dumps(self):
        return Factor.schema.dumps(self)


class FactorPrior(Factor):
  def __init__(self, 
            label: str, 
            fncType: str, 
            variableOrderSymbols: List[str], 
            tags: List[str] = ["FACTOR"], 
            # Why is this datastr and the prior is str?
            data: str = "{\"eliminated\":false,\"potentialused\":false,\"edgeIDs\":[],\"fnc\":{\"str\":\"FullNormal(\\ndim: 3\\nμ: [0.0, 0.0, 0.0]\\nΣ: [0.01 0.0 0.0; 0.0 0.01 0.0; 0.0 0.0 0.01]\\n)\\n\"},\"multihypo\":[],\"certainhypo\":[1],\"nullhypo\":0.0,\"solveInProgress\":0,\"inflation\":5.0}",
            timestamp: str = datetime.utcnow()):
        super().__init__(label, fncType, variableOrderSymbols, tags, data, timestamp)
