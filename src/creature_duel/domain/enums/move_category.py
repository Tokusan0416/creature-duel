from enum import Enum


class MoveCategory(Enum):
    """技のカテゴリ"""
    PHYSICAL = "physical"  # 物理技
    SPECIAL = "special"    # 特殊技
    STATUS = "status"      # 変化技
