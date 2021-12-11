# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 09:55:32 2021

@author: Lenovo
"""

import numpy as np
import random

class td0():
    def __init__(self,env,discount,epsilon,episode_num,alpha):
        self.env=env
        self.action_space=self.env.action_space
        self.q={}
        self.epsilon=epsilon
        self.episode_num=episode_num
        self.alpha=alpha
        self.discount=discount
        
    #根据当前q函数和给定observation通过ε-greedy选择行为
    def get_action(self,observation):
        self.state_in_dict(observation)
        max_value,best_index=self.get_best(self.q[observation])
        best_action_index=random.choice(best_index)
        p=[self.epsilon/4]*4
        p[best_action_index]+=1-self.epsilon
        action=np.random.choice([0,1,2,3],p=p)
        return action
    
    def state_in_dict(self,state):
        if not self.q.__contains__(state):
            self.q[state]=[0]*len(self.action_space)
        
        
    #q为list，返回这个list中的最大值以及所有最大值的index
    def get_best(self,q):
        max_value=max(q)
        best_index=[]
        for i in range(len(q)):
            if q[i]==max_value:
                best_index.append(i)
        return max_value,best_index
    
    #
    def learn(self):
        for i in range(self.episode_num):
            print(i)
            state=tuple(self.env.reset())
            action=self.get_action(state)

            self.state_in_dict(state)
            while True:
                self.env.render()
                s_,reward,done=self.env.step(action)
                if done==True:
                    self.q[state][action]+=self.alpha*reward
                    break
                else:
                    s_=tuple(s_)
                    action_=self.get_action(s_)
                    self.q[state][action]+=self.alpha*(reward+self.discount*self.q[s_][action_]-self.q[state][action])
                state=s_
                action=action_
                
        self.policy=[[],[],[],[],[]]
        for i in range(5):
            for j in range(5):
               coord_x_up=5+40*i
               coord_x_down=35+40*i
               coord_y_up=5+40*j
               coord_y_down=35+40*j
               coords=(coord_x_up,coord_y_up,coord_x_down,coord_y_down)
               if coords in self.q.keys():
                   max_value,best_index=self.get_best(self.q[coords])
                   self.policy[i].append(best_index)
               elif coords in [tuple(self.env.canvas.coords(self.env.hell1)),
                                  tuple(self.env.canvas.coords(self.env.hell2)),
                                  tuple(self.env.canvas.coords(self.env.hell3)),
                                  tuple(self.env.canvas.coords(self.env.hell4)),
                                  tuple(self.env.canvas.coords(self.env.hell5)),
                                  tuple(self.env.canvas.coords(self.env.hell6)),
                                  tuple(self.env.canvas.coords(self.env.hell7))]:
                   self.policy[i].append([-1])
               else:
                   self.policy[i].append([0,1,2,3])
                
        return self.policy   
                