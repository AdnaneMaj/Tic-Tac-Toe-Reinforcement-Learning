import tic_env
from tic_env.tic_game import PlayerId
import gymnasium as gym

from tic_env.warppers import MiniMaxEnv


env = gym.make("tic_env/TicTacToe-v0").unwrapped

menv = MiniMaxEnv(env=env)
menv.reset(player_id=PlayerId.O)

menv.render()

done = False


while not done:

    action = int(input("> "))

    menv.step(action=action)

    menv.render()