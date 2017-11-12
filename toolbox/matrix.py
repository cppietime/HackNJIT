# Matrix, row-major

import math

def id(n):
    return [1 if x//n==x%n else 0 for x in range(n*n)]

def scale(m,n):
    for i in range(len(m)):
        m[i] *= n
    return m

def size(a,b,c):
    return [a,0,0,
            0,b,0,
            0,0,c]

def rotate3(angle, axis):
    rad = math.radians(angle)
    if axis.lower()=='x':
        return [1.,0,0,
                0,math.cos(rad),math.sin(rad),
                0,-math.sin(rad),math.cos(rad)]
    if axis.lower()=='y':
        return [math.cos(rad),0,-math.sin(rad),
                0,1.,0,
                math.sin(rad),0,math.cos(rad)]
    if axis.lower()=='z':
        return [math.cos(rad),math.sin(rad),0,
                -math.sin(rad),math.cos(rad),0,
                0,0,1.]
