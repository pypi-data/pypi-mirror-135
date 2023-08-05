# This will become common across all SDKs so we can't assume it's going to flake cleanly.
# flake8: noqa

# Very generic find query
GQL_FRAGMENT_VARIABLES = """
fragment ppe_fields on PPE {
  solveKey
  suggested
  max
  mean
  lastUpdatedTimestamp {formatted}
}
fragment solverdata_fields on SOLVERDATA {
  solveKey
  BayesNetOutVertIDs
  BayesNetVertID
  dimIDs
  dimbw
  dims
  dimval
  dontmargin
  eliminated
  infoPerCoord
  initialized
  ismargin
  separator
  solveInProgress
  solvedCount
  variableType
  vecbw
  vecval
  _version
}
fragment variable_skeleton_fields on VARIABLE {
	label
  tags
}
fragment variable_summary_fields on VARIABLE {
  timestamp {formatted}
  ppes {
    ...ppe_fields
  }
  variableType
  _version
  _id
}
fragment variable_full_fields on VARIABLE{
  smallData
  solvable
  solverData
  {
		...solverdata_fields
  }
}
"""

GQL_FRAGMENT_FACTORS = """
fragment factor_skeleton_fields on FACTOR {
	label
  tags
  _variableOrderSymbols
}
fragment factor_summary_fields on FACTOR {
  timestamp {formatted}
  _version
}
fragment factor_full_fields on FACTOR {
  fnctype
  solvable
  data
}
"""

GQL_GETVARIABLES = """
query sdk_get_variables(
  	$userId: ID!,
  	$robotIds: [ID!]!,
  	$sessionIds: [ID!]!,
    $variable_label_regexp: ID = ".*",
    $variable_tags: [String!] = ["VARIABLE"],
    $solvable: Int! = 0,
  	$fields_summary: Boolean! = false,
  	$fields_full: Boolean! = false){
	USER(id: $userId) {
    name
		robots(filter:{id_in: $robotIds}) {
      name
      sessions(filter:{id_in: $sessionIds}){
        name
        variables(filter:{
            label_regexp: $variable_label_regexp,
          	tags_contains: $variable_tags,
          	solvable_gte: $solvable}) {
          ...variable_skeleton_fields # Always include
          ...variable_summary_fields @include(if: $fields_summary)
          ...variable_full_fields @include(if: $fields_full)
        }
      }
    }
  }
}"""

GQL_GETFACTORS = """
query sdk_get_factors(
  	$userId: ID!,
  	$robotIds: [ID!]!,
  	$sessionIds: [ID!]!,
    $factor_label_regexp: ID = ".*",
    $factor_tags: [String!] = ["FACTOR"],
    $solvable: Int! = 0,
  	$fields_summary: Boolean! = false,
  	$fields_full: Boolean! = false){
	USER(id: $userId) {
    name
		robots(filter:{id_in: $robotIds}) {
      name
      sessions(filter:{id_in: $sessionIds}){
        name
        factors(filter:{
            label_regexp: $factor_label_regexp,
          	tags_contains: $factor_tags,
          	solvable_gte: $solvable}) {
          ...factor_skeleton_fields # Always include
          ...factor_summary_fields @include(if: $fields_summary)
          ...factor_full_fields @include(if: $fields_full)
        }
      }
    }
  }
}"""


GQL_GETVARIABLESFACTORS = """
query sdk_get_variablesfactors(
  	$userId: ID!,
  	$robotIds: [ID!]!,
  	$sessionIds: [ID!]!,
  	$variables: Boolean! = true,
  	$factors: Boolean! = true,
    $variable_label_regexp: ID = ".*",
    $factor_label_regexp: ID = ".*",
    $variable_tags: [String!] = ["VARIABLE"],
    $factor_tags: [String!] = ["FACTOR"],
    $solvable: Int! = 0,
  	$fields_summary: Boolean! = false,
  	$fields_full: Boolean! = false){
	USER(id: $userId) {
    name
		robots(filter:{id_in: $robotIds}) {
      name
      sessions(filter:{id_in: $sessionIds}){
        name
        variables(filter:{
            label_regexp: $variable_label_regexp,
          	tags_contains: $variable_tags,
          	solvable_gte: 0}) @include(if: $variables){
          ...variable_skeleton_fields # Always include
          ...variable_summary_fields @include(if: $fields_summary)
          ...variable_full_fields @include(if: $fields_full)
        }
        factors(filter:{
            label_regexp: $factor_label_regexp,
          	tags_contains: $factor_tags,
          	solvable_gte: $solvable}) @include(if: $factors){
          ...factor_skeleton_fields # Always include
          ...factor_summary_fields @include(if: $fields_summary)
          ...factor_full_fields @include(if: $fields_full)
        }
      }
    }
  }
}"""


GQL_GETVARIABLE = """
query sdk_get_variable(
  	$userId: ID!,
  	$robotId: ID!,
  	$sessionId: ID!,
    $label: ID!) {
	USER(id: $userId) {
		robots(filter:{id: $robotId}) {
      sessions(filter:{id: $sessionId}) {
        variables(filter:{label: $label}) {
          ...variable_skeleton_fields
          ...variable_summary_fields
          ...variable_full_fields
        }
      }
    }
  }
}"""


GQL_GETFACTOR = """
query sdk_get_variable(
  	$userId: ID!,
  	$robotId: ID!,
  	$sessionId: ID!,
    $label: ID!) {
	USER(id: $userId) {
		robots(filter:{id: $robotId}) {
      sessions(filter:{id: $sessionId}) {
        factors(filter:{label: $label}) {
          ...factor_skeleton_fields
          ...factor_summary_fields
          ...factor_full_fields
        }
      }
    }
  }
}"""


GQL_GETSTATUSMESSAGES = """
query sdk_ls_statusmessages($id: ID!) {
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
"""

GQL_GETSTATUSLATEST = """
query sdk_get_statuslatest($id: ID!) {
  statusLatest(id: $id) {
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
"""
