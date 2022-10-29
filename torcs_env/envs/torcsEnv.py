from re import S
import gym
from gym import spaces
import numpy as np
from torcs_env.envs.client import TorcsClient

class TorcsEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {"render_modes": ["human", "training"]}

    def __init__(self, render_mode=None):
        super(TorcsEnv, self).__init__()
        self.connected = False
        if render_mode == "human":
            self.training = False
        else:
            self.training = True
        # Define action and observation space
        # They must be gym.spaces objects
        self.client = TorcsClient(self.training)
        self.stuck = 0
        torcsActions = {
            'accel' : spaces.Box(low=0, high=1, shape = (1, )),
            'break' : spaces.Box(low=0, high=1, shape = (1, )),
            'steer' : spaces.Box(low=-1, high=1, shape = (1, )),
        }
        
        # Box 2, 1 action
        # 1 - Break / Accel
        # 2 - Steering        
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,))

        # Parameters Recieved
        # Angle, CurrentLapTime, Damage, DistanceFromStart, DistanceRaced, Fuel, Gear, LastLapTime, Opponents * 36?
        # Race Position, RPM, SpeedX, SpeedY, Speedz?, Track Sensors * 19, z?, Focus * 5
        
        #To use: Gear, DistanceFromStart, DistanceRaced, Gear, RPM, Track Sensors 
        torcsSpaces = {
            'angle' : spaces.Box(low=-np.pi, high=np.pi, shape = (1, )),
            #'curLapTime' : spaces.Box(low = 0, high=float("+inf"), shape = (1, )),
            #'damage' : spaces.Box(low=0, high= float("+inf"), shape = (1, )),
            #'distFromStart' : spaces.Box(low=0, high=float("+inf"), shape = (1, )),
            #'distRaced' : spaces.Box(low = 0, high=float("+inf"), shape = (1, )),
            #'fuel': spaces.Box(low=0, high=float("+inf"), shape = (1, )),
            #'gear' : spaces.Discrete(7),
            #'lastLapTime' : spaces.Box(low=0, high=float("+inf"), shape = (1, )),
            #'opponents' : spaces.Box(low=0, high=200, shape=(36, )),
            #'racePos' : spaces.Discrete(20),
            #'rpm' : spaces.Box(low=0, high=float("+inf"), shape = (1, )),
            'speedX': spaces.Box(low = float("-inf"), high=float("+inf"), shape = (1, )),
            #'speedY': spaces.Box(low = float("-inf"), high=float("+inf"), shape = (1, )),
            #'speedZ': spaces.Box(low = float("-inf"), high=float("+inf"), shape = (1, )),
            'track' : spaces.Box(low=0, high=200, shape=(19, )),
            #'trackPos': spaces.Box(low = float("-inf"), high=float("+inf"), shape = (1, )),
            #'wheelSpinVel' : spaces.Box(low = 0, high=float("+inf"), shape = (4, )),
            #'z': spaces.Box(low = float("-inf"), high=float("+inf"), shape = (1, )),
            #'focus': spaces.Box(low= 0, high=200, shape=(5,)),
        }
        
        self.observation_space = spaces.Dict(torcsSpaces)
        self.previousObservation = None

    def step(self, action):
        if not self.connected:
            self.connected = True
        action = self.processAction(action)
        
        observation  = self.client.recieveMessage()
        if observation == {}:
            
            observation  = self.reset()
            observation  = self.client.recieveMessage()
        action['gear'] = [self.gear(observation['gear'][0], observation['rpm'][0])]
        reward = self.reward(observation)
        info = {}
        # Put if wall etc, now just to try
        terminated = self.checkTerminated()
        #if(terminated):
        #    action['meta'] = [1]
        self.client.sendMessage(action)

        self.previousObservation = observation
        return self.process_obs(observation), reward, terminated, info
    
    
    # Create Dictionary from action
    def processAction(self, action):
        if action.shape == (1, 2):
            return {}
        output = {}
        if(action[0] > 0):
            output['accel'] = [action[0]]
        else:
            output['break'] = [-action[0]]
        output['steer'] = [action[1]]
    
        return output
    
   
    
    
    def show_results(self):
        self.training = False
    
    def reset(self):
        self.client.restart(self.training)
        
        obs = self.step(np.array([0, 0, 0, 0]))[0]
        
        return self.process_obs(obs)
        
    def process_obs(self, obs):
        observation = {}
        observation['angle'] = obs['angle']
        observation['track'] = obs['track']
        observation['speedX'] = obs['speedX']
        return observation
        
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...
        
    def checkTerminated(self):
       
        if self.stuck == 25:
            return 1
        return 0
    
        
    def reward(self, observation):
        speed = observation['speedX'][0]
        trackpos = observation['trackPos'][0]
        angle = np.degrees(observation['angle'][0])
        dist = observation['distRaced'][0]
        is_stuck = False
        
        #print(speed, trackpos, angle, dist)
        if (np.abs(angle) >= 45 and speed<10) or (speed<3 and dist>10):
            self.stuck += 1
            return -2
        else:
            self.stuck = 0
        
        
        
        Reward = speed * np.cos(angle)  - speed * np.sin(angle) - speed * np.abs(trackpos)
        
        if(speed < 3):
            return -100
            
        
       
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