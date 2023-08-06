import logging
from typing import List

from gql import gql

from navability.common.mutations import GQL_ADDFACTOR
from navability.common.queries import (
    GQL_FRAGMENT_FACTORS,
    GQL_GETFACTOR,
    GQL_GETFACTORS,
)
from navability.entities.client import Client
from navability.entities.factor.factor import (
    Factor,
    FactorSchema,
    FactorSkeleton,
    FactorSkeletonSchema,
    FactorSummarySchema,
)
from navability.entities.navabilityclient import (
    MutationOptions,
    NavAbilityClient,
    QueryOptions,
)
from navability.entities.querydetail import QueryDetail

DETAIL_SCHEMA = {
    QueryDetail.LABEL: None,
    QueryDetail.SKELETON: FactorSkeletonSchema(),
    QueryDetail.SUMMARY: FactorSummarySchema(),
    QueryDetail.FULL: FactorSchema(),
}

logger = logging.getLogger(__name__)


def addFactor(navAbilityClient: NavAbilityClient, client: Client, f: Factor):
    return navAbilityClient.mutate(
        MutationOptions(
            gql(GQL_ADDFACTOR),
            {"factor": {"client": client.dump(), "packedData": f.dumps()}},
        )
    )["addFactor"]


def listFactors(
    navAbilityClient: NavAbilityClient,
    client: Client,
    regexFilter: str = ".*",
    tags: List[str] = None,
    solvable: int = 0,
) -> List[str]:
    return [
        v.label
        for v in getFactors(
            navAbilityClient,
            client,
            detail=QueryDetail.SKELETON,
            regexFilter=regexFilter,
            tags=tags,
            solvable=solvable,
        )
    ]


# Alias
lsf = listFactors


def getFactors(
    navAbilityClient: NavAbilityClient,
    client: Client,
    detail: QueryDetail = QueryDetail.SKELETON,
    regexFilter: str = ".*",
    tags: List[str] = None,
    solvable: int = 0,
) -> List[FactorSkeleton]:
    params = {
        "userId": client.userId,
        "robotIds": [client.robotId],
        "sessionIds": [client.sessionId],
        "factor_label_regexp": regexFilter,
        "factor_tags": tags if tags is not None else ["FACTOR"],
        "solvable": solvable,
        "fields_summary": detail in [QueryDetail.SUMMARY, QueryDetail.FULL],
        "fields_full": detail == QueryDetail.FULL,
    }
    logger.debug(f"Query params: {params}")
    res = navAbilityClient.query(
        QueryOptions(gql(GQL_FRAGMENT_FACTORS + GQL_GETFACTORS), params)
    )
    logger.debug(f"Query result: {res}")
    # TODO: Check for errors
    schema = DETAIL_SCHEMA[detail]
    # Using the hierarchy approach, we need to check that
    # we have exactly one user/robot/session in it, otherwise error.
    if (
        "USER" not in res
        or len(res["USER"]) != 1
        or len(res["USER"][0]["robots"]) != 1
        or len(res["USER"][0]["robots"][0]["sessions"]) != 1
        or "factors" not in res["USER"][0]["robots"][0]["sessions"][0]
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
        return res["USER"][0]["robots"][0]["sessions"][0]["factors"]
    return [
        schema.load(l) for l in res["USER"][0]["robots"][0]["sessions"][0]["factors"]
    ]


def getFactor(navAbilityClient: NavAbilityClient, client: Client, label: str):
    params = client.dump()
    params["label"] = label
    logger.debug(f"Query params: {params}")
    res = navAbilityClient.query(
        QueryOptions(gql(GQL_FRAGMENT_FACTORS + GQL_GETFACTOR), params)
    )
    logger.debug(f"Query result: {res}")
    # TODO: Check for errors
    # Using the hierarchy approach, we need to check that we
    # have exactly one user/robot/session in it, otherwise error.
    if (
        "USER" not in res
        or len(res["USER"][0]["robots"]) != 1
        or len(res["USER"][0]["robots"][0]["sessions"]) != 1
        or "variables" not in res["USER"][0]["robots"][0]["sessions"][0]
    ):
        raise Exception(
            "Received an empty data structure, set logger to debug for the payload"
        )
    fs = res["USER"][0]["robots"][0]["sessions"][0]["factors"]
    # TODO: Check for errors
    if len(fs) == 0:
        return None
    if len(fs) > 1:
        raise Exception(f"More than one factor named {label} returned")
    return Factor.load(fs[0])
