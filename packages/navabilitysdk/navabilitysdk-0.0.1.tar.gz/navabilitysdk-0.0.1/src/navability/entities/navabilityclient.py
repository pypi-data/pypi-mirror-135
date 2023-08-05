from dataclasses import dataclass

from gql import Client as GQLCLient
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport


@dataclass(frozen=True)
class QueryOptions:
    query: str
    variables: any = None
    fetchPolicy: any = None


@dataclass(frozen=True)
class MutationOptions:
    mutation: str
    variables: any = None
    fetchPolicy: any = None


class NavAbilityClient:
    def query(self, options: QueryOptions):
        pass

    def mutate(self, options: MutationOptions):
        pass


class NavAbilityWebsocketClient(NavAbilityClient):
    def __init__(self, url: str = "wss://api.d1.navability.io/graphql") -> None:
        super().__init__()
        transport = WebsocketsTransport(url=url)
        self.client = GQLCLient(transport=transport, fetch_schema_from_transport=True)

    def query(self, options: QueryOptions):
        return self.client.execute(options.query, options.variables)

    def mutate(self, options: MutationOptions):
        return self.client.execute(options.mutation, options.variables)


class NavAbilityHttpsClient(NavAbilityClient):
    def __init__(self, url: str = "https://api.d1.navability.io") -> None:
        super().__init__()
        transport = AIOHTTPTransport(url=url)
        self.client = GQLCLient(transport=transport, fetch_schema_from_transport=True)

    def query(self, options: QueryOptions):
        return self.client.execute(options.query, options.variables)

    def mutate(self, options: MutationOptions):
        return self.client.execute(options.mutation, options.variables)
