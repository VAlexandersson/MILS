from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Chunk:
    content: str
    book: str
    chapter: str
    headings: List[str]
    order: int