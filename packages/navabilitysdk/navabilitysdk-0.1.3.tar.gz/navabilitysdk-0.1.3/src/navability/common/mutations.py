# This will become common across all SDKs so we can't assume it's going to flake cleanly.
# flake8: noqa

GQL_ADDVARIABLE = """
mutation sdk_addVariable ($variable: FactorGraphInput!) {
    addVariable(variable: $variable)
}
"""

GQL_ADDFACTOR = """
mutation sdk_addFactor ($factor: FactorGraphInput!) {
  addFactor(factor: $factor)
}
"""

GQL_SOLVESESSION = """
mutation sdk_solveSession ($client: ClientInput!) {
  solveSession(client: $client)
}
"""
