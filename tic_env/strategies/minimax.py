import tic_env

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tic_env.envs import TicTacToeEnv


import numpy as np
from copy import deepcopy


class MiniMaxStartegy:

    def minimax(self, env, state, depth, is_max_player):
        done = env.game.is_done()
        if done:
            return env.game.get_reward()

        if is_max_player:
            max_eval = -float("inf")
            for action in env.game.get_allowed_actions():
                next_state, _, _, _ = env.step(action)
                eval = self.minimax(env, next_state, depth + 1, False)
                max_eval = max(max_eval, eval)
                env.undo_action()
            return max_eval
        else:
            min_eval = float("inf")
            for action in env.game.get_allowed_actions():
                next_state, _, _, _ = env.step(action)
                eval = self.minimax(env, next_state, depth + 1, True)
                min_eval = min(min_eval, eval)
                env.undo_action()
            return min_eval

    def find_best_move(self, env):
        best_move = None
        best_value = -float("inf")

        denv = deepcopy(env)
        
        for action in denv.game.get_allowed_actions():
            next_state, _, _, _ = denv.step(action)
            move_value = self.minimax(denv, next_state, 0, True)
            denv.undo_action()
            
            # print(action, ":", move_value)
            
            if move_value >= best_value:
                best_value = move_value
                best_move = action

        return best_move


