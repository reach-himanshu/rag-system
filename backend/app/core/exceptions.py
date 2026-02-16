"""Custom exception classes for the RAG System."""


class RAGSystemError(Exception):
    """Base exception for the RAG System."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(RAGSystemError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message=message, code="AUTHENTICATION_ERROR")


class DocumentProcessingError(RAGSystemError):
    """Raised when document processing fails."""

    def __init__(self, message: str):
        super().__init__(message=message, code="DOCUMENT_PROCESSING_ERROR")


class LLMError(RAGSystemError):
    """Raised when LLM API calls fail."""

    def __init__(self, message: str):
        super().__init__(message=message, code="LLM_ERROR")


class NotFoundError(RAGSystemError):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} with id '{resource_id}' not found",
            code="NOT_FOUND",
        )
