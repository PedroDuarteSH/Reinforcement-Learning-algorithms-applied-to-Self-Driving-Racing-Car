import gym
import numpy as np
from stable_baselines3 import A2C
import torcs_env
from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.env_checker import check_env
env = gym.make("Torcs-v0")


# The noise objects for DDPG
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))
print(n_actions)
model = A2C("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=1000_000, progress_bar=True)
model.save("a2c_carro")
model = A2C.load("a2c_carro", env=env)

env.show_results()
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    #action = env.action_space.sample()
    print(action)
    obs, rewards, done, info = env.step(action[0])
    if(done):
        break
    env.render()
    