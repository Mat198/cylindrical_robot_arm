"""
Implementação de classe para controle do robô cilíndrico. 

Foi utilizado considerado no modelo os seguintes limites para as juntas:
Eixo 0 (Rotação): -180° <-> 180°
Eixo 1 (Translação em Z): 0 <-> 2.0 m 
Eixo 2 (Translação radial): 0 <-> 1.2 m
 Embedded Financial Solutions

Matriz de DH do manipulador:
Link θi     di     ai    αi
1    θ*     d1      0    0
2    0      d2*    a2   -90°
3   90°  df + d3*  a3    0

Sendo d1 = 0.15 m e a2 = 0.15 m a3 = 0.075 df = 0.25
Transformação de 3 -> 0 (Cinemática direta)
|0  -c1  -s1  -s1 (d3 + df) + c1 a2 |
|0  -s1   c1   c1 (d3 + df) + s1 a2 |
|1   0    0        d1 + d2 - a3     |
|0   0    0               1         |

Transformação de 0 -> 3 (Cinemática inversa)
| 0    0    1     a3 - d1 - d2 |
|-c1  -s1   0          a2      |
|-s1   c1   0      -(d3 + df)  |
| 0    0    0           1      |
"""
import numpy as np
import math

class CylindricRobot(object):
    def __init__(self, name, sim):
        self.name = name
        self.sim = sim
        self.d1 = 0.15 # m
        self.a2 = 0.15 # m
        self.a3 = 0.075 # m
        self.df = 0.25 # m
        self.motorBaseName = "/motor"
        self.jointNumber = 3
        self.motors = self.getMotors(self.sim)
        self.tipName = "/tip"
        self.tip = self.getTipObject(self.sim)
        # Limite de movimentação das juntas
        self.limits = {'motor0': {'min': -math.pi, 'max': math.pi}, # rad
                       'motor1': {'min': 0, 'max': 2.0}, # m
                       'motor2': {'min': 0, 'max': 1.2}} # m
    
    def setJointPosition(self, positon):
        jointPos = self.ik(positon[0], positon[1], positon[2])
        self.sim.setJointPosition(self.motors[0], jointPos[0])
        self.sim.setJointPosition(self.motors[1], jointPos[1])
        self.sim.setJointPosition(self.motors[2], jointPos[2])
    
    def getTipObject(self, sim):
        return sim.getObject(self.name + self.tipName)
    

    def getMotors(self, sim):
        motors = []
        for i in range(0, self.jointNumber):
            print("Getting motor ", self.name + self.motorBaseName + str(i))
            result = sim.getObject(self.name + self.motorBaseName + str(i))
            if not result:
                raise KeyError("Unknow motor")
            motors.append(result)
        return motors

    def getCurrentPosition(self):
        pos = self.sim.getObjectPosition(self.tip, self.sim.handle_world)
        return pos
    
    def getCurrentJointPostions(self):
        jointPos = []
        for i in range(0, self.jointNumber):
            jointPos.append(self.sim.getJointPosition(self.motors[i]))
        return jointPos
    
    def jointMove(self, theta, d2, d3):
        print("Joint move to (", theta, " °,", d2, " m,", d3, " m)")
        self.sim.setJointTargetPosition(self.motors[0], theta)
        self.sim.setJointTargetPosition(self.motors[1], d2)
        self.sim.setJointTargetPosition(self.motors[2], d3)
    
    def cartesianMove(self, x, y, z, duration):
        print("Cartesian move to (", x, " ,", y, " ,", z, " ) m")
        [theta, d2, d3] = self.ik(x, y, z)
        print("IK solution is (", theta, " °,", d2, " m,", d3, " m)")
        jointPos = self.getCurrentJointPostions()
        vel, acc = self.calculateExecutionParams([theta, d2, d3], jointPos, duration)
        print("Current joint position is: ", jointPos)
        print("Execution velocity: ", vel)
        print("Execution acceleration: ", acc)
        self.sim.setJointTargetPosition(self.motors[0], theta, [vel[0], acc[0], 1000])
        self.sim.setJointTargetPosition(self.motors[1], d2, [vel[1], acc[1], 1000])
        self.sim.setJointTargetPosition(self.motors[2], d3, [vel[2], acc[2], 1000])

    def calculateExecutionParams(self, target, currentPosition, duration):
        vel = []
        acc = []
        for i in range(0, self.jointNumber):
            jointVel = 2 * (target[i] - currentPosition[i]) / duration
            jointAcc = 4 * (target[i] - currentPosition[i]) / duration**2
            vel.append(abs(jointVel))
            acc.append(abs(jointAcc))
        return vel, acc

    def executeBangBangTrajectory(self, target, duration):
        # Função lambda que calcula o valor de alfa na etapa de aceleração
        accAlfa = lambda time : time**2 / duration 
        # Função lambda que calcula o valor de alfa na etapa de frenagem
        brakeAlfa = lambda time : 2 * time / duration - time**2 / duration

        # while time < duration:

    # Retorna a matriz de rotação para transformação direta
    def genDirRotMatrix (self, theta):
        c1 = math.cos(theta)
        s1 = math.sin(theta)
        return np.array(
            [[0, -c1, -s1],
             [0, -s1,  c1],
             [1,   0,   0]])
    
    def genDirTransVector(self, theta, d2, d3):
        c1 = math.cos(theta)
        s1 = math.sin(theta)
        return [-s1*(d3 + self.df) + c1 * self.a2, 
                c1*(d3 + self.df) + s1 * self.a2, 
                self.d1 + d2 - self.a3]

    def fk(self, theta, d2, d3):
        return self.genDirTransVector(theta, d2, d3)

    def ik(self, x, y, z):
        d2 = z - self.d1 + self.a3
        thetaList = self.calculateIkTheta(x, y)
        theta = None
        d3 = None
        d3List = []
        for angle in thetaList:
            c1 = math.cos(angle)
            s1 = math.sin(angle)
            d3 = y * c1 - x * s1 - self.df
            d3List.append(d3)
        print("Soluções para theta: ", thetaList)
        print("Soluções para d3: ", d3List)
    
        if d3List[0] >= 0:
            d3 = d3List[0]
            theta = thetaList[0]
        elif d3List[1] >= 0:
            d3 = d3List[1]
            theta = thetaList[1]
        else:
            raise ValueError("Falhou em calcular ik")
        print("Solução da cinemática inversa: ", 
            [round(math.degrees(theta), 3), round(d2, 3), round(d3, 3)])
        
        return [theta, d2, d3]

    def calculateIkTheta(self, x, y):
        x2 = x**2
        y2 = y**2
        y4 = y**4
        a2 = self.a2
        a2_2 =self.a2**2
        d = x**2 + y**2
        denSqrtTerm = math.sqrt(x2*y2 + y4 - y2*a2_2)
        numSqrtTerm = math.sqrt(-y2 * (-x2 - y2 + a2_2))
        root1DenTerm = (x * a2 - denSqrtTerm) / d
        root1NumTerm = ((x * numSqrtTerm / d) - (x2 * a2 / d) + a2) / y
        root1 = math.atan2(root1NumTerm, root1DenTerm)
        root2DenTerm = (x * a2 + denSqrtTerm) / d
        root2NumTerm = (-(x * numSqrtTerm / d) - (x2 * a2 / d) + a2) / y
        root2 = math.atan2(root2NumTerm, root2DenTerm)
        return [root1, root2]