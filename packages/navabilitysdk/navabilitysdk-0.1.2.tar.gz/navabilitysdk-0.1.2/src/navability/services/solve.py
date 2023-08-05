from gql import gql

from navability.common.mutations import GQL_SOLVESESSION
from navability.entities.client import Client
from navability.entities.navabilityclient import MutationOptions, NavAbilityClient


def solveSession(navAbilityClient: NavAbilityClient, client: Client):
    return navAbilityClient.mutate(
        MutationOptions(gql(GQL_SOLVESESSION), {"client": client.dump()})
    )["solveSession"]
