import random
from value_objects.type import get_type_multiplier
from entities.skill import Category

def calculate_damage(attacker, defender, skill):
    """
    Calculates the damage dealt by the attacker to the defender using the specified skill.

    Args:        
        attacker: The attacking creature (Creature instance).
        defender: The defending creature (Creature instance).
        skill: The skill being used (Skill instance).
    
    Returns:
        The damage dealt (int).
    
    Notes:
    - If the skill is a status move, it does not deal damage and returns 0.
    - For physical moves, the attacker's attack stat and defender's defence stat are used.
    - For special moves, the attacker's special attack stat and defender's special defence stat are used.
    - The base damage is calculated as (attack * skill power / defence).
    - The damage is then modified by the type effectiveness multiplier, STAB (Same Type Attack Bonus), and a critical hit multiplier.
    - The type effectiveness multiplier is determined by the attack type and the defender's types.
    - STAB is 1.5 if the skill's type matches one of the attacker's types, otherwise it is 1.0.
    - The critical hit multiplier is 2.0 if a random number between 0 and 1 is less than 0.1 (10% chance), otherwise it is 1.0.
    """
    if skill.category == Category.STATUS:
        return 0

    if skill.category == Category.PHYSICAL:
        attack = attacker.battle_stats.attack
        defence = defender.battle_stats.defence
    else:
        attack = attacker.battle_stats.sp_attack
        defence = defender.battle_stats.sp_defence

    base = attack * skill.power / defence

    type_bonus = get_type_multiplier(skill.type, defender.types)

    stab = 1.5 if skill.type in attacker.types else 1.0

    crit = 2.0 if random.random() < 0.1 else 1.0

    return int(base * type_bonus * stab * crit)