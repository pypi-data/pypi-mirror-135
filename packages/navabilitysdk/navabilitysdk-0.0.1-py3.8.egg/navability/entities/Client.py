from dataclasses import dataclass
from typing import ClassVar

from marshmallow import Schema, fields


class ClientSchema(Schema):
    userId = fields.String(required=True)
    robotId = fields.String(required=True)
    sessionId = fields.String(required=True)

    class Meta:
        ordered = True


@dataclass()
class Client:
    schema: ClassVar[ClientSchema] = ClientSchema()
    userId: str
    robotId: str
    sessionId: str

    def __repr__(self):
        return f"<Client(userId={self.userId}, robotId={self.robotId}, sessionId={self.sessionId})>"  # noqa: E501, B950

    def dump(self):
        return Client.schema.dump(self)

    def dumps(self):
        return Client.schema.dumps(self)
