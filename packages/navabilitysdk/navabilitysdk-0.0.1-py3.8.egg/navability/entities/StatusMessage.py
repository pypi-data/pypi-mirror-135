from datetime import datetime

from marshmallow import Schema, fields

from navability.entities.Client import Client, ClientSchema


class StatusMessageSchema(Schema):
    requestId = fields.String(required=True)
    action = fields.String(required=True)
    state = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    client = fields.Nested(ClientSchema, required=True)


class StatusMessage:
    schema: StatusMessageSchema = StatusMessageSchema()

    def __init__(
        self,
        requestId: str,
        action: str,
        state: str,
        timestamp: datetime,
        client: Client,
    ):
        self.requestId = requestId
        self.action = action
        self.state = state
        self.timestamp = timestamp
        self.client = client

    def __repr__(self):
        return f"<StatusMessage(requestId={self.requestId})>"

    def dump(self):
        return StatusMessage.schema.dump(self)

    def dumps(self):
        return StatusMessage.schema.dumps(self)
