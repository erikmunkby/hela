from dataclasses import dataclass, field


@dataclass
class BigqueryMode:
    NULLABLE = 'NULLABLE'
    REPEATED = 'REPEATED'


@dataclass
class BigqueryType:
    """Bigquery type, used to standardise the way bigquery Data Types are propagated down."""
    field_type: str
    mode: BigqueryMode = BigqueryMode.NULLABLE
    fields: tuple = field(default_factory=tuple)
