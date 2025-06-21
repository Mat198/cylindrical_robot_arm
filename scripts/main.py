import math
# Conexão com o Coppelia Sim
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from connect import connect

# Classe para interface com o robô
from robot import CylindricRobot

# Funções para gerar resultados
from generate_workspace import generateWorkspace
from plot_graphs import * 

client = RemoteAPIClient()
sim = connect()

print("Simulação iniciada")
sim.startSimulation()

# Cria objeto para interface com o robô
robot = CylindricRobot("/P0_ST", sim)

# A matrícula é: 122800
duration = 13.0 # s
startPosition = [-0.75, -0.25, 0.75]
targetPosition = [0.75, 0.75, 1.75] 

# Executa a varedura no espaço de trabalho do robô
wsPoints = generateWorkspace(robot)
plotRobotWorkspace(wsPoints)

# Mostra porque não é possível executar os pontos propostos pelo exercício
# A linha entre os pontos final e inical cruza a região central que o robô não alcança
plotRouteInWorkspace(startPosition, targetPosition, wsPoints)

# Vamos então empurrar os pontos um pouco para fora dessa região central
startPosition = [-0.75, -0.25, 0.75]
targetPosition = [-0.25, 0.75, 1.75] 
plotRouteInWorkspace(startPosition, targetPosition, wsPoints)

# Executa trajetória
# Move o robô para a posição inicial da simulação (teletransporta para facilitar)
robot.setJointPosition(startPosition)
trajTime, eefPos, eefVel, desiredVel, velTime, jointsPos = robot.executeBangBangTrajectory(targetPosition, duration)

# Salva os dados num arquivo para testes
import pickle
filePath = "data.pkl"
with open(filePath, 'wb') as file:
    pickle.dump([trajTime, eefPos, eefVel, desiredVel, velTime, jointsPos], file)
    print(f"Variable saved to {filePath}")

plotEefTrajectory(trajTime, eefPos)
plotTrajectory(trajTime, eefPos)
plotEefVelocity(velTime, eefVel, desiredVel)
plotJointsTrajectory(trajTime, jointsPos)

sim.stopSimulation()
print("Simulação encerrada")