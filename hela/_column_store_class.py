from hela._column_classes import _ColumnType
from hela._constants import _COL_STORE_FLAG


def _make_column_store(cls: object, label: str = None):
    columns_, columns_recursive_ = [], []
    for field, obj in cls.__dict__.items():
        if field.startswith('__') and field.endswith('__'):
            continue

        if getattr(obj, _COL_STORE_FLAG, False):
            columns_recursive_.extend(obj.columns_recursive_)
            continue

        if issubclass(obj.__class__, _ColumnType):
            if obj.name is None:
                obj.name = field
            obj.from_store = True
            obj.label = label
            columns_.append(obj)

    # Set properties to the column store
    setattr(cls, 'columns_', columns_)
    setattr(cls, 'columns_recursive_', columns_ + columns_recursive_)

    # Add functions to column store
    setattr(cls, _COL_STORE_FLAG, True)

    # Sort all fields in the column store alphabetically, for easier auto-complete
    all_fields = [(field_name, field_obj) for field_name, field_obj in cls.__dict__.items()]
    for f_tuple in sorted(all_fields, key=lambda x: x[0], reverse=True):
        # Cannot set __dict__, skip it
        if f_tuple[0] == '__dict__':
            continue
        setattr(cls, f_tuple[0], f_tuple[1])
    return cls


def column_store(cls=None, label: str = None) -> object:
    """Decorator to used to flag a class as a column store.

    A column store is a referencable class used when multiple datasets use the same column.
    In order to ensure that this column is purposefully duplicated among datasets we
    check that any duplicated column must originate from the same column store.

    Args:
        label: This string label will be passed down to all column objects within the store.

    Returns:
        The decorated class.


    Examples:
        >>> from hela import column_store, Col
        >>> from hela.data_types import String
        >>> @column_store(label='cool_columns')
        >>> class MyStore:
        ...     my_column = Col('my_column', String(), 'Example column')
        >>> MyStore.my_column
    """

    def wrap(cls):
        return _make_column_store(cls, label=label)

    # This is triggered when called as @column_store() (with parentheses)
    if cls is None:
        return wrap

    # This is triggered when called as @column_store (no parentheses)
    # Only allow triggered with parenthesis, this will keep IDE hints.
    raise ValueError('A column store can only be decorated with called method: `@column_store()`')
