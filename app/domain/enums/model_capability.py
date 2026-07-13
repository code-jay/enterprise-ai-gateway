from enum import Enum


class ModelCapability(str, Enum):

    CHAT = "chat"

    REASONING = "reasoning"

    CODING = "coding"

    VISION = "vision"

    AUDIO = "audio"

    IMAGE_GENERATION = "image_generation"

    LONG_CONTEXT = "long_context"

    FUNCTION_CALLING = "function_calling"

    STRUCTURED_OUTPUT = "structured_output"