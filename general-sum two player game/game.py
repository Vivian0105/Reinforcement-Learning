import numpy as np
import random

class grid_world:
    def __init__(self,A_location=6,B_location=8):
        self.A_location=A_location
        self.B_location=B_location
        self.goal=1
        self.done=False
    def reset(self):
        self.A_location=6
        self.B_location=8
        self.done=False
    def step(self,location,direction):
        grid_range=list(range(9))
        if direction=='N':
            destination=location-3
            if destination in grid_range:
                if location==6 or location==8:
                    p=random.random()
                    if p>0.5:
                        return destination
                    else:
                         return location
                else:
                    return destination
            else:
                return location
        elif direction=="S":
            destination=location+3
            if destination in grid_range:
                return destination
            else:
                return location
        elif direction=='E':
            destination=location+1
            if destination in [3,6,9]:
                return location
            else:
                return destination
        elif direction=='W':
            destination=location-1
            if destination in [-1,2,5]:
                return location
            else:
                return destination
    def move(self,actionA,actionB):
        destinationA=self.step(self.A_location,actionA)
        destinationB=self.step(self.B_location,actionB)
        #print("destinationA, destinationB: ", destinationA, " ", destinationB)
        if destinationA==destinationB:
            if destinationA==1:
                self.A_location=1
                self.B_location=1
                rewardA=50
                rewardB=50
                self.done=True
                return(rewardA,rewardB,self.done)
            else:
                if destinationA==self.A_location:
                    first='A'
                elif destinationB==self.B_location:
                    first='B'
                else:
                    p=random.random()
                    if p>0.5:
                        first='A'
                    else:
                        first='B'
                if first=='A':
                   self.A_location=destinationA
                   return(0,0,self.done)
                elif first=='B':
                   self.B_location=destinationB
                   return(0,0,self.done)
        elif destinationA!=destinationB:
            self.A_location=destinationA
            self.B_location=destinationB
            if destinationA==1:
                self.done=True
                return (100,0,self.done)
            elif destinationB==1:
                self.done=True
                return (0,100,self.done)
            else:
                return (0,0,self.done)


