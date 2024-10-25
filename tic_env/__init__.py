from gymnasium.envs.registration import register


register(
    id='tic_env/TicTacToe-v0',
    entry_point='tic_env.envs:TicTacToeEnv',
    max_episode_steps=300,
)
