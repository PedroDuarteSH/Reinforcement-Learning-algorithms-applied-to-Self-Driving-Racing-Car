from gym.envs.registration import register

register(
    id='Torcs-v0',
    entry_point='torcs_env.envs:TorcsEnv',
)