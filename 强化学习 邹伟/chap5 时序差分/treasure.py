# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 10:45:38 2021

@author: Lenovo
"""

import tkinter as tk
import numpy as np
import time

h=5
w=5
unit=40

class treasure(tk.Tk,object):
    def __init__(self):
        super(treasure,self).__init__()
        self.action_space=[0,1,2,3]
        self.n_action=len(self.action_space)
        self.title('寻宝')
        self.geometry('{0}x{1}'.format(h*unit,h*unit))
        self._build()
        
        
    def _build(self):
        self.canvas=tk.Canvas(self,height=h*unit,width=w*unit)
        for c in range(0,w*unit,unit):
            self.canvas.create_line(c,0,c,h*unit)
        
        for r in range(0,h*unit,unit):
            self.canvas.create_line(0,r,w*unit,r)
            
        self.hell1=self.canvas.create_rectangle(45,45,75,75,fill='black')
        self.hell2=self.canvas.create_rectangle(85,45,115,75,fill='black')
        self.hell3=self.canvas.create_rectangle(125,45,155,75,fill='black')
        self.hell4=self.canvas.create_rectangle(45,125,75,155,fill='black')
        self.hell5=self.canvas.create_rectangle(125,125,155,155,fill='black')
        self.hell6=self.canvas.create_rectangle(5,165,35,195,fill='black')
        self.hell7=self.canvas.create_rectangle(165,165,195,195,fill='black')
        
        self.oval=self.canvas.create_oval(85,165,115,195,fill='yellow')
        self.rect=self.canvas.create_rectangle(5,5,35,35,fill='red')
        
        self.canvas.pack()
        
    def reset(self):
        self.update()
        time.sleep(0.5)
        
        self.canvas.delete(self.rect)
        self.rect=self.canvas.create_rectangle(5,5,35,35,fill='red')
        return self.canvas.coords(self.rect)
    
    def step(self,action):
        s=self.canvas.coords(self.rect)
        base_step=np.zeros(2)
        if action==0:
            if s[1]>unit:
                base_step[1]=base_step[1]-unit
        elif action==1:
            if s[1]<h*unit-unit:
                base_step[1]+=unit
        elif action==2:
            if s[0]>unit:
                base_step[0]=base_step[0]-unit
        elif action==3:
            if s[0]<w*unit-unit:
                base_step[0]+=unit
                    
        self.canvas.move(self.rect,base_step[0],base_step[1])
        s_=self.canvas.coords(self.rect)
        reward=0
        done=False
        if s_==self.canvas.coords(self.oval):
            s_='terminal'
            reward=1
            done=True
        elif s_ in [self.canvas.coords(self.hell1),self.canvas.coords(self.hell2),self.canvas.coords(self.hell3),self.canvas.coords(self.hell4),self.canvas.coords(self.hell5),self.canvas.coords(self.hell6),self.canvas.coords(self.hell7)]:
            s_='terminal'
            reward=-1
            done=True
            
        return s_,reward,done
    
    def render(self):
        time.sleep(0.1)
        self.update()
    

