import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represented by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

#indexes
AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    a = limit_color(calculate_ambient(ambient, areflect))
    d = limit_color(calculate_diffuse(light, dreflect, normal))
    s = limit_color(calculate_specular(light, sreflect, view, normal))
    inten = []
    for i in range(3):
        inten.append(int(a[i] + d[i] + s[i]))
    return limit_color(inten)

def calculate_ambient(alight, areflect):
    # color-of-ambient-light [0-255] * constant-of-ambient-reflection [0-1]
    am = []
    for i in range(3):
        am.append(alight[i] * areflect[i])
    return am

def calculate_diffuse(light, dreflect, normal):
    normalize(light[LOCATION])
    normalize(normal)
    dp = dot_product(light[LOCATION], normal)
    dif = []
    for i in range(3):
        dif.append(light[COLOR][i] * dreflect[i] * dp)
    return dif

def calculate_specular(light, sreflect, view, normal):
    normalize(light[LOCATION])
    normalize(normal)
    r = []
    for i in range(3):
        r.append(dot_product(normal, light[LOCATION]) * 2 * normal[i] - light[LOCATION][i])

    dp = dot_product(r, view)
    spec = []
    for i in range(3):
        spec.append(light[COLOR][i] * sreflect[i] * dp ** SPECULAR_EXP)
    return spec

def limit_color(color):
    if (color[AMBIENT] < 0):
        color[AMBIENT] = 0
    elif (color[AMBIENT] > 255):
        color[AMBIENT] = 255
    if (color[DIFFUSE] < 0):
        color[DIFFUSE] = 0
    elif (color[DIFFUSE] > 255):
        color[DIFFUSE] = 255
    if (color[SPECULAR] < 0):
        color[SPECULAR] = 0
    elif (color[SPECULAR] > 255):
        color[SPECULAR] = 255
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
