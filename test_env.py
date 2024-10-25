import tic_env
import gymnasium as gym


env = gym.make("tic_env/TicTacToe-v0").unwrapped



obv = env.reset()


rewards = 0

done = False

for i in range(3):

    env.reset()

    while not done:

        action = env.sample_action()

        # print(env.game.get_allowed_actions())
        # print(action)

        next_state, reward, done, _ = env.step(action=action)

        rewards += reward

        # env.render()

print("Totale_rewards", rewards)