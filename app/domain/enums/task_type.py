"""
Supported AI Tasks.
"""

from enum import Enum


class TaskType(str, Enum):

    CHAT = "chat"

    QA = "qa"

    SUMMARIZATION = "summarization"

    TRANSLATION = "translation"

    CLASSIFICATION = "classification"

    EXTRACTION = "extraction"

    CODE_GENERATION = "code_generation"

    CODE_REVIEW = "code_review"

    DOCUMENT_ANALYSIS = "document_analysis"

    RAG = "rag"

    VISION = "vision"

    AGENT = "agent"

    REASONING = "reasoning"

    GENERAL = "general"