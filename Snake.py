# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 2019 in ShangHai

@author: HuQiTong, ShanDong University
"""
import os
from threading import Thread
import numpy as np
from time import sleep
from tkinter import Tk,Canvas,messagebox
from random import shuffle

class Snake():
    def __init__(self,width,height,length,scale):
        setattr(self,'width',width)
        setattr(self,'height',height)
        setattr(self,'length',length)
        setattr(self,'scale',scale)
        setattr(self,'snake',[])
        setattr(self,'food_map',[])
        setattr(self,'snake_map',[])
        self.snake_window()

    def snake_bound(self):
        snake=getattr(self,'snake')
        width=getattr(self,'width')
        height=getattr(self,'height')
        length=len(snake)-1
        if(snake[length][0]<0 or snake[length][0]>width-1):
            return True
        if(snake[length][1]<0 or snake[length][1]>height-1):
            return True
        if(snake[0][0]<0 or snake[0][0]>width-1):
            return True
        if(snake[0][1]<0 or snake[0][1]>height-1):
            return True
        return False
    
    def snake_self(self):
        snake=getattr(self,'snake')
        if(snake[0] in snake[1:len(snake)]):
            return True
        return False
    
    def snake_inital(self):
        width=getattr(self,'width')
        height=getattr(self,'height')
        length=getattr(self,'length')
        snake=getattr(self,'snake')
        snake_map=getattr(self,'snake_map')
        cen_width=np.random.randint(1,width-1,1)[0]
        cen_height=np.random.randint(1,height-1,1)[0]
        snake.append([cen_width,cen_height])
        setattr(self,'snake',snake)
        snake_map.create_rectangle(cen_width*10,cen_height*10,cen_width*10+10, \
                                   cen_height*10+10,fill='blue',width=0)
        for i in range(length-1):
            self.snake_lengthen()

    def snake_lengthen(self):
        snake=getattr(self,'snake')
        length=getattr(self,'length')
        scale=getattr(self,'scale')
        snake_map=getattr(self,'snake_map')
        old_snake=snake
        old_length=length
        dirction=[[-1,0],[1,0],[0,-1],[0,1]]
        shuffle(dirction)
        for i in range(len(dirction)):
            new_rect=list(np.array(snake[len(snake)-1])+np.array(dirction[i]))
            if(new_rect in snake):
                continue
            snake.append(new_rect)
            setattr(self,'snake',snake)
            if(self.snake_bound() or self.snake_self()):
                setattr(self,'snake',old_snake)
                continue
            else:
                snake_map.create_rectangle(new_rect[0]*scale,new_rect[1]*scale, \
                                           (new_rect[0]+1)*scale,(new_rect[1]+1)*scale,fill='blue',width=0)
                break
        if(old_length==length):
            return False
        return True
    
    def snake_forward(self):
        count=0
        while(True):
            sleep(0.5)
            count=count+1
            try:
                if(not count%10):
                    self.snake_food()
                self.snake_automove()
            except:
                os._exit(0)

    def snake_food(self):
        width=getattr(self,'width')
        height=getattr(self,'height')
        scale=getattr(self,'scale')
        snake=getattr(self,'snake')
        snake_map=getattr(self,'snake_map')
        food_map=getattr(self,'food_map')
        food_avil=[[i,j] for i in range(width) for j in range(height) \
                      if([i,j] not in snake)]
        index=np.random.randint(0,len(food_avil))
        food=food_avil[index]
        food_map.append(food)
        snake_map.create_rectangle(food[0]*scale,food[1]*scale, \
                                   (food[0]+1)*scale,(food[1]+1)*scale,fill='blue',width=0)
        snake_map.update()
    
    def snake_automove(self):
        snake=getattr(self,'snake')
        length=len(snake)-1
        dirction=(np.array(snake[length])-np.array(snake[length-1])).tolist()
        self.snake_move_(None,dirction)
        
    def snake_move_(self,event,dirction):
        scale=getattr(self,'scale')
        snake=getattr(self,'snake')
        snake_map=getattr(self,'snake_map')
        food_map=getattr(self,'food_map')
        new_rect=list(np.array(snake[len(snake)-1])+np.array(dirction))
        if(new_rect in snake):
            return False
        old_rect=snake[0]
        snake.append(new_rect)
        if(new_rect not in food_map):
            del snake[0]
            snake_map.create_rectangle(old_rect[0]*scale,old_rect[1]*scale, \
                                           (old_rect[0]+1)*scale,(old_rect[1]+1)*scale,fill='white',width=0)
        else:
            setattr(self,'length',getattr(self,'length')+1)
        snake_map.create_rectangle(new_rect[0]*scale,new_rect[1]*scale, \
                                           (new_rect[0]+1)*scale,(new_rect[1]+1)*scale,fill='blue',width=0)
        setattr(self,'snake',snake)
        if(self.snake_bound() or self.snake_self()):
            setattr(self,'snake',[])
            setattr(self,'food_map',[])
            result=messagebox.askyesno('提示','是否重新来过')
            if(result):
                snake_map=getattr(self,'snake_map')
                snake_map.destroy()
                self.snake_canvas()
            else:
                os._exit(0)

    def snake_move(self,fun,**kwds):
        return lambda event,fun=fun,kwds=kwds:fun(event,**kwds)

    def snake_window(self):
        def window_destroy():
            setattr(self,'snake',[])
            setattr(self,'food_map',[])
            snake_window.destroy()
            os._exit(0)

        snake_window=Tk()
        setattr(self,'snake_window',snake_window)
        self.snake_canvas()
        snake_window.bind(sequence='<Left>',func=self.snake_move(self.snake_move_,dirction=[-1,0]))
        snake_window.bind(sequence='<Right>',func=self.snake_move(self.snake_move_,dirction=[1,0]))
        snake_window.bind(sequence='<Up>',func=self.snake_move(self.snake_move_,dirction=[0,-1]))
        snake_window.bind(sequence='<Down>',func=self.snake_move(self.snake_move_,dirction=[0,1]))
        snake_window.protocol('WM_DELETE_WINDOW',window_destroy)
        snake_window.mainloop()

    def snake_canvas(self):
        width=getattr(self,'width')
        height=getattr(self,'height')
        scale=getattr(self,'scale')
        snake_window=getattr(self,'snake_window')
        snake_map=Canvas(snake_window,width=width*scale,height=height*scale,background="white")
        setattr(self,'snake_map',snake_map)
        self.snake_inital()
        snake_map.pack()
        make_food=Thread(target=self.snake_forward)
        make_food.setDaemon(False)
        make_food.start()

if __name__=='__main__':
    Snake(100,50,10,10)