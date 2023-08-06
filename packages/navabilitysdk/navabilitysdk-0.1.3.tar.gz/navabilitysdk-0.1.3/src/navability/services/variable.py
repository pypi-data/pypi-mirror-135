import logging
from typing import List

from gql import gql

from navability.common.mutations import GQL_ADDVARIABLE
from navability.common.queries import (
    GQL_FRAGMENT_VARIABLES,
    GQL_GETVARIABLE,
    GQL_GETVARIABLES,
)
from navability.entities.client import Client
from navability.entities.navabilityclient import (
    MutationOptions,
    NavAbilityClient,
    QueryOptions,
)
from navability.entities.querydetail import QueryDetail
from navability.entities.variable.variable import (
    Variable,
    VariableSchema,
    VariableSkeleton,
    VariableSkeletonSchema,
    VariableSummarySchema,
)

DETAIL_SCHEMA = {
    QueryDetail.LABEL: None,
    QueryDetail.SKELETON: VariableSkeletonSchema(),
    QueryDetail.SUMMARY: VariableSummarySchema(),
    QueryDetail.FULL: VariableSchema(),
}

logger = logging.getLogger(__name__)


def addVariable(navAbilityClient: NavAbilityClient, client: Client, v: Variable):
    return navAbilityClient.mutate(
        MutationOptions(
            gql(GQL_ADDVARIABLE),
            {"variable": {"client": client.dump(), "packedData": v.dumpsPacked()}},
        )
    )["addVariable"]


def listVariables(
    navAbilityClient: NavAbilityClient,
    client: Client,
    regexFilter: str = ".*",
    tags: List[str] = None,
    solvable: int = 0,
) -> List[str]:
    return [
        v.label
        for v in getVariables(
            navAbilityClient,
            client,
            detail=QueryDetail.SKELETON,
            regexFilter=regexFilter,
            tags=tags,
            solvable=solvable,
        )
    ]


# Alias
ls = listVariables


def getVariables(
    navAbilityClient: NavAbilityClient,
    client: Client,
    detail: QueryDetail = QueryDetail.SKELETON,
    regexFilter: str = ".*",
    tags: List[str] = None,
    solvable: int = 0,
) -> List[VariableSkeleton]:
    params = {
        "userId": client.userId,
        "robotIds": [client.robotId],
        "sessionIds": [client.sessionId],
        "variable_label_regexp": regexFilter,
        "variable_tags": tags if tags is not None else ["VARIABLE"],
        "solvable": solvable,
        "fields_summary": detail in [QueryDetail.SUMMARY, QueryDetail.FULL],
        "fields_full": detail == QueryDetail.FULL,
    }
    logger.debug(f"Query params: {params}")
    res = navAbilityClient.query(
        QueryOptions(gql(GQL_FRAGMENT_VARIABLES + GQL_GETVARIABLES), params)
    )
    logger.debug(f"Query result: {res}")
    # TODO: Check for errors
    schema = DETAIL_SCHEMA[detail]
    # Using the hierarchy approach, we need to check that we have
    # exactly one user/robot/session in it, otherwise error.
    if (
        "USER" not in res
        or len(res["USER"]) != 1
        or len(res["USER"][0]["robots"]) != 1
        or len(res["USER"][0]["robots"][0]["sessions"]) != 1
        or "variables" not in res["USER"][0]["robots"][0]["sessions"][0]
    ):
        # Debugging information
        if len(res["USER"]) != 1:
            logger.warn("User not found in result, returning empty list")
        if len(res["USER"][0]["robots"]) != 1:
            logger.warn("Robot not found in result, returning empty list")
        if len(res["USER"][0]["robots"][0]["sessions"]) != 1:
            logger.warn("Robot not found in result, returning empty list")
        return []
    if schema is None:
        return res["USER"][0]["robots"][0]["sessions"][0]["variables"]
    return [
        schema.load(l) for l in res["USER"][0]["robots"][0]["sessions"][0]["variables"]
    ]


def getVariable(navAbilityClient: NavAbilityClient, client: Client, label: str):
    params = client.dump()
    params["label"] = label
    logger.debug(f"Query params: {params}")
    res = navAbilityClient.query(
        QueryOptions(gql(GQL_FRAGMENT_VARIABLES + GQL_GETVARIABLE), params)
    )
    logger.debug(f"Query result: {res}")
    # TODO: Check for errors
    # Using the hierarchy approach, we need to check that we have
    # exactly one user/robot/session in it, otherwise error.
    if (
        "USER" not in res
        or len(res["USER"][0]["robots"]) != 1
        or len(res["USER"][0]["robots"][0]["sessions"]) != 1
        or "variables" not in res["USER"][0]["robots"][0]["sessions"][0]
    ):
        raise Exception(
            "Received an empty data structure, set logger to debug for the payload"
        )
    vs = res["USER"][0]["robots"][0]["sessions"][0]["variables"]
    # TODO: Check for errors
    if len(vs) == 0:
        return None
    if len(vs) > 1:
        raise Exception(f"More than one variable named {label} returned")
    return Variable.load(vs[0])
