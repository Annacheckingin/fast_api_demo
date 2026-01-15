from dataclasses import dataclass,field
import random
from typing import ClassVar

@dataclass(order=True)
class User:
    id: int
    name: str
    email: int = field(repr=False)
    height: float = field(default_factory=random.randint(150, 200))  # in cm

from typing import TypeVar
T = TypeVar('T', int, str)

def add(x: T, y: T) -> T:
    return x + y