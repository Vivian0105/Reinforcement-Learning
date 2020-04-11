import numpy as np
from game import grid_world
from cvxopt import matrix,solvers
from matplotlib import pyplot as plt
import random

solvers.options['show_progress'] = False
def foeQ(Q):
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
    return sol['x'][0]

QA=np.zeros((9,9,4,4))
QB=np.zeros((9,9,4,4))

episodes=10**5
alpha=0.1
alpha_decay=0.99995
alpha_min=0.001
gamma=0.9
error_list=[]
actiondict={0:'N',1:"S",2:'W',3:'E'}

game=grid_world()
for e in range(episodes):
    game.reset()
    QA_initial=QA[6][8][0][0]
    QB_initial=QB[6][8][0][0]
    while True:
        lA=game.A_location
        lB=game.B_location
        aA=random.randint(0,3)
        aB=random.randint(0,3)
        actionA=actiondict[aA]
        actionB=actiondict[aB]
        rewardA, rewardB, done=game.move(actionA,actionB)
        VA=foeQ(QA[game.A_location][game.B_location])
        VB=foeQ(QB[game.A_location][game.B_location])
        QA[lA][lB][aA][aB]=(1-alpha)*QA[lA][lB][aA][aB]+alpha*(rewardA+gamma*VA)
        QB[lA][lB][aB][aA]=(1-alpha)*QB[lA][lB][aB][aA]+alpha*(rewardB+gamma*VB)
        if done:
           QA_end=QA[6][8][0][0]
           QB_end=QB[6][8][0][0]
           error=abs(QA_initial-QA_end)+abs(QB_initial-QB_end)
           error_list.append(error)
           if error!=0:
               print("The error at episode %i is %f. Alpha is %f."%(e,error,alpha))
           else:
               if e%1000==0:
                   print("Episode %i ends."%(e))
           break
    new_alpha=alpha*alpha_decay
    if new_alpha>alpha_min:
        alpha=new_alpha
    else:
        alpha=alpha_min

np.save('QA_FOE.npy',QA)
np.save('QB_FOE.npy',QB)
error_list=np.array(error_list)
np.save("FOE_ERROR.npy",error_list)

plt.plot(list(range(10**5)),error_list)
plt.xlabel("Episodes")
plt.ylabel("Sum of absolute Q-value differences")
plt.title("Foe-Q")
plt.savefig("FoeQ"+".png")
plt.show()