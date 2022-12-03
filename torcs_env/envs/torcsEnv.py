from re import S
import gym
from gym import spaces
import numpy as np
from torcs_env.envs.client import TorcsClient
MAXSPEED = 300

class TorcsEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {"render_modes": ["human", "training"]}

    
    """_summary_:
    Function to init the agent and initialize the client to connect to the server
    Also Gym Variables are initialized
    """
    def __init__(self, render_mode=None, discrete_action=True):
        super(TorcsEnv, self).__init__()
        self.connected = False
        if render_mode == "human":
            self.training = False
        else:
            self.training = True

        self.client = TorcsClient(self.training)
        self.stuck = 0
        self.stuckBeggining = 0
        
        
        
        # Define action and observation space
        if discrete_action:
            self.action_space = spaces.Discrete(n=4)
        else:
            # Box 2, 1 action
            # 1 - Break / Accel
            # 2 - Steering
            self.action_space = spaces.Box(low=-1, high=1, shape=(2,))
        self.time_step = 0

        self.min_reward_limit_start = 300
        self.min_reward_limit = 1
        # Parameters Recieved
        # Angle, CurrentLapTime, Damage, DistanceFromStart, DistanceRaced, Fuel, Gear, LastLapTime, Opponents * 36?
        # Race Position, RPM, SpeedX, SpeedY, Speedz?, Track Sensors * 19, z?, Focus * 5
        # Box 21, 3 observations, 0 - Angle, 1-19- Track Sensors, 20 - Speed,
        self.observation_space = spaces.Box(low=float("0"), high=float("1"), shape=(21,))

    def step(self, action):
        if not self.connected:
            self.connected = True
        
        action = self.processAction(action)
        observation  = self.client.recieveMessage()
        while observation == {}:
            observation  = self.reset()
            observation  = self.client.recieveMessage()
    
        action['gear'] = [self.gear(observation['gear'][0], observation['rpm'][0])]
        reward = self.reward(observation)

        terminated = self.checkTerminated(observation, reward)
        
        self.client.sendMessage(action)
        observation = self.process_obs(observation)
        self.time_step += 1
        self.previousObservation = observation

        if terminated:
            reward = -1000

        return observation, reward, terminated, {}
    

    def getPreviousObservation(self):
        return self.previousObservation
    
    # Create Dictionary from action
    def processAction(self, action):
        output = {}
        # Action -> Continous space
        if action.shape == (4,):
            output['accel'] = [1]
            output['brake'] = [0]
            output['steer'] = [0]

        elif action.shape == (2,):
            if(action[0] > 0):
                output['accel'] = [action[0]]
                output['brake'] = [0]
            else:
                output['accel'] = [0]
                output['brake'] = [action[0]]
            output['steer'] = [action[1]]
        # Action -> Discrete space
        else:
            output['brake'] = [0]
            output['accel'] = [0]
            output['steer'] = [0]
            if(action == 1):
                output['accel'] =[1]
            elif(action == 2):
                output['brake'] = [1]
            elif(action == 3):
                output['steer'] = [-1]
            else:
                output['steer'] = [1]
        return output
    
   
    
    
    def show_results(self):
        self.training = False
    
    def reset(self):
        self.client.restart(self.training)
        self.time_step = 0

        obs = self.step(np.array([0, 0, 0, 0]))[0]
        
        return obs
        
    # Process observation to be used in the model with normalization

    
    def process_obs(self, observation):
        obs = np.zeros(21)
        obs[0] = (observation['angle']+np.pi)/(2*np.pi)
        obs[1:20] = observation['track']/200
        obs[20] = observation['speedX']/MAXSPEED
        return obs
        
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...
        
    def checkTerminated(self, observation, current_reward):
        track = observation['track']
        angle = observation['angle']
        damage = observation['damage']
        #if damage > 0:
        #    return True

        if track.min() < 0:  # Episode is terminated if the car is out of track
            return True


        if self.min_reward_limit_start < self.time_step: # Episode terminates if the progress of agent is small
            if current_reward < self.min_reward_limit:
                return True

        if np.cos(angle) < 0: # Episode is terminated if the agent runs backward
            return True
        
       

        return False
    
        
    def reward(self, observation):
        speed = observation['speedX'][0]
        angle = observation['angle'][0]
  
        Reward = speed * np.cos(angle)

        return Reward

    

    
    
    def gear(self, gear, rpm):
        gearup   =[7000 , 7000 , 7000 , 7000 , 7000 , 0]
        geardown =[0 , 2500 , 3000 , 3000 , 3500 , 3500]
        gear = int(gear)
        rpm = int(rpm)
        if gear < 1 :
            gear = 1 
        if(gear < 6) and (rpm  >= gearup[gear -1]):
            gear = gear +1 ;
        elif(gear > 1) and (rpm <= geardown[gear -1]):
            gear =  gear -1
        return gear