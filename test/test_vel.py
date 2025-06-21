import pickle

f = open('data.pkl', 'rb')
trajTime, eefPos, eefVel, desiredVel, velTime, jointsPos = pickle.load(f)
f.close()

import plot_graphs
plot_graphs.plotEefTrajectory(trajTime, eefPos)

import plot_graphs
import matplotlib.pyplot as plt
import numpy as np

toolVelocity = [[0,0,0]]

start = 1

for i in range(start, len(eefPos)):
    vel = [( cur - last) / (trajTime[i] - trajTime[i - start]) for cur, last in zip(eefPos[i], eefPos[i-start])]
    toolVelocity.append(vel)
toolVelocity.append([0,0,0])

# int(start/2):len(trajTime) - int(start/2)
timeList = trajTime[:len(trajTime) -1]
timeList.insert(0, 0)
timeList.append(13)

__, axis = plt.subplots(3, 1)
vel = np.array(toolVelocity)
dVel = np.array(desiredVel)

axis[0].plot(timeList, vel[:, 0])
axis[0].plot(velTime, dVel[:, 0])
axis[0].set_ylabel('vel [m]', fontsize=12)
axis[0].set_title("vel no eixo X")

# axis[1].plot(trajTime[start:], vel[:, 1])
# axis[1].plot(velTime, dVel[:, 1])
# axis[1].set_ylabel('vel [m]', fontsize=12)
# axis[1].set_title("vel no eixo Y")

# axis[2].plot(trajTime[start:], vel[:, 2])
# axis[2].plot(velTime, dVel[:, 2])
# axis[2].set_ylabel('vel [m]', fontsize=12)
# axis[2].set_title("vel no eixo Z")

plt.tight_layout()
plt.show()