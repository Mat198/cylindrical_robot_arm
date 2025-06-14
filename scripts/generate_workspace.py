import numpy as np
import math
from robot import CylindricRobot

# Intervalo definido para a varredura do espaço de trabalho
ANGLE_INTERVAL = math.radians(10) # rads
LINEAR_INTERVAL = 0.2 # m

# Realiza a varredura do espaço de trabalho usando a cinemática direta
def generateWorkspace(robot: CylindricRobot):
    print('Gerando varredura do espaço de trabalho')
    
    # Encontra o total de pontos avaliados para cada junta
    motor0Points = int((robot.limits[0]['max'] - robot.limits[0]['min']) / ANGLE_INTERVAL)
    motor1Points = int((robot.limits[1]['max'] - robot.limits[1]['min']) / LINEAR_INTERVAL)
    motor2Points = int((robot.limits[2]['max'] - robot.limits[2]['min']) / LINEAR_INTERVAL)

    # Junta rotacional
    motor0Range= np.linspace(robot.limits[0]['min'], robot.limits[0]['max'], motor0Points)
    # Juntas prismáticas
    motor1Range = np.linspace(robot.limits[1]['min'], robot.limits[1]['max'], motor1Points)
    motor2Range = np.linspace(robot.limits[2]['min'], robot.limits[2]['max'], motor2Points)

    points = []
    points.append(robot.fk(0, 0, 0))
    for angle in motor0Range:
        for pos1 in motor1Range:
            for pos2 in motor2Range:
                position = robot.fk(angle, pos1, pos2)
                points.append(position)

    return np.array(points)


