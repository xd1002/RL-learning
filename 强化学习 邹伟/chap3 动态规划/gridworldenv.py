# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 09:55:00 2021

@author: Lenovo
"""

import numpy as np
from gym.envs.toy_text import discrete
#找宝藏环境搭建
#为看起来方便，定义一些全局变量
up=0
right=1
down=2
left=3
done_location=8

class gridworldenv(discrete.DiscreteEnv):
    
    def __init__(self,shape=[5,5]):
        
        #shape：grid的行数和列数
        #p：一个dict，用于存储dict，外层每个key对应grid中的一个位置，key的内容还是一个dict，他的key是上下左右四种操作方式，每个key的内容是一个list包含了一个tuple，记录了在grid的这一位置下执行相应操作的概率、下一个位置、奖励和下次是否到达指定位置
        #it：产生一个可迭代的对象（方便执行，其实也可以直接遍历grid）
        self.shape=shape
        p={}
        nS=np.prod(shape)
        na=4
        max_x=shape[0]
        max_y=shape[1]
        grid=np.arange(nS).reshape(shape)
        it=np.nditer(grid,flags=['multi_index'])
        
        while not it.finished:
            s=it.iterindex
            x,y=it.multi_index
            p[s]={a:[] for a in range(na)}
            is_done= lambda s:s==done_location
            reward=0 if is_done(s) else -1
            
            #如果当前位置是指定位置done_location
            if is_done(s):
                p[s][up].append((1,s,reward,True))
                p[s][right].append((1,s,reward,True))
                p[s][down].append((1,s,reward,True))
                p[s][left].append((1,s,reward,True))
            else:
                s_up=s if x==0 else s-max_x
                s_right=s if y==max_y-1 else s+1
                s_down=s if x==max_x-1 else s+max_x
                s_left=s if y==0 else s-1
                p[s][up].append((1,s_up,reward,is_done(s_up)))
                p[s][right].append((1,s_right,reward,is_done(s_right)))
                p[s][down].append((1,s_down,reward,is_done(s_down)))
                p[s][left].append((1,s_left,reward,is_done(s_left)))
            it.iternext()
        self.p=p
        isd=np.ones(nS)/nS
        
        #这句非常必要，虽然我不太清楚为什么要有这句
        super(gridworldenv,self).__init__(nS,na,p,isd)
#question：离散的问题能一个个列出来，连续的问题怎么办？，还有这里每个行为(上右下左对应了0123)进行的概率都是1？
#另外，如果在别的程序中引用这个class？
