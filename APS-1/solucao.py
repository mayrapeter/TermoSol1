import math
import numpy as numpy

#matrizes
A = [[1.59e8, -0.4e8, -0.54e8], [-0.4e8, 1.7e8, 0.4e8], [-0.54e8, 0.4e8, 0.54e8]]
U = [0, 0, 0]
b = [0, 150, -100]
#metodo jacobi
#n iterações
print(len(A))
condicao = True
while condicao:
    for i in range(0,len(A)):
        sub = 0
        for j in range(0, len(A)):
            if i != j:
                sub -= A[i][j] * U[j]

        new_u = (b[i] + sub)/A[i][i]

        if new_u != 0:

            erro = abs((new_u - U[i])/new_u)

            if erro < 1e-10:
                condicao = False
                break

            U[i] = new_u

print(U)






#metodo gauss-seidel