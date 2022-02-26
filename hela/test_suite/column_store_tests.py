from hela import _constants
from hela._column_classes import _ColumnType
from hela.errors import ValidationError
from collections import Counter


def validate_column_store_field_names(root_store: object) -> True:
    """Runs a validation check on all columns within a column store in order
    to make sure that all store variables have the same name as their
    column name

    Args:
        root_store: A class decorated with @column_store

    Returns:
        True if there were no mismatches

    Raises:
        ValidationError: If any columns are found with mismatching name & field

    Examples:
    >>> @column_store
    >>> class MyStore:
    >>>     b = Col('a', String())
    >>> validate_column_store_field_names(MyStore)
    ValidationError
    >>> @column_store
    >>> class MyStore:
    >>>     a = Col('a', String())
    >>> validate_column_store_field_names(MyStore)
    True
    """
    def _run_check(column_store: object) -> list:
        error_msgs = []
        for field_name, obj in column_store.__dict__.items():
            if isinstance(obj, _ColumnType):
                if field_name != obj.name:
                    error_msgs.append(f'Field "{field_name}" != Column "{obj.name}"')
            elif getattr(obj, _constants._COL_STORE_FLAG, False):
                error_msgs.extend(_run_check(obj))
        return error_msgs

    msgs = _run_check(root_store)
    if len(msgs) == 0:
        return True
    output = '\n'.join(msgs)
    raise ValidationError(f'Found following discrepancies:\n{output}')


def validate_no_duplicate_columns(root_store: object) -> True:
    """Runs a validation check on all columns within the store to make sure there
    are no duplicate columns

    Args:
        root_store: A column store class decorated with @column_store

    Returns:
        True if there are no duplicate columns

    Raises:
        ValidationError: If there exists duplicate columns
    """
    duplicate_columns = []
    for col, occurences in Counter(root_store.columns_recursive_).items():
        if occurences == 1:
            continue
        duplicate_columns.append(f'"{col.name}"')
    if len(duplicate_columns) == 0:
        return True
    out = ', '.join(duplicate_columns)
    raise ValidationError(f'Found duplicates of column(s): {out}')
