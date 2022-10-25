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
        self.firstEpisode = True
        
        if render_mode == "human":
            self.training = False
        else:
            self.training = True
        # Define action and observation space
        # They must be gym.spaces objects
        self.client = TorcsClient(self.training)
        
        torcsActions = {
            'accel' : spaces.Box(low=0, high=1),
            'break' : spaces.Box(low=0, high=1),
            'steer' : spaces.Box(low=-1, high=1),
            'clutch' : spaces.Box(low=0, high=1),
            'focus' : spaces.Box(low=-90, high=90),
            'gear' : spaces.Discrete(7, start= -1),
            # Used to terminate Race
            #'meta' : spaces.Discrete(n=2)
        }
        
        self.action_space = spaces.Dict(torcsActions)

        # Parameters Recieved
        # Angle, CurrentLapTime, Damage, DistanceFromStart, DistanceRaced, Fuel, Gear, LastLapTime, Opponents * 36?
        # Race Position, RPM, SpeedX, SpeedY, Speedz?, Track Sensors * 19, z?, Focus * 5
        
        #To use: Gear, DistanceFromStart, DistanceRaced, Gear, RPM, Track Sensors 
        torcsSpaces = {
            'angle' : spaces.Box(low=-np.pi, high=np.pi),
            'curLapTime' : spaces.Box(low = 0, high=float("+inf")),
            'damage' : spaces.Box(low=0, high= float("+inf")),
            'distFromStart' : spaces.Box(low=0, high=float("+inf")),
            'distRaced' : spaces.Box(low = 0, high=float("+inf")),
            'fuel': spaces.Box(low=0, high=float("+inf")),
            'gear' : spaces.Discrete(7, start= -1),
            'lastLapTime' : spaces.Box(low=0, high=float("+inf")),
            'opponents' : spaces.Box(low=0, high=200, shape=(36, )),
            'racePos' : spaces.Discrete(20, start=1),
            'rpm' : spaces.Box(low=0, high=float("+inf")),
            'speedX': spaces.Box(low = float("-inf"), high=float("+inf")),
            'speedY': spaces.Box(low = float("-inf"), high=float("+inf")),
            'speedZ': spaces.Box(low = float("-inf"), high=float("+inf")),
            'track' : spaces.Box(low=0, high=200, shape=(19, )),
            'trackPos': spaces.Box(low = float("-inf"), high=float("+inf")),
            'wheelSpinVel' : spaces.Box(low = 0, high=float("+inf")),
            'z': spaces.Box(low = float("-inf"), high=float("+inf")),
            'focus': spaces.Box(low= 0, high=200, shape=(5,)),
        }
        
        self.observation_space = spaces.Dict(torcsSpaces)
    
        self.previousObservation = None


    def step(self, action):
        action['gear'] = [action['gear']]
        observation  = self.client.recieveMessage()
        reward = self.reward(float(observation['speedX'][0]), float(observation['distRaced'][0]), float(observation['angle'][0]), float(observation['distFromStart'][0]))
        info = {}
        # Put if wall etc, now just to try
        terminated = self.checkTerminated(observation)
        self.client.sendMessage(action)

        self.previousObservation = observation
        return observation, reward, terminated, 0, info
    
    
    
    
    def reset(self, ):
        if self.firstEpisode:
            self.firstEpisode = False
        # Reset the state of the environment to an initial state
        else:
            self.client.kill()
            self.client = TorcsClient(self.training)
            ...
        
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...
        
    
    def checkTerminated(self, observation):
        
        # Vehicle is damaged
        if int(observation['damage'][0]) > 0:
            print("Got Damage")
            return 1
        # Vehicle is out of track
        if np.min(observation['track']) < 0:
            print("Out of Track")
            return 1
        # Vehicle is oriented Backwards
        if np.cos(observation['angle']) < 0:
            print("Angle " + observation['gear'])
            return 1
            
        if self.previousObservation != None:
            #Compare with previous to see progress
            ...
            
            
        return 0
        
    
        
    def reward(self, speed,trackpos,angle,dist):
        stuck = 0
        SOOT = 0
        OOT = 0
        if np.abs(trackpos)>=0.98:
            OOT=1   
        elif np.abs(trackpos)>=0.75:
            SOOT=1    
            
        Rspeed=np.power((speed/float(160)),4)*0.05
        Rtrackpos=np.power(1/(float(np.abs(trackpos))+1),4)*0.7
        Rangle=np.power((1/((float(np.abs(angle))/40)+1)),4)*0.25

        if stuck==1:
            Reward=-2
        elif SOOT==1:
            Reward=(Rspeed+Rtrackpos+Rangle)*0.5
        elif OOT==1:
            if np.abs(trackpos) >=1.5:
                Reward=-1.5
            else:
                Reward=np.abs(trackpos)*(-1)
        else:
            Reward=Rspeed+Rtrackpos+Rangle
        return Reward