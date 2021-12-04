# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 09:40:51 2021

@author: Lenovo
"""

import gym
from gym import spaces
from gym.utils import seeding

deck=[1,2,3,4,5,6,7,8,9,10,0.5,0.5,0.5]
p_value=0.5
dest=10.5

#根据随机种子从牌队中随机选择一张牌
def draw_card(np_random):
    return np_random.choice(deck)

#随机发到手一张牌
def draw_hand(np_random):
    return [draw_card(np_random)]

#算手中总分
def sum_score(hand):
    return sum(hand)

#算手中牌数
def sum_num(hand):
    return len(hand)

#手牌中人牌数
def sum_p_num(hand):
    count=0
    for i in range(len(hand)):
        if hand[i]==p_value:
            count+=1
    return count

#是否爆牌
def is_bust(hand):
    if sum_score(hand)>10.5:
        return True
    else:
        return False
    
#是否为平牌
def is_pp(hand):
    if sum_score(hand)<10.5:
        return True
    else:
        return False
    
#是否为十点半
def is_sdb(hand):
    if sum_score(hand)==10.5:
        return True
    else:
        return False
    
#是否为五小
def is_wx(hand):
    return True if sum_num(hand)==5 and is_pp(hand) and sum_p_num(hand)<5 else False
            
#是否为天王
def is_tw(hand):
    return True if sum_num(hand)==5 and is_sdb(hand) else False

#是否为人五小
def is_rwx(hand):
    return True if sum_num(hand)==5 and sum_p_num(hand)==5 else False

#判断当前手牌牌型
def hand_type(hand):
    card_type=1
    reward=1
    done=False
    
    #如果爆牌了
    if is_bust(hand):
        card_type=0
        reward=-1
        done=True
        
    elif is_sdb(hand):
        card_type=2
        reward=2
        done=True
        
    elif is_wx(hand):
        card_type=3
        reward=3
        done=True
        
    elif is_tw(hand):
        card_type=4
        reward=4
        done=True
        
    elif is_rwx(hand):
        card_type=5
        reward=5
        done=True
        
    return card_type,reward,done

def cmp(dealer,player):
    score_dealer=sum_score(dealer)
    score_player=sum_score(player)
    
    if score_dealer<score_player:
        return False
    elif score_dealer>score_player:
        return True
    else:
        num_dealer=sum_num(dealer)
        num_player=sum_num(player)
        return True if num_dealer>=num_player else False
    
class halftenenv(gym.Env):
    def __init__(self):
        self.action_space=spaces.Discrete(2)
        self.observation_space=spaces.Tuple((spaces.Discrete(21),spaces.Discrete(5),spaces.Discrete(6)))
        self._seed()
        self._reset()
        self.nA=2
        
        
    def _seed(self,seed=None):
        self.np_random,seed=seeding.np_random(seed)
        return [seed]
        
    def _reset(self):
        self.player=draw_hand(self.np_random)
        return self._get_obs()
        
    def _get_obs(self):
        return (sum_score(self.player),sum_num(self.player),sum_p_num(self.player))
    
    def _step(self,action):
        reward=0
        if action :
            self.player.append(draw_card(self.np_random))
            card_type,reward,done=hand_type(self.player)
        else:
            done=True
            self.dealer=draw_hand(self.np_random)
            result=cmp(self.dealer,self.player)
            if result:
                reward=-1
            else:
                
                while not result:
                    self.dealer.append(draw_hand(self.np_random))
                    card_type,dealer_reward,dealer_done=hand_type(self.dealer)
                    if dealer_done:
                        reward=-dealer_reward
                        break
                    else:
                        result=cmp(self.dealer,self.player)
                        if result:
                            reward=-1
        return self._get_obs(),reward,done


