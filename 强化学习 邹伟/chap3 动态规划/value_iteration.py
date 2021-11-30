# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 11:55:43 2021

@author: Lenovo
"""

import numpy as np

def get_max_index(action_value):
    max_index=[]
    policy_arr=np.zeros(len(action_value))
    max_value=np.max(action_value)
    for i in range(len(action_value)):
        if action_value[i]==max_value:
            max_index.append(action_value[i])
            policy_arr[i]=1
    
    return max_index,policy_arr

def value_iteration(env,discount=1,threshold=0.00001):
    
    def calculate_Q_function(state,V):
        q=np.zeros(env.nA)
        for a in range(env.nA):
            for prob,next_state,reward,done in env.P[state][a]:
                q[a]+=reward+prob*discount*V[next_state]
                
        return q
    
    policy=np.ones((env.nS,env.nA))/env.nA
    V=np.zeros(env.nS)
    
    iter_num=0
    
    while True:
        max_diff=0
        for s in range(env.nS):
            q=calculate_Q_function(s,V)
            v=np.max(q)
            max_diff=max(max_diff,np.abs(v-V[s]))
            V[s]=v
        if max_diff<=threshold:
            print('The best state value function has been found!')
            break
        iter_num+=1
        print(iter_num)
        
    for s in range(env.nS):
        q=calculate_Q_function(s,V)
        max_index,policy_arr=get_max_index(q)
        policy[s]=policy_arr
    return policy,V
