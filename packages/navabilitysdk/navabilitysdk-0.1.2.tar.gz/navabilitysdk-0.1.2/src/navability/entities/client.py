from dataclasses import dataclass

from marshmallow import Schema, fields, post_load


@dataclass()
class Client:
    userId: str
    robotId: str
    sessionId: str

    def __repr__(self):
        return f"<Client(userId={self.userId}, robotId={self.robotId}, sessionId={self.sessionId})>"  # noqa: E501, B950

    def dump(self):
        return ClientSchema().dump(self)

    def dumps(self):
        return ClientSchema().dumps(self)

    @staticmethod
    def load(data):
        return ClientSchema().load(data)


class ClientSchema(Schema):
    userId = fields.String(required=True)
    robotId = fields.String(required=True)
    sessionId = fields.String(required=True)

    class Meta:
        ordered = True

    @post_load
    def marshal(self, data, **kwargs):
        return Client(**data)
