from operator import mod
import gym
import random
import torcs_env
import numpy as np

from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise


def main():
    env = gym.make("Torcs-v0", render_mode = "human")
    states = env.observation_space
    actions = env.action_space
    # the noise objects for DDPG
    #n_actions = 3
    #action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

    #model = DDPG("MlpPolicy", env, action_noise=action_noise, verbose=1)
    #model.learn(total_timesteps=10000, log_interval=10)
    for i in range(10):
        obs = env.reset()
        
        while True:
            #action, _states = model.predict(obs)
            action = env.action_space.sample()
            obs, rewards, terminated, info = env.step(action)
            
            env.render()
            
            if(terminated):
                print("HEre")
                break



if __name__ == "__main__":
    main()

###