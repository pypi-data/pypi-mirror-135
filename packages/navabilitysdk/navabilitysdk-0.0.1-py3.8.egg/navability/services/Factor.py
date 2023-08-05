from typing import List

from gql import gql

from navability.common.queries import gql_addFactor, gql_list, gql_list_fields_default
from navability.entities.Client import Client
from navability.entities.Factor import Factor
from navability.entities.NavAbilityClient import (
    MutationOptions,
    NavAbilityClient,
    QueryOptions,
)


def addFactor(navAbilityClient: NavAbilityClient, client: Client, f: Factor):
    return navAbilityClient.mutate(
        MutationOptions(
            gql(gql_addFactor),
            {"factor": {"client": client.dump(), "packedData": f.dumps()}},
        )
    )


def lsf(
    navAbilityClient: NavAbilityClient,
    client: Client,
    regexFilter: str = None,
    tags: List[str] = None,
    solvable: int = 0,
    fields: str = gql_list_fields_default,
):
    ls = navAbilityClient.query(
        QueryOptions(
            gql(gql_list.replace("__TYPE__", "FACTOR").replace("__FIELDS__", fields)),
            {
                "userId": client.userId,
                "robotId": client.robotId,
                "sessionId": client.sessionId,
                "regexFilter": regexFilter,
                "tags": tags,
                "solvable": solvable,
            },
        )
    )
    # TODO: Check for errors
    return ls["list"]
