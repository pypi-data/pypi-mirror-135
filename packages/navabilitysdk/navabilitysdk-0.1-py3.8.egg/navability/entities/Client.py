from typing import List
from datetime import datetime
from pprint import pprint
from marshmallow import Schema, fields, INCLUDE

class ClientSchema(Schema):
    userId = fields.String(required=True)  
    robotId = fields.String(required=True)
    sessionId = fields.String(required=True)

    class Meta:
        ordered = True


class Client:
    schema: ClientSchema = ClientSchema()

    def __init__(self,
            userId: str,
            robotId: str,
            sessionId: str 
            ):
        self.userId = userId 
        self.robotId = robotId
        self.sessionId = sessionId

    def __repr__(self):
        return f"<Client(userId={self.userId}, robotId={self.robotId}, sessionId={self.sessionId})>"

    def dump(self):
        return Client.schema.dump(self)

    def dumps(self):
        return Client.schema.dumps(self)
