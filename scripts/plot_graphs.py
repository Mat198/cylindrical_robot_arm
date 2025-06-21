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
    ax.set_xlim3d(-2, 2)
    ax.set_ylim3d(-2, 2)
    ax.set_zlim3d(0, 2)
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

def plotEefTrajectory(time, toolPosition):
    fig, ax = setupPlot()
    trajectory_line, = ax.plot([], [], [], 'k-', linewidth=2)
    current_pos_marker = ax.scatter([], [], [], c='r', s=50)
    initialPos = toolPosition[0]

    def update(frame):
        x = toolPosition[frame][0]
        y = toolPosition[frame][1]
        z = toolPosition[frame][2]
        trajectory_line.set_data([initialPos[0], x], [initialPos[1], y])
        trajectory_line.set_3d_properties([initialPos[2], z])
        current_pos_marker._offsets3d = ([x], [y], [z])
        return trajectory_line, current_pos_marker

    ani = FuncAnimation(fig, update, frames=len(time),
                        interval=10, blit=False, repeat=True)

    plt.tight_layout()
    plt.show()
    
def plotEefVelocity(trajTime, toolVelocity, desiredVel):
    __, axis = plt.subplots(3, 1)
    vel = np.array(toolVelocity)
    dVel = np.array(desiredVel)

    axis[0].plot(trajTime, vel[:, 0], label='Medida')
    axis[0].plot(trajTime, dVel[:, 0], label='Enviada')
    axis[0].set_ylabel('Velocidade [m/s]', fontsize=12)
    axis[0].legend()
    axis[0].set_title("vel no eixo X")

    axis[1].plot(trajTime, vel[:, 1], label='Medida')
    axis[1].plot(trajTime, dVel[:, 1], label='Enviada')
    axis[1].set_ylabel('Velocidade [m/s]', fontsize=12)
    axis[1].set_title("Velocidade no eixo Y")
    axis[1].legend()

    axis[2].plot(trajTime, vel[:, 2], label='Medida')
    axis[2].plot(trajTime, dVel[:, 2], label='Enviada')
    axis[2].set_ylabel('Velocidade [m/s]', fontsize=12)
    axis[2].set_xlabel('Tempo [s]', fontsize=12)
    axis[2].set_title("Velocidade no eixo Z")
    axis[2].legend()

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
    axis[2].set_xlabel('Tempo [s]', fontsize=12)

    # Combine all the operations and display
    plt.tight_layout()
    plt.show()

def plotJointsTrajectory(trajTime, jointsPos):

    __, axis = plt.subplots(3, 1)
    jointArray = np.array(jointsPos)

    # For Sine Function
    axis[0].plot(trajTime, jointArray[:, 0])
    axis[0].set_ylabel('Posição [rad]', fontsize=12)
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
    axis[2].set_xlabel('Tempo [s]', fontsize=12)

    # Combine all the operations and display
    plt.tight_layout()
    plt.show()