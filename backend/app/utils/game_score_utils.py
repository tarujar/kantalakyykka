def calculate_player_for_round(round_num: int, player_position: int, total_players: int) -> int:
    """Calculate which player should throw in a given round position
    
    Args:
        round_num: Current round number (1-based)
        player_position: Position in the round (1 or 2)
        total_players: Total number of players in team
        
    Returns:
        Player index (0-based)
    """
    base_player = ((round_num - 1) // 2 * 2) % total_players
    return (base_player + player_position - 1) % total_players

def calculate_throw_index(set_num: int, throw_round_num: int, is_home_team: bool, player_position: int) -> int:
    """Calculate the throw index number (1-20) for display
    
    Args:
        set_num: Set number (1 or 2)
        throw_round_num: Round number within the set
        is_home_team: Whether this is home team
        player_position: Position in the round (1 or 2)
        
    Returns:
        Global throw index (1-based)
    """
    throws_per_player = 2
    players_per_team = 2
    throws_per_round = throws_per_player * players_per_team
    
    # Calculate base index that continues across rounds but resets for each team
    round_base = (throw_round_num - 1) * throws_per_round
    player_offset = (player_position - 1) * throws_per_player
    
    return round_base + player_offset + 1
