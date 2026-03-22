import random
from services.damage_calculator import calculate_damage

def select_skill(creature):
    """
    Selects a skill for the creature to use in the turn.

    Args:
        creature: The creature for which to select a skill (Creature instance).

    Returns:
        A skill from the creature's skill list that has PP remaining (Skill instance).
    
    Notes:
    - The function filters the creature's skills to only include those with PP greater than 0.
    - It then randomly selects one of the available skills to use for the turn.    
    """
    available = [s for s in creature.skills if s.pp > 0]

    return random.choice(available)

def process_turn(state):
    """
    Processes a single turn of the battle.
    
    Args:
        state: The current state of the battle (BattleState instance).
        
    Notes:
    - Each creature selects a skill to use for the turn.
    - The order of actions is determined by the creatures' speed stats, with the faster creature acting first.
    - Each creature attacks the other using the selected skill, and damage is calculated and applied to the defender's HP.
    - The battle log is updated with the details of each attack, including the attacker, defender, skill used, damage dealt, and remaining HP.
    - If a creature's HP drops to 0 or below, it is considered fainted and cannot act for the rest of the turn.
    - The turn counter is incremented at the end of the turn.
    """
    c1 = state.player1
    c2 = state.player2

    s1 = select_skill(c1)
    s2 = select_skill(c2)

    order = sorted(
        [(c1, s1, c2), (c2, s2, c1)],
        key=lambda x: x[0].battle_stats.speed,
        reverse=True
    )

    for attacker, skill, defender in order:
        if attacker.is_fainted():
            continue

        damage = calculate_damage(attacker, defender, skill)
        defender.battle_stats.current_hp -= damage

        state.add_log({
            "turn": state.turn,
            "event": "attack",
            "attacker": attacker.name,
            "defender": defender.name,
            "skill": skill.name,
            "damage": damage,
            "hp_after": defender.battle_stats.current_hp
        })

        if defender.is_fainted():
            break

    state.turn += 1