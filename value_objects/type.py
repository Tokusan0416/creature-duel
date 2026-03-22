from enum import Enum

class Type(Enum):
    NORMAL = "normal"
    FIRE = "fire"
    WATER = "water"
    GRASS = "grass"
    ELECTRIC = "electric"
    ICE = "ice"


# Effectiveness chart for the types
TYPE_EFFECTIVENESS = {
    (Type.FIRE, Type.GRASS): 2.0,
    (Type.FIRE, Type.WATER): 0.5,
    (Type.FIRE, Type.ICE): 2.0,
    (Type.WATER, Type.FIRE): 2.0,
    (Type.WATER, Type.GRASS): 0.5,
    (Type.GRASS, Type.FIRE): 0.5,
    (Type.GRASS, Type.WATER): 2.0,
    (Type.ELECTRIC, Type.WATER): 2.0,
    (Type.ELECTRIC, Type.GRASS): 0.5,
    (Type.ICE, Type.GRASS): 2.0,
    (Type.ICE, Type.FIRE): 0.5,
}
    
def get_type_multiplier(attack_type, defender_types):
    """
    Calculates the damage multiplier based on the attack type and defender types.

    Args:
        attack_type: The type of the attacking move (Type Enum).
        defender_types: A list of the defender's types (List of Type Enum).
    
    Returns: 
        The damage multiplier (float).

    Notes:
    - If the attack type is super effective against a defender type, the multiplier is 2.0.
    - If the attack type is not very effective against a defender type, the multiplier is 0.5.
    - If the attack type has no effect on a defender type, the multiplier is 0.0.
    - If the attack type is neutral against a defender type, the multiplier is 1.0.
    """
    multiplier = 1.0
    for d_type in defender_types:
        multiplier *= TYPE_EFFECTIVENESS.get((attack_type, d_type), 1.0)

    return multiplier