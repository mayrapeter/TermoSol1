import numpy as np
#from scipy import linalg

A = float(input('Insira o valor de area (A)')) #0.02
L = float(input('Insira o valor de comprimento (L)'))#2
P = float(input('Insira o valor de forca (P)'))#50000
E = float(input('Insira o valor de modulo de elasticidade (E)'))#200e9
g = int(input('Insira o grau de liberdade'))
n = 1
nos_presos = []
while (n != 0):
    n = int(input('Insira o numero de um nó preso, se nao houver digite 0'))
    if n != 0:
        nos_presos.append(n)

const = E*A/L #matriz de rigidez

Rx = -P
#Formar as matrizes
K = [[1,-1],[-1,1]]
Kg = np.zeros([g, g])
i = 0
for i in range(Kg.shape[0]-1):
    Kg[i:i+2, i:i+2] += K

print(Kg)

F = [Rx,50000]

#condicoes de contorno

for each in nos_presos:
    print('grau ',each)
    Kg = np.delete(Kg, each-1, 0) 
    Kg = np.delete(Kg, each-1, 1) 
    

print(Kg) 

#i = np.dot(linalg.inv(K),F)

# u1 = 0
# 50000 = ((E*A)/L)*u2

#print("i1=",i[0],"i2=",i[1])