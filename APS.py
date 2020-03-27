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
    ke = np.array([[Cos**2, Cos*Sen, -Cos**2, -Cos*Sen],[Cos*Sen, Sen*Sen, -Cos*Sen, -Sen*Sen], [-Cos**2, -Cos*Sen, Cos**2, Cos*Sen], [-Cos*Sen, -Sen*Sen, Cos*Sen, Sen*Sen]])

    return (np.multiply(ke,  k))
  
#Programa main
coor_elementos = getCoorElemento(nm, N)
#cada ke para cada elemento

ke_g = []
E = []
A = []
for i in range(0,nm):
    E.append(Inc[i,2])
    A.append(Inc[i,3])



for i in range(0,nm - 1):
    ke_g.append(Ke(coor_elementos[i][0], coor_elementos[i][1], E[i], A[i]))

ke_g.append(Ke(coor_elementos[0][0], coor_elementos[0][1], E[nm - 1], A[nm - 1]))


print(ke_g)
g_liber = 2
Kg = np.zeros([nm*g_liber, nm*g_liber])
for i in range(0, Kg.shape[0]-len(ke_g)):    
    for j in range(0, len(ke_g)):
        Kg[i:i+4, i:i+4] += ke_g[j]

#montagem de vetor de carga global

Pg = F

#aplicar condicoes de contorno
for each in R:
    Kg = np.delete(Kg, int(each[0]), 0) 
    Kg = np.delete(Kg, int(each[0]), 1) 
#print(Kg)
#solucao de sistemas de equação (solucao.py)

#determinaçao das reacoes de apoio estrutural/ deformacao e tensao do elemento
    







# from funcoesTermosol import plota
# plota(N,Inc)


# from funcoesTermosol import geraSaida
# geraSaida(nome,Ft,Ut,Epsi,Fi,Ti)