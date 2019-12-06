#!/usr/bin/env python2
from math import sqrt, pow


def dotProduct(a, b):
    c = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return c



def abs_dotProduct(c):
    if c < 0:
        return -c
    else:
        return c


def crossProduct(a, b):
    cross = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    return cross


def vector_length(c):
    return sqrt(pow(c[0], 2) + pow(c[1], 2) + pow(c[2], 2))


def subtract(a, b):
    sub = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
    return sub


def add(a, b):
    sum = [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
    return sum


def unit_vec(c):
    length_c = sqrt(pow(c[0], 2) + pow(c[1], 2) + pow(c[2], 2))
    return [c[0] / length_c, c[1] / length_c, c[2] / length_c]


def make_polygon(ee_xyz):
    line = []
    for i in range(len(ee_xyz / 3)):
        line.extend = [ee_xyz[3 * i + 3] - ee_xyz[3 * i],
                       ee_xyz[3 * i + 4] - ee_xyz[3 * i + 1],
                       ee_xyz[3 * i + 5] - ee_xyz[3 * i + 2]]
    return line
def scale_vec(a,b):
    length_b = vector_length(b)
    scale_vec = [a[0]/length_b, a[1]/length_b, a[2]/length_b]   
    return scale_vec

def scale_scale(a,t):
    scale_scale = [a[0]*t,a[1]*t,a[2]*t]
    return scale_scale