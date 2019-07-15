import math
def st_norm(u):
    '''标准正态分布'''
    x = abs(u) / math.sqrt(2)
    T = (0.0705230784, 0.0422820123, 0.0092705272,
         0.0001520143, 0.0002765672, 0.0000430638)
    E = 1 - pow((1 + sum([a * pow(x, (i + 1))
                          for i, a in enumerate(T)])), -16)
    p = 0.5 - 0.5 * E if u < 0 else 0.5 + 0.5 * E
    return (p)


def norm(a, sigma, x):
    '''一般正态分布'''
    u = (x - a) / sigma
    return (st_norm(u))