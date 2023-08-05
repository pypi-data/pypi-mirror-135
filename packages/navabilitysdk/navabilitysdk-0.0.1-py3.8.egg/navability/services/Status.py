from gql import gql

from navability.common.queries import gql_getStatusMessages
from navability.entities.NavAbilityClient import NavAbilityClient, QueryOptions
from navability.entities.StatusMessage import StatusMessageSchema


def getStatusMessages(navAbilityClient: NavAbilityClient, id: str):
    statusMessages = navAbilityClient.query(
        QueryOptions(gql(gql_getStatusMessages), {"id": id})
    )
    schema = StatusMessageSchema(many=True)
    return schema.load(statusMessages["statusMessages"])
