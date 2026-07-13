from enum import Enum


class FinishReason(str, Enum):

    STOP = "stop"

    LENGTH = "length"

    TOOL_CALL = "tool_call"

    CONTENT_FILTER = "content_filter"

    ERROR = "error"