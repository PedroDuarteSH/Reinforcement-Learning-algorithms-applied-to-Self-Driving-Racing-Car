import gym
import random
import torcs_env
def main():
    env = gym.make("Torcs-v0")
    states = env.observation_space
    actions = env.action_space
    print(actions)

    episodes = 10
    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False
        score = 0
        while not done:
            env.render()
            action = random.choice([0, 1])
            n_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            score += reward
        print(f'Episode: {episode} Score: {score} ')
 
if __name__ == "__main__":
    main()

