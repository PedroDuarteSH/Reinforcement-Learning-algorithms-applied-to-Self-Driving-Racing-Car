import gym
import numpy as np
from stable_baselines3 import A2C
import torcs_env
from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.callbacks import CheckpointCallback

env = gym.make("Torcs-v0", render_mode="human")


# The noise objects for DDPG

n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

model = DDPG("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=5000000, progress_bar=True)
model.save("DDPG")
model = DDPG.load("DDPG", env=env)

env.show_results()
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    print(action)
    obs, rewards, done, info = env.step(action)
    print(obs)
    #if(done):
    #    break
    env.render()
    