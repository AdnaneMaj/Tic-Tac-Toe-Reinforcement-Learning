from xogame.envs.game import XOGame, XOChoice
import xogame
import numpy as np

import gym


env = xogame.envs.XOGameEnv()

done = False
env.render()

while True:

    if done: 
        print("player: ", env.current_player, " win the game")
        break

    
    print("Current player: ", "x" if env.current_player == 1 else "o")

    pos = int(input("pos = "))

    states, reward, done = env.step(action=pos)
    
    env.render()