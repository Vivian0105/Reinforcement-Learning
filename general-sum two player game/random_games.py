import numpy as np
from game import grid_world
import random
from cvxopt import matrix,solvers
from matplotlib import pyplot as plt


solvers.options['show_progress'] = False

QA=np.load("QA_FOE.npy")
#print(QA[6][8])
QB=np.load("QB_FOE.npy")
#print(QB[6][8])

def foeQ_policy(Q):
    v=[1,1,1,1,0,0,0,0]
    x0=[-Q[0][0],-Q[0][1],-Q[0][2],-Q[0][3],-1.,0.,0.,0.]
    x1=[-Q[1][0],-Q[1][1],-Q[1][2],-Q[1][3],0.,-1.,0.,0.]
    x2=[-Q[2][0],-Q[2][1],-Q[2][2],-Q[2][3],0.,0.,-1.,0.]
    x3=[-Q[3][0],-Q[3][1],-Q[3][2],-Q[3][3],0.,0.,0.,-1.]
    G=matrix([v,x0,x1,x2,x3])
    h=matrix(np.zeros(8))
    c=matrix(np.array([-1.,0.,0.,0.,0.]))
    A = matrix([[0.],[1.],[1.],[1.],[1.]])
    b = matrix([1.])
    sol = solvers.lp(c, G, h, A, b)
    return [sol['x'][1],sol['x'][2],sol['x'][3],sol['x'][4]]

def get_action(prob):
    p=random.random()
    if p<prob[0]:
        return 'N'
    elif p<prob[0]+prob[1]:
        return 'S'
    elif p<prob[0]+prob[1]+prob[2]:
        return 'W'
    else:
        return 'E'

actiondict={0:'N',1:"S",2:'W',3:'E'}
game=grid_world()
episode=100
rewardA_list=[]
rewardB_list=[]
actionA_prob=[0,0,0,0]
actionB_prob=[0,0,0,0]
for e in range(episode):
    game.reset()
    #game=grid_world(3,5)
    while True:
        #print("Current state: ", game.A_location, game.B_location)
        actionA_prob=foeQ_policy(QA[game.A_location][game.B_location])
        actionB_prob=foeQ_policy(QB[game.A_location][game.B_location])
        actionA=get_action(actionA_prob)
        actionB=get_action(actionB_prob)
        #print("Action of A is %s, Action of B is %s."%(actionA,actionB))
        rewardA, rewardB, done=game.move(actionA,actionB)
        if done:
            #print("reward of A and B is %i, %i. "%(rewardA,rewardB))
            rewardA_list.append(rewardA)
            rewardB_list.append(rewardB)
            break

print("Reward of A: ", sum(rewardA_list)/len(rewardA_list))
print("Reward of B: ", sum(rewardB_list)/len(rewardA_list))



