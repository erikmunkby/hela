from dataclasses import dataclass


@dataclass
class ShortDescription:
    """Dataclass for short descriptions"""
    name: str
    type: str
    description: str
