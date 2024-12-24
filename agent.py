import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
from game import Game

class ValueNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(18, 128)
        self.l2 = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = self.l2(x)
        return x
    
class PolicyNet(nn.Module):
    def __init__(self, action_size):
        super().__init__()
        self.l1 = nn.Linear(18, 128)
        self.l2 = nn.Linear(128, action_size)

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = F.softmax(self.l2(x), dim=1)

        return x
    
class Agent:
    def __init__(self):
        self.gamma = 0.98
        self.lr_pi = 0.0002
        self.lr_v = 0.0005
        self.action_size = 3
        # actionは"call",fold","raise"のみとする
        self.pi = PolicyNet(self.action_size)
        self.v = ValueNet()
        
        self.optimizer_pi = optim.Adam(self.pi.parameters(), lr=self.lr_pi)
        self.optimizer_v = optim.Adam(self.v.parameters(), lr=self.lr_v)

    def get_action(self, state,mask):
        state = torch.tensor(state[np.newaxis, :], dtype=torch.float32)
        mask = torch.tensor(mask,dtype=torch.float32)
        probs = self.pi(state)
        probs = probs[0]
        probs = probs * mask
        m = Categorical(probs)
        action = m.sample().item()
        return action, probs[action]

    def update(self, state, action_prob, reward, next_state, player_done):
        state = torch.tensor(state[np.newaxis, :], dtype=torch.float32)

        if player_done:
            target = torch.tensor(reward, dtype=torch.float32)
        else:
            next_state = torch.tensor(next_state[np.newaxis, :], dtype=torch.float32)
            target = reward + self.gamma * self.v(next_state)

        target.detach()
        v = self.v(state)
        loss_fn = nn.MSELoss()
        loss_v = loss_fn(v, target)

        delta = target - v
        loss_pi = -torch.log(action_prob) * delta.item()
        loss_pi = loss_pi.float()

        self.optimizer_v.zero_grad()
        self.optimizer_pi.zero_grad()
        loss_v.backward()
        loss_pi.backward()
        self.optimizer_v.step()
        self.optimizer_pi.step()

    def copy_from(self, other_agent):
        # other_agent からパラメータをコピー
        self.pi.load_state_dict(other_agent.pi.state_dict())
        self.v.load_state_dict(other_agent.v.state_dict())

        self.optimizer_pi.load_state_dict(other_agent.optimizer_pi.state_dict())
        self.optimizer_v.load_state_dict(other_agent.optimizer_v.state_dict())