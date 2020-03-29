import numpy as np
import math

from funcoesTermosol import importa
from funcoesTermosol import plota
[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xlsx')


#plota(N, Inc)
#numero de nos [nn]
#matriz dos nos [N]
#numero de membros [nm]
#matriz de incidencia [Inc]
#numero de cargas [nc]
#vetor carregamento [F]
#numero de restricoes [nr]
#vetor de restricoes [R]

def SenCos(x1,x2,y1,y2):
    L = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
    sen = (y2 - y1)/L
    cos = (x2 -x1)/L

    return L,sen,cos

def getCoorNos(N, n_no):
    nos = []
    for i in range(0,len(N[0])):
        nos.append([N[0][i], N[1][i]])
    n_no = int(n_no)
    return (nos[n_no-1])

def getNos(nm):
    nos = []
    for i in range(0, nm):
        nos.append([Inc[i][0], Inc[i][1]])
    return nos

def getCoorElemento(nm, N):
    elemento = []
    for i in range(nm):
        elemento.append([getCoorNos(N, Inc[i,0]), getCoorNos(N, Inc[i,1])]) 
    return elemento

def Ke(coor1_elemento,coor2_elemento,E,A):
    X1 = coor1_elemento[0]
    Y1 = coor1_elemento[1]
    X2 = coor2_elemento[0]
    Y2 = coor2_elemento[1]
    l, Sen, Cos = SenCos(X1,X2,Y1,Y2)
    k = (E * A)/ l 
    #forma matriz
    m =  np.array([-Cos, -Sen, Cos, Sen], float)
    ke = np.array([[Cos**2, Cos*Sen, -Cos**2, -Cos*Sen],[Cos*Sen, Sen*Sen, -Cos*Sen, -Sen*Sen], [-Cos**2, -Cos*Sen, Cos**2, Cos*Sen], [-Cos*Sen, -Sen*Sen, Cos*Sen, Sen*Sen]])

    return (np.multiply(ke,  k), l, m)
  
#Programa main
coor_elementos = getCoorElemento(nm, N)
nos = getNos(nm)

#ke para cada elemento
ke_g = []
E = []
A = []
L = []
m = []

for i in range(0,nm):
    E.append(Inc[i,2])
    A.append(Inc[i,3])

for i in range(0,nm):
    ke_g.append(Ke(coor_elementos[i][0], coor_elementos[i][1], E[i], A[i])[0])
    L.append(Ke(coor_elementos[i][0], coor_elementos[i][1], E[i], A[i])[1])
    m.append(Ke(coor_elementos[i][0], coor_elementos[i][1], E[i], A[i])[2])
    

g_liber = 2
Kg = np.zeros([nn*g_liber, nn*g_liber])
for i in range(0, nm):
    if (nos[i][0] == 1):
        g1 = 1
        g2 = 2
    else:
        g2 = int(nos[i][0] * 2)
        g1 = int(g2 - 1)
    if (nos[i][1] == 1):
        g3 = 1
        g4 = 2
    else:
        g4 = int(nos[i][1] * 2)
        g3 = int(g4 - 1)
    Kg[g1-1:g2, g1-1:g2] += ke_g[i][0:2,0:2]
    Kg[g1-1:g2, g3-1:g4] += ke_g[i][0:2,2:4]
    Kg[g3-1:g4, g1-1:g2] += ke_g[i][2:4,0:2]
    Kg[g3-1:g4, g3-1:g4] += ke_g[i][2:4,2:4]
    

#montagem de vetor de carga global

Pg = F

#aplicar condicoes de contorno

Kg2 = Kg

i = 0
for each in R:
    index = int(each[0])-i
    Kg = np.delete(Kg, index, 0) 
    Kg = np.delete(Kg, index, 1) 
    Pg = np.delete(Pg, index, 0)
    i+=1
#solucao de sistemas de equação (solucao.py)

condicao = True
results = [0] * len(Pg)

print(len(results))

while condicao:
    for i in range(0,len(Kg)):
        sub = 0
        for j in range(0, len(Kg)):
            if i != j:
                sub -= Kg[i][j] * results[j]

        new_u = (Pg[i] + sub)/Kg[i][i]

        if new_u != 0:

            erro = abs((new_u - results[i])/new_u)

            if erro < 1e-10:
                condicao = False
                break

            results[i] = new_u

#determinaçao das reacoes de apoio estrutural/ deformacao e tensao do elemento
    
#deslocamentos nodais a serem calculados são os não excluidos, os excluidos são zero
not_deleted = []
#matriz do deslocamento nodal (results)
for i in range(0, nn*2):
    if (i not in R):
        not_deleted.append(i)
        
U = np.zeros([nn*2])
i = 0
for each in not_deleted:
    U[each] = results[i]
    i += 1

#matriz completa dos deslocamentos nodais = U
#o calculo das forças de apoio (multiplicação de Kg por U) com os resultados aonde foram apagados
#Kg * U = Re

Re = Kg2.dot(U)


#reactions = []
#for each in R:
#    index = int(each[0])
#    reactions.append(Re[index])

#calcular deformação
#A deformação específica pode ser calculada a partir dos deslocamentos nodais do elemento de barra. 
#def = (1/L)[-1 1][desl_no1 desl_no2] = (1/L)(desl_no2 - desl_no1)

deformation = []
tensoes = []
forcas_int = []

for i in range(0, nm):
    no1 = int(nos[i][0])
    no2 = int(nos[i][1])
    if (no1 == 1):
        g1 = 1
        g2 = 2
    else:
        g2 = int(no1 * 2)
        g1 = int(g2 - 1)
    if (no2 == 1):
        g3 = 1
        g4 = 2
    else:
        g4 = int(no2 * 2)
        g3 = int(g4 - 1)
    graus = [g1-1, g2-1, g3-1, g4-1]
    desl_g = []
    for each in graus:
        desl_g.append(U[each])
    deformation.append(np.matmul(m[i], desl_g) / L[i]) 
    tensoes.append(deformation[i]*E[i])
    forcas_int.append(tensoes[i]*A[i])


from funcoesTermosol import geraSaida
geraSaida("nome",Re,U,deformation,forcas_int,tensoes)