from gym.envs.registration import register

from .envs.game import XOGame, XOChoice
from . import envs


register(
    id="XoGame-V0",
    entry_point= "xogame.envs:XOGame", 
    max_episode_steps= 2000
)