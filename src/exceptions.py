class TextSplitterError(Exception):
    """Base exception class for TextSplitter errors."""
    pass

class FileProcessingError(TextSplitterError):
    """Raised when there's an error processing a file."""
    pass