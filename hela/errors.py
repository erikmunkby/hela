"""Module with custom errors."""


class InferralError(Exception):
    """Error sent when an inferral failed."""
    pass


class DatasetError(Exception):
    pass


class DuplicationError(Exception):
    pass


class ValidationError(Exception):
    pass
