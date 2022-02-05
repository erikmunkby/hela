from dataclasses import dataclass
from typing import Optional


@dataclass
class SimilarityInfo:
    score: float
    match_idx: int
    match_string: str
    target_string: Optional[str] = None
    target_idx: Optional[str] = None
