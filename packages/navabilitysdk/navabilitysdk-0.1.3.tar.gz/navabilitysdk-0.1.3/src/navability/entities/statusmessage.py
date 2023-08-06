from dataclasses import dataclass

from marshmallow import Schema, fields, post_load

from navability.entities.client import Client, ClientSchema


@dataclass()
class StatusMessage:
    requestId: str
    action: str
    state: str
    timestamp: str
    client: Client

    def __repr__(self):
        return (
            f"<StatusMessage(requestId={self.requestId}, "
            f"timestamp={self.timestamp}, client={self.client}, "
            f"action={self.action}, state={self.state})>"
        )

    def dump(self):
        return StatusMessage().dump(self)

    def dumps(self):
        return StatusMessage().dumps(self)

    @staticmethod
    def load(data):
        return StatusMessageSchema().load(data)


class StatusMessageSchema(Schema):
    requestId = fields.String(required=True)
    action = fields.String(required=True)
    state = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    client = fields.Nested(ClientSchema, required=True)

    class Meta:
        ordered = True

    @post_load
    def marshal(self, data, **kwargs):
        return StatusMessage(**data)


@dataclass
class MutationUpdate:
    mutationUpdate: StatusMessage

    def dump(self):
        return MutationUpdate().dump(self)

    def dumps(self):
        return MutationUpdate().dumps(self)

    @staticmethod
    def load(data):
        return MutationUpdate().load(data)


class MutationUpdateSchema(Schema):
    mutationUpdate = fields.Nested(StatusMessageSchema, required=True)

    class Meta:
        ordered = True

    @post_load
    def marshal(self, data, **kwargs):
        return MutationUpdate(**data)
