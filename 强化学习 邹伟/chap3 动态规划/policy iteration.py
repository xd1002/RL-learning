# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:35:58 2021

@author: Lenovo
"""

import numpy as np
def policy_eval(policy,env,threshold=0.0001,discount=1):
    V=np.zeros(env.nS)
    iter_num=0
    
    while True:
        max_diff=0
        for s in range(env.nS):
            v=0
            for a,action_prob in enumerate(policy[s]):
                for prob,next_state,reward,done in env.P[s][a]:
                    v+=action_prob*(reward+discount*prob*V[next_state])
                    
            max_diff=max(max_diff,np.abs(v-V[s]))
            V[s]=v
        if max_diff<=threshold:
            break
        iter_num+=1
        print(iter_num)
    return V


def get_max_index(action_value):
    max_value=np.max(action_value)
    policy_value=np.zeros(len(action_value))
    max_index=[]
    for i in range(len(action_value)):
        if action_value[i]==max_value:
            max_index.append(i)
            policy_value[i]=1
            
    return max_index,policy_value


def policy_improvement(env,discount=1):
    policy=np.ones([env.nS,env.nA])/env.nA
    num=0
    
    while True:
        state=True

        V=policy_eval(policy,env,discount=discount)
        for s in range(env.nS):
            max_index_origin=np.argmax(policy[s])
            value_arr=np.zeros(env.nA)
            for a in range(env.nA):
                for prob,next_state,reward,done in env.P[s][a]:
                    value_arr[a]+=reward+discount*prob*V[next_state]
            max_index,policy_value=get_max_index(value_arr)
            if max_index_origin not in max_index:
                state=False
            policy[s]=policy_value
        num+=1        
        if state==True:
            print('iter end,final iter num:',num)
            break
        if num%10==0:
            print('policy improvement iter time:',num)
    return policy
