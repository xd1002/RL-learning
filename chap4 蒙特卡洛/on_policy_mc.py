# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 16:13:03 2021

@author: Lenovo
"""

import gym
import numpy as np
from gym import spaces
from collections import defaultdict

def epsilon_greedy_policy(nA,Q,epsilon):
    def policy_fn(state):
        policy=np.ones(nA)*epsilon/nA
        action=np.argmax(Q[state])
        policy[action]+=1-epsilon
        return policy
    return policy_fn

def on_policy_mc(env,epsilon,num_episode,discount=1):
    Q=defaultdict(lambda:np.zeros(env.action_space.n))
    policy=epsilon_greedy_policy(env.nA,Q,epsilon)
    
    return_counts=defaultdict(float)
    return_sum=defaultdict(float)
    
    for i in range(num_episode):
        if i%1000==0:
            print('已进行迭代次数：',i)
        episode=[]
        state=env._reset()
        for j in range(100):
            prob=policy(state)
            action=np.random.choice(np.arange(len(prob)),p=prob)
            next_state,reward,done=env._step(action)
            episode.append((state,action,reward))
            if done==True:
                break
            state=next_state
        sa_in_episode=set([(tuple(x[0]),x[1]) for x in episode])
        for state,action in sa_in_episode:
            sa_pairs=(state,action)
            first_index=next(i for i,x in enumerate(sa_in_episode) if x[0]==state and x[1]==action)
            G=sum(x[2]*(discount**i) for i,x in enumerate(episode[first_index:]))
            return_sum[sa_pairs]+=G
            return_counts[sa_pairs]+=1
            Q[state][action]=return_sum[sa_pairs]/return_counts[sa_pairs]
    return policy,Q
    