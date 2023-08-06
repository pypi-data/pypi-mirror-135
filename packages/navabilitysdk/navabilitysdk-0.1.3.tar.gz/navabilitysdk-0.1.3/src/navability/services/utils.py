import time
from typing import List

from navability.entities import NavAbilityClient
from navability.services import getStatusLatest


def waitForCompletion(
    navAbilityClient: NavAbilityClient,
    requestIds: List[str],
    maxSeconds: int = 60,
    expectedStatus: str = "Complete",
    exceptionMessage: str = "Requests did not complete in time",
):
    """Wait for the requests to complete, poll until done.

    Args:
        requestIds (List[str]): The request IDs that should be polled.
        maxSeconds (int, optional): Maximum wait time. Defaults to 60.
        expectedStatus (str, optional): Expected status message per request.
            Defaults to "Complete".
    """
    wait_time = maxSeconds
    while any(
        [
            getStatusLatest(navAbilityClient, res).state != expectedStatus
            for res in requestIds
        ]
    ):
        time.sleep(2)
        wait_time -= 2
        if wait_time <= 0:
            raise Exception(exceptionMessage)
