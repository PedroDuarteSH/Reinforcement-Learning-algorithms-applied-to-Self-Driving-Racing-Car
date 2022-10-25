import gym
import random
import torcs_env
def main():
    env = gym.make("Torcs-v0", render_mode = "human")
    states = env.observation_space
    actions = env.action_space
    print(actions)

    episodes = 10
    for episode in range(1, episodes + 1):
        env.reset()
        done = False
        score = 0
        
        while not done:
            env.render()
            action = env.action_space.sample()
            n_state, reward, terminated, truncated, info = env.step(action)
            done = terminated

            score += reward
        print(f'Episode: {episode} Score: {score} ')
 
if __name__ == "__main__":
    main()

