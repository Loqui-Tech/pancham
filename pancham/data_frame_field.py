from typing import Type, Callable
import pandas as pd

class DataFrameField:
    """
    Represents a field in a DataFrame with specific properties and behavior.

    This class is used to define and represent a field/column in a pandas DataFrame.
    It provides customization options such as naming, type specification,
    nullable constraints, optional processing functions, and indexing preferences.
    The intent of this class is to act as a metadata descriptor or configuration
    entity that can enrich the DataFrame with more semantics or validation logic.

    :ivar name: Name of the field, typically used to reference it programmatically.
    :type name: str
    :ivar source_name: Original name of the field in the source file,
        which can be a string or an integer index.
    :type source_name: str | int
    :ivar field_type: The expected type of data in this field.
    :type field_type: Type
    :ivar nullable: Indicator of whether this field can contain null or missing values.
    :type nullable: bool
    :ivar func: A callable function that processes a DataFrame and extracts a value
        for this field. It can return various types including int, str, None,
        bool, or a pandas Series. None if no processing function is defined.
    :type func: Callable[[pd.DataFrame], int | str | None | bool | pd.Series] | None
    :ivar suppress_errors: Flag to indicate whether errors should be suppressed for a
        dynamic field.
    :type suppress_errors: bool
    """

    def __init__(
            self,
            name: str,
            source_name: str|int|None,
            field_type: Type,
            nullable: bool = True,
            func: Callable[[pd.DataFrame], int|str|None|bool|pd.Series]|None = None,
            suppress_errors: bool = False
    ) -> None:
        self.name = name
        self.source_name = source_name
        self.field_type = field_type
        self.nullable = nullable
        self.func = func
        self.suppress_errors = suppress_errors

    def is_dynamic(self) -> bool:
        return self.func is not None

    def __str__(self) -> str:
        return f"Name: {self.name}, Source Name: {self.source_name}, Type: {self.field_type}, Nullable: {self.nullable}"