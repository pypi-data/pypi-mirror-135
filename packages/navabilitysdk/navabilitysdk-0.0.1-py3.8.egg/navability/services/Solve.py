from gql import gql

from navability.common.queries import gql_solveSession
from navability.entities.Client import Client
from navability.entities.NavAbilityClient import MutationOptions, NavAbilityClient


def solveSession(navAbilityClient: NavAbilityClient, client: Client):
    return navAbilityClient.mutate(
        MutationOptions(gql(gql_solveSession), {"client": client.dump()})
    )
