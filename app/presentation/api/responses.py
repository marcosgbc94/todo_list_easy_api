from app.core.result import Result
from app.core.error_map import ERROR_MAP
from app.core.error_list import ErrorCode

def handle_result(result: Result):
    if not result.success:
        exception = ERROR_MAP.get(result.code, ERROR_MAP[ErrorCode.INTERNAL_ERROR])

        if result.error:
            exception.detail = result.error

        raise exception

    return result.data