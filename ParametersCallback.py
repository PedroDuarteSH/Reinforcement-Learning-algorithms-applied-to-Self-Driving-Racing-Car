from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import HParam
import os
import numpy as np


class ParametersCallback(BaseCallback):
    def __init__(self):
        """
        Saves the hyperparameters and metrics at the start of the training, and logs them to TensorBoard.
        """
        super().__init__()
        self.episodes = 0
        self.speed_mean = 0
        self.angle_mean = 0
        self.step_count = 0
        

    def _on_training_start(self) -> None:
        hparam_dict = {
            "algorithm": self.model.__class__.__name__,
            "learning rate": self.model.learning_rate,
            "gamma": self.model.gamma,
            "tau": self.model.tau,
            "batch size": self.model.batch_size,
            "buffer size": self.model.buffer_size,
            "learning start": self.model.learning_starts,

            }
        # define the metrics that will appear in the `HPARAMS` Tensorboard tab by referencing their tag
        # Tensorbaord will find & display metrics from the `SCALARS` tab
        metric_dict = {
            "rollout/ep_len_mean": 0,
            "train/value_loss": 0,
        }
        self.logger.record(
            "hparams",
            HParam(hparam_dict, metric_dict),
            exclude=("stdout", "log", "json", "csv"),
        )

    

    def _on_rollout_end(self) -> None:
        logger_name = self.logger.dir.split("/")[-1]
        self.episodes += 1

        if self.episodes % 10000 == 0:
            self.model.save(f"logs/{logger_name}/model_{self.n_calls}")
        
        
    def _on_step(self) -> bool:
        # log the metrics
        observation = self.training_env.buf_obs[None][0]
        self.step_count += 1
    
        speed = observation[20]
        angle = observation[0]
        self.speed_mean += speed
        self.angle_mean += np.abs(angle)
        
        return True