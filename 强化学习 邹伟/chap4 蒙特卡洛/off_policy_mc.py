# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 11:02:51 2021

@author: Lenovo
"""
import numpy as np
import gym
from collections import defaultdict

def create_random_policy(nA):
    A=np.ones(nA)/nA
    def policy_fn(state):
        return A
    return policy_fn

def greedy_policy(Q):
    def policy_fn(state):
        A=np.zeros_like(Q[state],dtype=float)
        index=np.argmax(Q[state])
        A[index]=1
        return A
    return policy_fn

def off_policy_mc(env,behavior_policy,epsilon,num_episode,discount=1):
    Q=defaultdict(lambda:np.zeros(env.action_space.n))
    target_policy=greedy_policy(Q)
    C=defaultdict(lambda:np.zeros(env.action_space.n))
    
    for i_episode in range(num_episode):
        if i_episode%1000==0:
            print('episode generated:',i_episode)
        episode=[]
        state=env._reset()
        
        for i in range(100):
            probs=behavior_policy(state)
            action=np.random.choice(np.arange(len(probs)),p=probs)
            next_state,reward,done=env._step(action)
            episode.append((state,reward,done))
            if done==True:
                break
            state=next_state
        G=0
        W=1
        for t in range(len(episode))[::-1]:
            state,reward,done=episode[t]
            G+=discount*G+reward
            C[state][action]+=W
            Q[state][action]+=W/C[state][action]*(G-Q[state][action])
            if action!=np.argmax(target_policy(state)):
                break
            W=W/behavior_policy(state)[action]
            
    return target_policy,Q
