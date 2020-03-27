import numpy as np
import math

from funcoesTermosol import importa
[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xlsx')

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

def getCoor(N, nm):
    elemento = []
    for i in range(0,nm):
        elemento.append([N[0][i], N[1][i]])
    return elemento

def Ke(X1,X2,Y1,Y2,E,A):

    l, Sen, Cos = SenCos(X1,X2,Y1,Y2)
    k = (E * A)/ l 
    #forma matriz
    ke = [[Cos**2, Cos*Sen, -Cos**2, -Cos*Sen],[Cos*Sen, Sen*Sen, -Cos*Sen, -Sen*Sen], [-Cos**2, -Cos*Sen, Cos**2, Cos*Sen], [-Cos*Sen, -Sen*Sen, Cos*Sen, Sen*Sen]] 
    for i in range(0, len(ke)):
        for j in range(0,len(ke[0])):
            ke[i][j] = ke[i][j] * k
    return ke
  
#Programa main
for i in range(0,nm):
    E = Inc[i,2]
    A = Inc[i,3]

coor_nos = getCoor(N, nm)
print('cordenadas', coor_nos)
print('nm', nm)

#cada ke para cada elemento

ke_g = []
E = []
A = []

for i in range(0,nm):
    E.append(Inc[i,2])
    A.append(Inc[i,3])

for i in range(0,nm - 1):
    ke_g.append(Ke(coor_nos[i][0], coor_nos[i+1][0], coor_nos[i][1], coor_nos[i+1][1], E[i], A[i]))

ke_g.append(Ke(coor_nos[0][0], coor_nos[nm - 1][0], coor_nos[0][1], coor_nos[nm - 1][1], E[nm - 1], A[nm - 1]))

g_liber = int(input('Digite o numero de graus de liberdade'))

Kg = np.zeros([nm*g_liber, nm*g_liber])
for i in range(0, Kg.shape[0]-len(ke_g)):    
    for j in range(0, len(ke_g)):
        Kg[i:i+4, i:i+4] += ke_g[j]
    

print(Kg)







# from funcoesTermosol import plota
# plota(N,Inc)


# from funcoesTermosol import geraSaida
# geraSaida(nome,Ft,Ut,Epsi,Fi,Ti)