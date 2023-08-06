import numpy as np

from poker_game_runner.infostate import Observation

def get_name():
    return "callBot"

def act(observation: Observation):
    return 1