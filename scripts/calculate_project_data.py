# Código para extrair informações do exercício
# Matheus Sousa Soares - 122800 
matricula = 122800
digR = matricula // 1e5 % 10
digS = matricula // 1e4 % 10
digT = matricula // 1e3 % 10
digX = matricula // 1e2 % 10
digY = matricula // 1e1 % 10
digZ = matricula // 1e0 % 10

print("A matrícula é:", matricula)
print("R:",digR,"S:",digS,"T:",digT,"X:",digX,"Y:",digY,"Z:",digZ)
# Tipo de robô que deve ser utilizado
robotTypeNumber = matricula % 3
if robotTypeNumber == 0:
    print("Robô SCARA deve ser utilizado!")
elif robotTypeNumber == 1:
    print("Robô cilíndico deve ser utilizado!")
elif robotTypeNumber == 2:
    print("Robô do tipo esférico deve ser utilizado!")
else:
    raise ValueError("Era esperado os valores 0, 1 ou 2 para o tipo do robô.")

# Tipo de estratégia de movimentação
if (digZ % 2): # Ímpar
    print("Deve ser utilizada a estratégia polinomial de 3ª ordem!")
else: # Par
    print("Deve ser utilizada a estratégia de tempo mínimo (bang-bang)!")

# Tempo total de execução:
tempoExecucao = digR + digS + digT + digX + digY + digZ
print("O tempo de execução deve ser de", tempoExecucao, "s!")

# Pontos de partida e de chegada
pontoPartida = [-0.5, -0.5, 0.5] # m
if (digR % 2): # Ímpar
    pontoPartida[0] += -0.25
else: # Par
    pontoPartida[0] += 0.25

if (digS % 2): # Ímpar
    pontoPartida[1] += -0.25
else: # Par
    pontoPartida[1] += 0.25

if (digT % 2): # Ímpar
    pontoPartida[2] += -0.25
else: # Par
    pontoPartida[2] += 0.25

print("O ponto de partida deve ser: ", pontoPartida, "!")

pontoChegada = [0.5, 0.5, 1.5] # m
if (digX % 2): # Ímpar
    pontoChegada[0] += -0.25
else: # Par
    pontoChegada[0] += 0.25

if (digY % 2): # Ímpar
    pontoChegada[1] += -0.25
else: # Par
    pontoChegada[1] += 0.25

if (digZ % 2): # Ímpar
    pontoChegada[2] += -0.25
else: # Par
    pontoChegada[2] += 0.25

print("O ponto de chegada deve ser: ", pontoChegada, "!")