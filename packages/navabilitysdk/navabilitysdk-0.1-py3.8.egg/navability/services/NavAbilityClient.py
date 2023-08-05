from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
# from gql.transport.aiohttp import AIOHTTPTransport

from src.navability.entities.Variable import Variable
from src.navability.entities.Factor import Factor
from src.navability.entities.StatusMessage import StatusMessage, StatusMessageSchema
from src.navability.entities.Client import Client as NaviClient


# TODO: Move this
gql_addVariable = gql("""
mutation addVariable ($variable: FactorGraphInput!) {
    addVariable(variable: $variable)
}
""")


def params_addVariable(v: Variable): 
    return {
        "variable": {
            "client": {
                # _gqlClient(userId, robotId, sessionId),
                "userId": "Guest", 
                "robotId": "PyBot",
                "sessionId": "PyBot1"
            },
            "packedData": v.dumps()
        }
    }

gql_getStatusMessages = gql("""
        query getStatusMessages($id: ID!) {
            statusMessages(id: $id) {
                requestId,
                action,
                state,
                timestamp,
                client {
                    userId,
                    robotId,
                    sessionId
                }
            }
        }
        """)

gql_addFactor = gql("""
mutation addFactor ($factor: FactorGraphInput!) {
  addFactor(factor: $factor)
}
""")

def params_addFactor(f: Factor): 
    return {
        "factor": {
            "client": {
                # _gqlClient(userId, robotId, sessionId),
                "userId": "Guest", 
                "robotId": "PyBot",
                "sessionId": "PyBot1"
            },
            "packedData": f.dumps()
        }
    }

gql_solveSession = gql("""
mutation solveSession ($client: ClientInput!) {
  solveSession(client: $client)
}
""")

class NavAbilityClient:
    def __init__(self,
            url: str = 'wss://api.d1.navability.io/graphql'):
        transport = WebsocketsTransport(url='wss://api.d1.navability.io/graphql')
        self.client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
        )
        # self.naviClient = client

    def addVariable(self, v: Variable):
        return self.client.execute(gql_addVariable, params_addVariable(v))

    def addFactor(self, f: Factor):
        return self.client.execute(gql_addFactor, params_addFactor(f))

    def solveSession(self, c: NaviClient):
        return self.client.execute(gql_solveSession, params_addFactor(f))

    def getStatusMessages(self, id: str):
        statusMessages = self.client.execute(gql_getStatusMessages, {'id': id})
        schema = StatusMessageSchema(many=True)
        return schema.load(statusMessages["statusMessages"])
