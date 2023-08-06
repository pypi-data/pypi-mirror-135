import numpy as np
import pyspiel
from poker_game_runner.state import InfoState
from typing import List, Tuple
from collections import namedtuple

BlindScheduleElement = namedtuple('BlindScheduleElement', 'next_blind_change small_blind big_blind ante')
Player = namedtuple('Player', 'bot_impl stack')

def play_hand(players: List[Player], blinds: List[int]):

    game = pyspiel.load_game("universal_poker", {
        "betting": "nolimit",
        "bettingAbstraction": "fullgame",
        "numPlayers": len(players),
        "stack": " ".join(str(player.stack) for player in players),
        "blind": " ".join(str(blind) for blind in blinds),
        "numRounds": 4,
        "numHoleCards": 2,
        "numBoardCards": "0 3 1 1",
        "numSuits": 4,
        "numRanks": 13,
        "firstPlayer": "3 1 1 1" if len(players) > 2 else "1 1 1 1"
    })
    state = game.new_initial_state()

    #deal private cards
    while state.is_chance_node():
        state.apply_action(np.random.choice(state.legal_actions()))
        continue

    info_state = InfoState(state.history(), [p.stack for p in players], [b for b in blinds])

    while not state.is_terminal():
        if state.is_chance_node():
            card_num = np.random.choice(state.legal_actions())
            state.apply_action(card_num)
            info_state.update_info_state_draw(card_num)
            continue
        
        current_idx = state.current_player()
        observation = info_state.to_observation(current_idx, state.legal_actions())
        action = players[current_idx].bot_impl.act(observation)
        if not action in state.legal_actions():
            if 0 in state.legal_actions():
                action = 0
            else:
                action = 1
        state.apply_action(action)
        info_state.update_info_state_action(current_idx, action)

    return map(int, state.rewards())

def play_tournament_table(bots, start_stack: int, blind_schedule: Tuple[BlindScheduleElement]):

    active_players = [Player(bot,start_stack) for bot in bots]
    np.random.shuffle(active_players)

    results = []
    hand_count = 0
    blinds_iter = iter(blind_schedule)
    current_blinds = next(blinds_iter)
    if current_blinds.big_blind > start_stack:
        print("big_blind cannot be bigger than start_stack")
        return []

    while len(active_players) > 1:
        print(sorted([player.bot_impl.get_name() for player in active_players]))

        rewards = play_hand(active_players, get_blinds_input(current_blinds, len(active_players)))

        if hand_count == current_blinds.next_blind_change:
            current_blinds = next(blinds_iter)

        defeated_players, active_players = update_active_players(active_players, rewards, current_blinds.big_blind)

        results = results + defeated_players
        active_players = active_players[1:] + [active_players[0]]
        hand_count += 1
    
    results = results + [active_players[0].bot_impl.get_name()]
    results.reverse()
    return results

def update_active_players(active_players: List[Player], rewards: List[int], big_blind: int):    
    updated_players = [Player(player.bot_impl, int(player.stack+r)) for player,r in zip(active_players, rewards)]

    defeated_players = [player.bot_impl.get_name() for player in updated_players if player.stack < big_blind]
    active_players = [player for player in updated_players if player.stack >= big_blind]
    return defeated_players, active_players

def get_blinds_input(current_blinds: BlindScheduleElement, playerCount: int) -> List[int]:
    return [current_blinds.small_blind, current_blinds.big_blind] + ([current_blinds.ante] * (playerCount-2))