import gym
from gym import spaces
import numpy as np
from gym_tank.envs.pytank_2d import PyTank2D
import pygame

class TankEnv(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self):
        print("init")
        # 0:left, 1:right, 2:up, 3:down
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.array([-12, -8, 0]), np.array([12, 8, 120]), dtype=np.int)
        self.is_view = True
        self.pytank = PyTank2D(self.is_view)
        self.mode = 0
        self.memory = []

    def reset(self):
        del self.pytank
        if self.mode == 0:
            self.pytank = PyTank2D(self.is_view)
        else:
            self.pytank = PyTank2D(self.is_view)
        obs = self.pytank.observe()
        return obs

    def step(self, action):
        self.pytank.action(action)
        reward = self.pytank.evaluate()
        done = self.pytank.is_done()
        obs = self.pytank.observe()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        if self.is_view:
            self.pytank.view()

    def set_view(self, flag):
        self.is_view = flag

    def set_mode(self, mode):
        self.mode = mode

    def save_memory(self, file):
        np.save(file, self.memory)
        print("history saved")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def make_input(self, input):
        return np.reshape(input, [1, len(input)])
