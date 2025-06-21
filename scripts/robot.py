"""
Implementação de classe para controle do robô cilíndrico. 

Foram considerados no modelo os seguintes limites para as juntas:
Eixo 0 (Rotação): -180° <-> 180°
Eixo 1 (Translação em Z): 0 <-> 2.0 m 
Eixo 2 (Translação radial): 0 <-> 1.2 m
 Embedded Financial Solutions

Matriz de DH do manipulador:
Link θi     di     ai    alpha i
1    θ*     d1      0    0
2    0      d2*    a2   -90°
3   90°  df + d3*  a3    0

Sendo d1 = 0.15 m e a2 = 0.15 m a3 = 0.075 df = 0.25
df corresponde a distância do 0 do eixo 3 até o ponto de fixação
de modo que quando d3 está em 0 a ferramenta está na posição df. 
Transformação de 3 -> 0 (Cinemática direta)
|0  -c1  -s1  -s1 (d3 + df) + c1 a2 |
|0  -s1   c1   c1 (d3 + df) + s1 a2 |
|1   0    0        d1 + d2 - a3     |
|0   0    0               1         |

"""
import numpy as np
import math
from time import perf_counter

class CylindricRobot(object):
    def __init__(self, name, sim, debug = False):
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
        self.limits = [{'min': -math.pi, 'max': math.pi}, # rad
                        {'min': 0., 'max': 2.0}, # m
                        {'min': 0., 'max': 1.2}] # m

        self.jointJerk = 1000
        self.debug = debug
        self.teleport = False
    
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
    
    def getCurrentVelocity(self):
        linVel, __ = self.sim.getObjectVelocity(self.tip, self.sim.handle_world)
        return linVel
    
    def getCurrentJointPostions(self):
        jointPos = []
        for i in range(0, self.jointNumber):
            jointPos.append(self.sim.getJointPosition(self.motors[i]))
        return jointPos
    
    def jointMove(self, theta, d2, d3):
        if self.debug:
            print("Joint move to (", round(theta,3), " °,", round(d2,3), " m,", round(d3,3), " m)")
        self.sim.setJointTargetPosition(self.motors[0], theta)
        self.sim.setJointTargetPosition(self.motors[1], d2)
        self.sim.setJointTargetPosition(self.motors[2], d3)
    
    def cartesianMove(self, x, y, z):
        if self.debug:
            print("Cartesian move to (", round(x,3), " ,", round(y,3), " ,", round(z,3), " ) m")
        [theta, d2, d3] = self.ik(x, y, z)
        if not self.teleport:
            self.sim.setJointTargetPosition(self.motors[0], theta)
            self.sim.setJointTargetPosition(self.motors[1], d2)
            self.sim.setJointTargetPosition(self.motors[2], d3)
        else:
            self.sim.setJointPosition(self.motors[0], theta)
            self.sim.setJointPosition(self.motors[1], d2)
            self.sim.setJointPosition(self.motors[2], d3)

    def cartesianTrajectoryMove(self, x, y, z, duration):
        print("Cartesian Trajectory move to (", x, " ,", y, " ,", z, " ) m")
        [theta, d2, d3] = self.ik(x, y, z)
        print("Joint target is (", round(theta,3), " °,", round(d2,3), " m,", round(d3,3), " m)")
        jointPos = self.getCurrentJointPostions()
        vel, acc = self.calculateExecutionParams([theta, d2, d3], jointPos, duration)
        print("Current joint position is: ", [round(elem, 3) for elem in jointPos])
        print("Execution velocity: ", [round(elem, 3) for elem in vel])
        print("Execution acceleration: ", [round(elem, 3) for elem in acc])
        self.sim.setJointTargetPosition(self.motors[0], theta, [vel[0], acc[0], self.jointJerk])
        self.sim.setJointTargetPosition(self.motors[1], d2, [vel[1], acc[1], self.jointJerk])
        self.sim.setJointTargetPosition(self.motors[2], d3, [vel[2], acc[2], self.jointJerk])

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
        print("Executing linear Bang Bang trajectory to (",  
              [round(elem, 3) for elem in target], " in " , duration, "s")
        COORDINATES = 3
        # Função lambda que calcula o valor de alfa na etapa de aceleração
        accAlpha = lambda time : 2 * (time**2) / (duration**2) 
        # Função lambda que calcula o valor de alfa na etapa de frenagem
        brakeAlpha = lambda time : -1 + (4 * time / duration) - (2 * (time**2) / (duration**2))
        
        # Dados de execução da trajetória em coordenada cartesianas
        initialPos = self.getCurrentPosition()
        lastPos = initialPos
        lastDPos = initialPos

        # Listas para armazenar dados
        jointsPosition = []
        endEffectorPos = []
        endEffectorVel = []
        desiredVel = []
        trajectoryTime = []
        velocityTime = []

        # Variáveis de temporização
        switchTime = duration / 2.0
        startTime = perf_counter() # Mais preciso que time.time()
        lastTime = 0.0
        now = 0.0
        desiredVel.append([0,0,0])
        endEffectorVel.append([0,0,0])
        velocityTime.append(0)
        while perf_counter() - startTime <= duration:
            
            now = (perf_counter() - startTime) 
            # Fixa o tempo de envio para 0.2 s e envia o ponto de inflexão da velocidade
            if now - lastTime < 0.2 and abs(now - switchTime) > 0.001:
                continue

            # Define a função alpha utilizada
            if now < switchTime:
                alpha = accAlpha(now)
            else:
                alpha = brakeAlpha(now)

            # Calcula a posição alvo nesse instante
            pos = []
            for i in range(0, COORDINATES):
                # Lista com as posições x, y, z nessa ordem
                pos.append(initialPos[i] + alpha * (target[i] - initialPos[i]))

            # Realiza a movimentação do robô
            self.cartesianMove(*pos)

            # Mostra o progresso da trajetória
            curPos = self.getCurrentPosition()
            print("Time:", round(now, 4), "    Position: ", [round(elem, 3) for elem in curPos])
            print("")

            # Mede a velocidade executada e a velocidade final
            dVel = [(cur - last) / (now - lastTime) for cur, last in zip(pos, lastDPos)]
            lastDPos = pos
            vel = [(cur - last) / (now - lastTime) for cur, last in zip(curPos, lastPos)]
            lastPos = curPos
            lastTime = now
            desiredVel.append(dVel)
            endEffectorVel.append(vel)
            velocityTime.append(now)

            # Salva os dados para plot dos gráficos
            trajectoryTime.append(now) 
            endEffectorPos.append(curPos)
            jointsPosition.append(self.getCurrentJointPostions())

        print("Time:", round(duration,2), "    Position: ", 
              [round(elem, 3) for elem in self.getCurrentPosition()])

        # Salva os valores finais de velocidade 
        endEffectorVel.append([0,0,0])
        desiredVel.append([0,0,0])
        velocityTime.append(duration)
        
        return trajectoryTime, endEffectorPos, endEffectorVel, desiredVel, velocityTime, jointsPosition

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
        
        if self.debug:
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
        if self.debug:
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