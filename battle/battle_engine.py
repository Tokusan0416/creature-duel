from battle.turn_processor import process_turn

def run_battle(state):
    """Runs the battle loop until one creature faints.
    
    Args:
        state: The initial state of the battle (BattleState instance).
    
    Returns:
        A tuple containing the winner ("player1" or "player2") and the battle logs.
    
    Notes:
    - The function continuously processes turns until one of the creatures' HP drops to 0 or below.
    - After each turn, it checks if either creature has fainted and returns the winner and the battle logs.
    """
    while True:
        process_turn(state)

        if state.player1.is_fainted():
            return "player2", state.logs

        if state.player2.is_fainted():
            return "player1", state.logs