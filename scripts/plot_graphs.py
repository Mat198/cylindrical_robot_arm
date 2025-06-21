import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def setupPlot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X [m]', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y [m]', fontsize=12, fontweight='bold')
    ax.set_zlabel('Z [m]', fontsize=12, fontweight='bold')
    ax.grid(True)
    return fig, ax


def plotRobotWorkspace(points):
    __, ax = setupPlot()
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, alpha=0.5, c='blue')
    ax.set_title('Área de Trabalho - Gerada pela cinemática direta')
    plt.tight_layout()
    plt.show()

def plotRouteInWorkspace(origin, target, workspace):
    __, ax = setupPlot()
    ax.scatter(workspace[:, 0], workspace[:, 1], workspace[:, 2], s=1, alpha=0.5, c='blue')
    ax.plot([origin[0], target[0]], [origin[1], target[1]], [origin[2], target[2]], c='red')
    ax.set_title('Área de Trabalho com rota proposta')
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt

def plotRobotWorkspace(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, alpha=0.5, c='blue')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Área de Trabalho - Gerada pela cinemática direta')
    plt.tight_layout()
    plt.show()

def plotRouteInWorkspace(origin, target, workspace):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(workspace[:, 0], workspace[:, 1], workspace[:, 2], s=1, alpha=0.5, c='blue')
    ax.plot([origin[0], target[0]], [origin[1], target[1]], [origin[2], target[2]], c='red')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Área de Trabalho com rota proposta')
    plt.tight_layout()
    plt.show()
def plotTrajectory(trajTime, eefPositions):

    __, axis = plt.subplots(3, 1)
    eefArray = np.array(eefPositions)

    # For Sine Function
    axis[0].plot(trajTime, eefArray[:, 0])
    axis[0].set_ylabel('Posição [m]', fontsize=12)
    axis[0].set_title("Posição no eixo X")

    axis[1].plot(trajTime, eefArray[:, 1])
    axis[1].set_ylabel('Posição [m]', fontsize=12)
    axis[1].set_title("Posição no eixo Y")

    axis[2].plot(trajTime, eefArray[:, 2])
    axis[2].set_ylabel('Posição [m]', fontsize=12)
    axis[2].set_title("Posição no eixo Z")

    # Combine all the operations and display
    plt.tight_layout()
    plt.show()

def plotJointsTrajectory(trajTime, jointsPos):

    __, axis = plt.subplots(3, 1)
    jointArray = np.array(jointsPos)

    # For Sine Function
    axis[0].plot(trajTime, math.degrees(jointArray[:, 0]))
    axis[0].set_ylabel('Posição [°]', fontsize=12)
    axis[0].set_title("Posição da junta 0 (Rotação da base)")

    # For Cosine Function
    axis[1].plot(trajTime, jointArray[:, 1])
    axis[1].set_ylabel('Posição [m]', fontsize=12)
    axis[1].set_title("Posição da junta 1 (Translação em Z)")

    # For Tangent Function
    axis[2].plot(trajTime, jointArray[:, 2])
    axis[2].set_xlabel('Tempo [s]', fontsize=12)
    axis[2].set_ylabel('Posição [m]', fontsize=12)
    axis[2].set_title("Posição da junta 2 (Translação radial)")

    # Combine all the operations and display
    plt.tight_layout()
    plt.show()