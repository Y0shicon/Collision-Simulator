from __future__ import division
from sympy import *

from gekko import GEKKO
import timeit

def main():
    m = GEKKO()
    x,y,w = [m.Var(1) for i in range(3)]
    m.Equations([4*x-2*y+3*w==1,\
                x+3*y-4*w==-7,\
                3*x+y+2*w==5])
    m.solve(disp=False)
    print(x.value,y.value,w.value)


x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)

def main2():
    print(linsolve([4*x - 2*y + 3*z - 1,x + 3*y - 4*z + 7, 3*x + y + 2*z - 5 ], (x, y, z)))

import numpy as np

def main3():
    a = np.array([[4,-2,3], [1,3,-4], [3,1,2]])
    b = np.array([1,-7,5])
    print(np.linalg.solve(a,b))

'''
'''

a = 1
b = 7
c = 5

print(linsolve([4*x - 2*y + 3*z - a,x + 3*y - 4*z + b, 3*x + y + 2*z - c ], (x, y, z)))

def main4():
    m1 = m2 = 5
    u1cn = 5
    u2cn = 0
    u1ct = 6.55
    u2ct = 0
    e = 1

    a = np.array([[m1, m2], [-1, 1]])
    b = np.array([m1*u1cn + m2*u2cn, e*(u2cn - u1cn)])

    v1cn, v2cn = np.linalg.solve(a,b)
    v1cn, v2cn = round(v1cn), round(v2cn)

    print(v1cn, v2cn)

print(timeit.timeit(setup = 'from gekko import GEKKO', stmt = main, number = 1))
print(timeit.timeit(stmt = main2, number = 1))
print(timeit.timeit(stmt = main3, number = 1))
print(timeit.timeit(stmt = main4, number = 1))

