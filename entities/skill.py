from dataclasses import dataclass
from enum import Enum
from value_objects.type import Type

class Category(Enum):
    PHYSICAL = "physical"
    SPECIAL = "special"
    STATUS = "status"

@dataclass
class Skill:
    name: str
    type: Type
    category: Category
    power: int
    accuracy: float
    pp: int