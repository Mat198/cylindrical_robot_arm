import pickle
import matplotlib.pyplot as plt
import numpy as np

f = open('data.pkl', 'rb')
trajTime, eefPos, eefVel, desiredVel, velTime, jointsPos = pickle.load(f)
f.close()

toolVelocity = [[0,0,0]]
start = 10

for i in range(start, len(eefPos)):
    vel = [( cur - last) / (trajTime[i] - trajTime[i - start]) for cur, last in zip(eefPos[i], eefPos[i-start])]
    toolVelocity.append(vel)
toolVelocity.append([0,0,0])

timeList = trajTime[int(start/2):len(trajTime) - int(start/2)]
timeList.insert(0, 0)
timeList.append(13)

__, axis = plt.subplots(3, 1)
vel = np.array(toolVelocity)
dVel = np.array(desiredVel)

axis[0].plot(timeList, vel[:, 0], label='Medida')
axis[0].plot(velTime, dVel[:, 0], label='Enviada')
axis[0].set_ylabel('Velocidade [m/s]', fontsize=12)
axis[0].set_title("Velocidade no eixo X")

axis[1].plot(timeList, vel[:, 1], label='Medida')
axis[1].plot(velTime, dVel[:, 1], label='Enviada')
axis[1].set_ylabel('Velocidade [m/s]', fontsize=12)
axis[1].set_title("Velocidade no eixo Y")

axis[2].plot(timeList, vel[:, 2], label='Medida')
axis[2].plot(velTime, dVel[:, 2], label='Enviada')
axis[2].set_ylabel('Velocidade [m/s]', fontsize=12)
axis[2].set_xlabel('Tempo [s]', fontsize=12)
axis[2].set_title("Velocidade no eixo Z")

plt.tight_layout()
plt.show()