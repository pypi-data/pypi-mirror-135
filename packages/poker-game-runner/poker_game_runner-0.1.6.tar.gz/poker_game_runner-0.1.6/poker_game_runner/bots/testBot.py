import numpy as np

from poker_game_runner.state import Observation

def get_name():
    return "testBot"

def act(obs: Observation):
    obs.action_to_str(obs.legal_actions[-1])
    obs.can_raise()
    obs.get_actions_in_round(0)
    obs.get_actions_this_round()
    obs.get_active_players()
    obs.get_asked_amount()
    obs.get_max_raise()
    obs.get_max_spent()
    obs.get_min_raise()
    obs.get_player_count()
    return 1