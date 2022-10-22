from re import S
import gym
from gym import spaces
import numpy as np

from torcs_env.envs.client import TorcsClient

class TorcsEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(TorcsEnv, self).__init__()
        
        # Define action and observation space
        # They must be gym.spaces objects
        self.client = TorcsClient()
        self.client.connect()
        torcsActions = {
            'accel' : spaces.Box(low=0, high=1),
            'break' : spaces.Box(low=0, high=1),
            'steering' : spaces.Box(low=-1, high=1),
        }
        
        self.action_space = spaces.Dict(torcsActions)

        # Parameters Recieved
        # Angle, CurrentLapTime, Damage, DistanceFromStart, DistanceRaced, Fuel, Gear, LastLapTime, Opponents * 36?
        # Race Position, RPM, SpeedX, SpeedY, Speedz?, Track Sensors * 19, z?, Focus * 5
        
        #To use: Gear, DistanceFromStart, DistanceRaced, Gear, RPM, Track Sensors 
        torcsSpaces = {
            'gear' : spaces.Discrete(7, start= -1),
            'angle' : spaces.Box(low=-np.pi, high=np.pi),
            'distFromStart' : spaces.Box(low=0, high=float("+inf")),
            'distRaced' : spaces.Box(low = 0, high=float("+inf")),
            'track' : spaces.Box(low=0, high=200, shape=(19, ))
        }
        
        self.observation_space = spaces.Dict(torcsSpaces)
        
        
        self.isStuckCount = 0



    def step(self, action):
        send_to_sv =  {
            'accel' : [1],
            'brake' : [0],
            'gear'  : [1],
            'clutch': [0],
            'meta'  : [False],
            'focus' : [0]
        }
        
       
        
        observation = self.client.recieveMessage()
        
        reward = self.reward(1, 1, 1, 1)
        info = None
        # Put if wall etc, now just to try
        terminated = False
        self.client.sendMessage(send_to_sv)
        
        return observation, reward, terminated, False, info
       
    def reset(self):
        # Reset the state of the environment to an initial state
        self.client.restart_race()
        
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...
        
        
        
    def reward(self, speed,trackpos,angle,dist):
        stuck = 0
        SOOT = 0
        OOT = 0
        if np.abs(trackpos)>=0.98:
            OOT=1   
        elif np.abs(trackpos)>=0.75:
            SOOT=1    
            
        if (np.abs(angle) >= 45 and speed<10) or (speed<3 and dist>20):
            self.isStuckCount += 1
            if self.isStuckCount==25:
                stuck=1
                self.isStuckCount=0
        else:
            self.isStuckCount
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
        print("Reward = "+str(Reward))
        return Reward