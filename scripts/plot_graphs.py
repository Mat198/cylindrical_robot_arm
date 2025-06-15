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