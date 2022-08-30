from tracepointdebug.probe.coded_error import CodedError

UNKNOWN = CodedError(0, "Unknown")

INSTRUMENTATION_IS_NOT_ACTIVE = CodedError(1000,
                                           "Couldn't activate instrumentation support." +
                                           " So custom tracepoints is not supported")
UNABLE_TO_FIND_MODULE = CodedError(1002, "Unable to find module")
LINE_NO_IS_NOT_AVAILABLE = CodedError(1004, "Line {} is not available in {} for tracepoint")
LINE_NO_IS_NOT_AVAILABLE_2 = CodedError(1004, "Line {} is not available in {} for tracepoint. Try line {}")
LINE_NO_IS_NOT_AVAILABLE_3 = CodedError(1004, "Line {} is not available in {} for tracepoint. Try lines {} or {}")
CONDITION_CHECK_FAILED = CodedError(
    1900,
    "Error occurred while checking condition '{}': {}")
CONDITION_EXPRESSION_SYNTAX_CHECK_FAILED = CodedError(
    1901,
    "Syntax check failed while checking condition '{}': {}")
UNABLE_TO_FIND_PROPERTY_FOR_CONDITION = CodedError(
    1904,
    "Unable to find property over file {} while evaluating condition: {}")

TRACEPOINT_ALREADY_EXIST = CodedError(2000, "Tracepoint has been already added in file {} on line {} from client {}")

NO_TRACEPOINT_EXIST = CodedError(2001, "No tracepoint could be found in file {} on line {} from client {}")
FILE_NAME_IS_MANDATORY = CodedError(2002, "File name is mandatory")
LINE_NUMBER_IS_MANDATORY = CodedError(2003, "Line number is mandatory")
NO_TRACEPOINT_EXIST_WITH_ID = CodedError(2004, "No tracepoint could be found with id {} from client {}")
CLIENT_HAS_NO_ACCESS_TO_TRACEPOINT = CodedError(2005, "Client {} has no access to tracepoint with id {}")

PUT_TRACEPOINT_FAILED = CodedError(
    2050,
    "Error occurred while putting tracepoint to file {} on line {} from client {}: {}")

SOURCE_CODE_MISMATCH_DETECTED = CodedError(
    2051,
    "Source code mismatch detected while putting {} to file {} on line {} from client {}")

UPDATE_TRACEPOINT_FAILED = CodedError(
    2100,
    "Error occurred while updating tracepoint to file {} on line {} from client {}: {}")

UPDATE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    2101,
    "Error occurred while updating tracepoint with id {} from client {}: {}")

REMOVE_TRACEPOINT_FAILED = CodedError(
    2150,
    "Error occurred while removing tracepoint from file {} on line {} from client {}: {}")

REMOVE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    2151,
    "Error occurred while removing tracepoint with id {} from client {}: {}")

ENABLE_TRACEPOINT_FAILED = CodedError(
    2200,
    "Error occurred while enabling tracepoint to file {} on line {} from client {}: {}")

ENABLE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    2201,
    "Error occurred while enabling tracepoint with id {} from client {}: {}")

DISABLE_TRACEPOINT_FAILED = CodedError(
    2250,
    "Error occurred while disabling tracepoint to file {} on line {} from client {}: {}")

DISABLE_TRACEPOINT_WITH_ID_FAILED = CodedError(
    2251,
    "Error occurred while disabling tracepoint with id {} from client {}: {}")

# LOGPOINT ERROR CODES

LOGPOINT_ALREADY_EXIST = CodedError(
    3000,
    "Logpoint has been already added in file {} on line {} from client {}"
)

NO_LOGPOINT_EXIST = CodedError(
    3001,
    "No logpoint could be found in file {} on line {} from client {}"
)

NO_LOGPOINT_EXIST_WITH_ID = CodedError(
    3004,
    "No logpoint could be found with id {} from client {}"
)

CLIENT_HAS_NO_ACCESS_TO_LOGPOINT = CodedError(
    3005,
    "Client {} has no access to logpoint with id {}"
)

PUT_LOGPOINT_FAILED = CodedError(
    3050,
    "Error occurred while putting logpoint to file {} on line {} from client {}: {}"
)

UPDATE_LOGPOINT_FAILED = CodedError(
    3100,
    "Error occurred while updating logpoint to file {} on line {} from client {}: {}")

UPDATE_LOGPOINT_WITH_ID_FAILED = CodedError(
    3101,
    "Error occurred while updating logpoint with id {} from client {}: {}")

REMOVE_LOGPOINT_FAILED = CodedError(
    3150,
    "Error occurred while removing logpoint from file {} on line {} from client {}: {}")

REMOVE_LOGPOINT_WITH_ID_FAILED = CodedError(
    3151,
    "Error occurred while removing logpoint with id {} from client {}: {}")

ENABLE_LOGPOINT_FAILED = CodedError(
    3200,
    "Error occurred while enabling logpoint to file {} on line {} from client {}: {}")

ENABLE_LOGPOINT_WITH_ID_FAILED = CodedError(
    3201,
    "Error occurred while enabling logpoint with id {} from client {}: {}")

DISABLE_LOGPOINT_FAILED = CodedError(
    3250,
    "Error occurred while disabling logpoint to file {} on line {} from client {}: {}")

DISABLE_LOGPOINT_WITH_ID_FAILED = CodedError(
    3251,
    "Error occurred while disabling logpoint with id {} from client {}: {}")