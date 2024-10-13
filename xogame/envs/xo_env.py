import gym 
from gym import spaces
from .game import XOChoice, XOGame

import numpy as np 


class XOGameEnv(gym.Env):
    def __init__(self):
        super(XOGameEnv, self).__init__()

        self.observation_space = spaces.Box(low=-1, high=1, shape=(9,), dtype=np.int8)

        self.action_space = spaces.Discrete(9)

        self.game = XOGame()

        self.current_player = 1

        self.done = False
    
    def reset(self):
        self.game.reset()
        self.current_player = 1
        self.done = False
        return self.game.states

    def step(self, action):

        if self.done:
            print("📢 Game has already finished. Please reset the environment.")

        if self.current_player == XOChoice.X.value:
            self.game.play(XOChoice.X, pos=action)
        else:
            self.game.play(XOChoice.O, pos=action)

        
        win = self.game.check_winner(player= self.current_player)

        if win:
            self.done = True
            reward = 1
        else:
            reward = 0
            self.current_player *= -1

        return self.game.states, reward, self.done

    def render(self):
        self.game.render()


