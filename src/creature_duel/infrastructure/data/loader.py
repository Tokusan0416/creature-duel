"""
マスタデータローダー

JSONファイルからCreature、Skill、Abilityのマスタデータを読み込みます。
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from creature_duel.domain.entities.creature import Creature
from creature_duel.domain.entities.skill import Skill
from creature_duel.domain.entities.ability import Ability
from creature_duel.domain.value_objects.stats import Stats
from creature_duel.domain.value_objects.type import Type
from creature_duel.domain.enums.move_category import MoveCategory


class MasterDataLoader:
    """マスタデータを読み込むローダークラス"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        初期化

        Args:
            data_dir: データディレクトリのパス（未指定の場合はデフォルトパス）
        """
        if data_dir is None:
            # デフォルトはこのファイルと同じディレクトリ
            data_dir = Path(__file__).parent
        self.data_dir = data_dir

        # キャッシュ
        self._skills: Optional[Dict[str, Skill]] = None
        self._creatures: Optional[Dict[str, Creature]] = None
        self._abilities: Optional[Dict[str, Ability]] = None
        self._type_chart: Optional[Dict[str, Dict[str, float]]] = None

    def load_skills(self) -> Dict[str, Skill]:
        """
        スキルマスタを読み込む

        Returns:
            スキルID -> Skillエンティティの辞書
        """
        if self._skills is not None:
            return self._skills

        skills_file = self.data_dir / "skills.json"
        with open(skills_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        skills = {}
        for skill_data in data["skills"]:
            skill = Skill(
                name=skill_data["name"],
                type=Type(skill_data["type"]),
                category=MoveCategory(skill_data["category"]),
                power=skill_data["power"],
                accuracy=skill_data["accuracy"],
                max_pp=skill_data["max_pp"],
                effects=skill_data.get("effects", []),
            )
            skills[skill_data["id"]] = skill

        self._skills = skills
        return skills

    def load_creatures(self) -> Dict[str, Creature]:
        """
        クリーチャーマスタを読み込む

        Returns:
            クリーチャーID -> Creatureエンティティの辞書
        """
        if self._creatures is not None:
            return self._creatures

        # まずスキルを読み込む
        skills = self.load_skills()

        creatures_file = self.data_dir / "creatures.json"
        with open(creatures_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        creatures = {}
        for creature_data in data["creatures"]:
            # タイプの変換
            types = [Type(t) for t in creature_data["types"]]

            # スキルの取得
            creature_skills = [
                skills[skill_id] for skill_id in creature_data["skill_ids"]
            ]

            # Statsの構築
            stats_data = creature_data["base_stats"]
            stats = Stats(
                hp=stats_data["hp"],
                attack=stats_data["attack"],
                defence=stats_data["defence"],
                sp_attack=stats_data["sp_attack"],
                sp_defence=stats_data["sp_defence"],
                speed=stats_data["speed"],
            )

            # Creatureの構築
            creature = Creature(
                name=creature_data["name"],
                types=types,
                base_stats=stats,
                skills=creature_skills,
                ability=creature_data.get("ability"),
            )

            creatures[creature_data["id"]] = creature

        self._creatures = creatures
        return creatures

    def load_abilities(self) -> Dict[str, Ability]:
        """
        アビリティマスタを読み込む

        Returns:
            アビリティID -> Abilityオブジェクトの辞書
        """
        if self._abilities is not None:
            return self._abilities

        abilities_file = self.data_dir / "abilities.json"
        with open(abilities_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        abilities = {}
        for ability_data in data["abilities"]:
            ability = Ability.from_dict(ability_data)
            abilities[ability.id] = ability

        self._abilities = abilities
        return abilities

    def load_type_chart(self) -> Dict[str, Dict[str, float]]:
        """
        タイプ相性表を読み込む

        Returns:
            攻撃タイプ -> {防御タイプ -> 倍率} の辞書
        """
        if self._type_chart is not None:
            return self._type_chart

        type_chart_file = self.data_dir / "type_chart.json"
        with open(type_chart_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._type_chart = data["type_chart"]
        return self._type_chart

    def get_creature(self, creature_id: str) -> Creature:
        """
        IDでクリーチャーを取得

        Args:
            creature_id: クリーチャーID

        Returns:
            Creatureエンティティ

        Raises:
            KeyError: 指定されたIDのクリーチャーが存在しない
        """
        creatures = self.load_creatures()
        if creature_id not in creatures:
            raise KeyError(f"Creature '{creature_id}' not found")
        return creatures[creature_id]

    def get_skill(self, skill_id: str) -> Skill:
        """
        IDでスキルを取得

        Args:
            skill_id: スキルID

        Returns:
            Skillエンティティ

        Raises:
            KeyError: 指定されたIDのスキルが存在しない
        """
        skills = self.load_skills()
        if skill_id not in skills:
            raise KeyError(f"Skill '{skill_id}' not found")
        return skills[skill_id]

    def get_ability(self, ability_id: str) -> Ability:
        """
        IDでアビリティを取得

        Args:
            ability_id: アビリティID

        Returns:
            Abilityオブジェクト

        Raises:
            KeyError: 指定されたIDのアビリティが存在しない
        """
        abilities = self.load_abilities()
        if ability_id not in abilities:
            raise KeyError(f"Ability '{ability_id}' not found")
        return abilities[ability_id]

    def list_creatures(self) -> List[str]:
        """
        全クリーチャーのIDリストを取得

        Returns:
            クリーチャーIDのリスト
        """
        creatures = self.load_creatures()
        return list(creatures.keys())

    def list_skills(self) -> List[str]:
        """
        全スキルのIDリストを取得

        Returns:
            スキルIDのリスト
        """
        skills = self.load_skills()
        return list(skills.keys())

    def list_abilities(self) -> List[str]:
        """
        全アビリティのIDリストを取得

        Returns:
            アビリティIDのリスト
        """
        abilities = self.load_abilities()
        return list(abilities.keys())
