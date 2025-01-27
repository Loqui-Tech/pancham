from enum import Enum

class FileType(Enum):
    """
    Enumeration of various file types supported by the system.

    This class defines constants used to represent different file types
    formats, primarily for use cases involving file processing,
    identification, or format-specific operations.

    :cvar EXCEL_XLSX: Represents Excel files with the '.xlsx' extension.
    :type EXCEL_XLSX: str
    """

    EXCEL_XLSX = "xlsx"