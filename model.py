import gym
import torcs_env
from stable_baselines3 import DQN, A2C, DDPG
import torch.nn as nn
import os

import argparse

import ParametersCallback


class Model():
    def __init__(self, args) -> None:
        self.algorithm = args.a
        self.showResult = args.s
        self.modelName = args.m
        self.training_timesteps = args.t
        self.log_interval = args.l
        self.progress_bar = args.p
        self.save_model_dir = args.d
        self.verbose = args.v
        self.batch_size = args.b
        self.exploration_fraction = args.e
        self.tensorFlowLogDir = args.td
        self.use_custom_network = args.n
        if(self.algorithm == "DQN"):
            self.env = gym.make("Torcs-v0", discrete_action=True)
        else:
            self.env = gym.make("Torcs-v0", discrete_action=False)
        self.model = None
        self.callback = None

        if(args.ed == True):
            self.env.show_results()
        pass

    def use_custom_net(self):
        if self.algorithm == "DQN":
             net_arch = [256, 256, 256, 100]
        else:
            pi_layers = [64, 32, 20]
            vf_layers = [64, 32, 16]
            qf_layers = [64, 32, 20]
            net_arch =  dict(pi=pi_layers, vf=vf_layers, qf=qf_layers)
       
        policy_kwargs = dict( net_arch=net_arch, activation_fn=nn.ReLU, )
        return policy_kwargs

    def createModel(self):
        policy_kwargs = self.use_custom_net() if self.use_custom_network else None
        if self.algorithm == "DQN":
            self.model = DQN("MlpPolicy", self.env, verbose=self.verbose, batch_size=self.batch_size, exploration_fraction=self.exploration_fraction)
        elif self.algorithm == "A2C":
            self.model = A2C("MlpPolicy", self.env, verbose=self.verbose, policy_kwargs=policy_kwargs, batch_size=self.batch_size)
        elif self.algorithm == "DDPG":
            self.model = DDPG("MlpPolicy", self.env, verbose=self.verbose, policy_kwargs=policy_kwargs, batch_size=self.batch_size)
    def createCallback(self):
        self.callback = ParametersCallback.ParametersCallback()

    def trainModel(self):
       self.model.learn(total_timesteps=self.training_timesteps, log_interval=self.log_interval, callback=self.callback, tb_log_name=self.tensorFlowLogDir, progress_bar=self.progress_bar)
        
    def showResults(self):
        path = self.save_model_dir + self.modelName
        model = DQN.load(path)
        self.env.show_results()
        obs = self.env.reset()
        while True:
            action, _state = model.predict(obs)
            obs, rewards, done, info = self.env.step(action)
            self.env.render()

    def saveModel(self):
        path = self.save_model_dir + self.modelName
        count = 1
        while os.path.exists(path):
            path += "_" + str(count)
            count += 1
        self.model.save(path)
