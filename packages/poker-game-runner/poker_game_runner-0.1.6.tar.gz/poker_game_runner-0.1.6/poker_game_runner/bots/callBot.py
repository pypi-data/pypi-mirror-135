import numpy as np

from poker_game_runner.state import Observation

def get_name():
    return "callBot"

def act(observation: Observation):
    return 1