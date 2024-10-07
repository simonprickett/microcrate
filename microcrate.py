import requests
from base64 import b64encode

# IDs of CrateDB supported data types.
# https://cratedb.com/docs/crate/reference/en/latest/interfaces/http.html#id4
CRATEDB_TYPE_NULL = 0
CRATEDB_TYPE_NOT_SUPPORTED = 1
CRATEDB_TYPE_CHAR = 2
CRATEDB_TYPE_BOOLEAN = 3
CRATEDB_TYPE_TEXT = 4
CRATEDB_TYPE_IP = 5
CRATEDB_TYPE_DOUBLE_PRECISION = 6
CRATEDB_TYPE_REAL = 7
CRATEDB_TYPE_SMALLINT = 8
CRATEDB_TYPE_INTEGER = 9
CRATEDB_TYPE_BIGINT = 10
CRATEDB_TYPE_TIMESTAMP_WITH_TIME_ZONE = 11
CRATEDB_TYPE_OBJECT = 12
CRATEDB_TYPE_GEO_POINT = 13
CRATEDB_TYPE_GEO_SHAPE = 14
CRATEDB_TYPE_TIMESTAMP_WITHOUT_TIME_ZONE = 15
CRATEDB_TYPE_UNCHECKED_OBJECT = 16
CRATEDB_TYPE_INTERVAL = 17
CRATEDB_TYPE_REGPROC = 19
CRATEDB_TYPE_TIME = 20
CRATEDB_TYPE_OIDVECTOR = 21
CRATEDB_TYPE_NUMERIC = 22
CRATEDB_TYPE_REGCLASS = 23
CRATEDB_TYPE_DATE = 24
CRATEDB_TYPE_BIT = 25
CRATEDB_TYPE_JSON = 26
CRATEDB_TYPE_CHARACTER = 27
CRATEDB_TYPE_FLOAT_VECTOR = 28
CRATEDB_TYPE_ARRAY = 100

# CrateDB error codes.
# https://cratedb.com/docs/crate/reference/en/latest/interfaces/http.html#error-codes
CRATEDB_ERROR_INVALID_SYNTAX = 4000
CRATEDB_ERROR_INVALID_ANALYZER = 4001
CRATEDB_ERROR_INVALID_RELATION_NAME = 4002
CRATEDB_ERROR_FIELD_TYPE_VALIDATION_FAILED = 4003
CRATEDB_ERROR_FEATURE_UNSUPPORTED = 4004
CRATEDB_ERROR_ALTER_TABLE_WITH_ALIAS_UNSUPPORTED = 4005
CRATEDB_ERROR_COLUMN_ALIAS_AMBIGUOUS = 4006
CRATEDB_ERROR_OPERATION_NOT_SUPPORTED_ON_RELATION = 4007
CRATEDB_ERROR_INVALID_COLUMN_NAME = 4008
CRATEDB_ERROR_USER_NOT_AUTHORIZED = 4010
CRATEDB_ERROR_MISSING_USER_PRIVILEGE = 4011
CRATEDB_ERROR_NODE_READ_ONLY = 4031
CRATEDB_ERROR_UNKNOWN_RELATION = 4041
CRATEDB_ERROR_UNKNOWN_ANALYZER = 4042
CRATEDB_ERROR_UNKNOWN_COLUMN = 4043
CRATEDB_ERROR_UNKNOWN_TYPE = 4044
CRATEDB_ERROR_UNKNOWN_SCHEMA = 4045
CRATEDB_ERROR_UNKNOWN_PARTITION = 4046
CRATEDB_ERROR_UNKNOWN_REPOSITORY = 4047
CRATEDB_ERROR_UNKNOWN_SNAPSHOT = 4048
CRATEDB_ERROR_UNKNOWN_FUNCTION = 4049
CRATEDB_ERROR_UNKNOWN_USER = 40410
CRATEDB_ERROR_DOCUMENT_EXISTS = 4091
CRATEDB_ERROR_VERSION_CONFLICT = 4092
CRATEDB_ERROR_RELATION_EXISTS = 4093
CRATEDB_ERROR_TABLE_ALIAS_SCHEMA_DIFFERS = 4094
CRATEDB_ERROR_REPOSITORY_EXISTS = 4095
CRATEDB_ERROR_SNAPSHOT_EXISTS = 4096
CRATEDB_ERROR_PARTITION_EXISTS = 4097
CRATEDB_ERROR_FUNCTION_EXISTS = 4098
CRATEDB_ERROR_USER_EXISTS = 4099
CRATEDB_ERROR_OBJECT_EXISTS = 4100
CRATEDB_ERROR_UNHANDLED_SERVER_ERROR = 5000
CRATEDB_ERROR_TASK_EXECUTION_FAILED = 5001
CRATEDB_ERROR_SHARDS_UNAVAILABLE = 5002
CRATEDB_ERROR_QUERY_FAILED_ON_SHARDS = 5003
CRATEDB_ERROR_SNAPSHOT_CREATION_FAILED = 5004
CRATEDB_ERROR_QUERY_KILLED = 5030

class NetworkError(Exception):
    pass

class CrateDBError(Exception):
    pass

class CrateDB:
    def __init__(self, host, port=4200, user=None, password=None, schema="doc", use_ssl=True):
        self.user = user
        self.password = password
        self.schema = schema
        self.host = host
        self.port = port
        self.use_ssl = use_ssl

        self.cratedb_url = f"{'https' if self.use_ssl == True else 'http'}://{self.host}:{self.port}/_sql"

        if self.user is not None and self.password is not None:
            self.encoded_credentials = self.__encode_credentials(self.user, self.password)


    def __encode_credentials(self, user, password):
        creds_str = f"{user}:{password}"
        return b64encode(creds_str.encode("UTF-8")).decode("UTF-8")
    

    def __make_request(self, sql, args=None, with_types = False, return_response = True):
        headers = {
            "Content-Type": "text/json",
            "Default-Schema": self.schema
        }

        if hasattr(self, "encoded_credentials"):
            headers["Authorization"] = f"Basic {self.encoded_credentials}"

        request_url = self.cratedb_url if with_types == False else f"{self.cratedb_url}?types"

        payload = {
            "stmt": sql
        }

        if args is not None:
            for arg in args:
                if not isinstance(arg, list):
                    payload["args"] = args
                    break

            if not "args" in payload:
                payload["bulk_args"] = args

        response = requests.post(
            request_url,
            headers = headers,
            json = payload
        )

        if response.status_code == 400 or response.status_code == 404 or response.status_code == 409:
            error_doc = response.json()
            raise CrateDBError(error_doc)
        elif response.status_code != 200:
            raise NetworkError(f"Error {response.status_code}: {response.reason.decode('UTF-8')}")

        if return_response == True:
            return response.json()


    def execute(self, sql, args = None, with_types = False, return_response = True):
        return self.__make_request(sql, args, with_types, return_response)
    