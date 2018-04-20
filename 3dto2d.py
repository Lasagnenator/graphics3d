"""Converts 3d cooridante to 3d coordinates for rendering to a 2d screen
The whole library assumes that the camera is fixed at 0,0,0 looking at
positive z:

    Y
    |
    |
Z---\ <- 0,0,0
     \
      X

The library will project to a plane 1 unit away from the camera with 0,0
point on the plane intersecting 0,0,1. This means that when we project to
the screen. the x and y axis will be correct.
The whole world is rotated instead of the camera so that points only
rotate around the origin.

Steps to project something:
    1. point = (x,y,z)
    2. mat = Transformation(type, args)
    3. point = Translate(point, mat)
    4. point = Rotate(point, mat)
    5. if InFrustum(point, theta_x, theta_y):
        x,y = Project(point)"""
#Written by Matthew Richards

###The math functions we will be using in the whole library
import math
cos = math.cos
sin = math.sin
tan = math.tan
radians = math.radians
def tan_deg(x):
    """Accurate tangent for every 5 degrees."""
    x = x%360
    table = {0: 0,
             5: 0.175,
             10: 0.1763,
             15: 0.2679,
             20: 0.3640,
             25: 0.4663,
             30: 0.5773,
             35: 0.7002,
             40: 0.8391,
             45: 1,
             50: 1.1918,
             55: 1.4281,
             60: 1.7321,
             65: 2.1441,
             70: 2.7475,
             75: 3.7321,
             80: 5.6713,
             85: 11.430,
             }
    try:
        return table[x]
    except:
        return tan(radians(x))


###My on matrix so I don't need numpy as a dependecy
class Matrix():
    """Matrix class for matrix multiplication
Usage Matrix(x) @ Matrix(y)"""
    def __init__(self, matrix):
        if type(matrix)==Matrix:
            self.list = matrix.list
        else:
            self.list = matrix
    def __matmul__(self, matrix):
        matrix = Matrix(matrix)
        a = self.list
        b = matrix.list
        zip_b = list(zip(*b))
        return Matrix([[sum(map(lambda x, y: x * y, row_a, col_b)) for col_b in zip_b] for row_a in a])
    def __rmatmul__(self, matrix):
        matrix - Matrix(matrix)
        a = matrix.list
        b = self.list
        zip_b = list(zip(*b))
        return Matrix([[sum(map(lambda x, y: x * y, row_a, col_b)) for col_b in zip_b] for row_a in a])
    def __list__(self):
        return self.list

    
###Generates a trnsformation matrix to be used.
def Transformation(type, *args):
    """Generates a transformation matrix.
Type is either 'T', 'S', 'Rx', 'Ry', 'Rz'
Translation -> args = (x,y,z)
Scaling -> args = (x,y,z)
Rotate_x,y,z -> args = (theta)"""
    type = type.upper()
    if type == "T":
        return Matrix([[1, 0, 0, args[0]],
                       [0, 1, 0, args[1]],
                       [0, 0, 1, args[2]],
                       [0, 0, 0, 1]])
    elif type == "S":
        return Matrix([[args[0], 0, 0, 0],
                       [0, args[1], 0, 0],
                       [0, 0, args[2], 0],
                       [0, 0, 0, 1]])
    elif type == "Rx":
        return Matrix([[1, 0, 0, 0],
                       [0, cos(args[0]), -sin(args[0]), 0],
                       [0, sin(args[0]), cos(args[0])],
                       [0, 0, 0, 1]])
    elif type == "Ry":
        return Matrix([[cos(args[0]), 0, sin(args[0]), 0],
                       [0, 1, 0, 0],
                       [-sin(args[0]), 0, cos(args[0]), 0],
                       [0, 0, 0, 1]])
    elif type == "Rz":
        return Matrix([[cos(args[0]), -sin(args[0]), 0, 0],
                       [sin(args[0]), cos(args[0]), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

###Applies the rotation matrices
def Rotate(pivot_point, point, Rx, Ry, Rz):
    """point is a list (x,y,z)
pivot_point is a list (x,y,z)
Rx, Ry, Rz are rotation matrices to be applied."""
    Rx = Matrix(Rx)
    Ry = Matrix(Ry)
    Rz = Matrix(Rz)
    point[0] -= pivot_point[0]
    point[1] -= pivot_point[1]
    point[2] -= pivot_point[2]
    point_matrix = Matrix([[point[0]],[point[1]],[point[2]],[1]])
    new_matrix = ((Rx @ Ry)@ Rz )@ point_matrix
    final_matrix = [[1, 0, 0, pivot_point[0]],
                                 [0, 1, 0, pivot_point[1]],
                                 [0, 0, 1, pivot_point[2]],
                                 [0, 0, 0, 1]] @ new_matrix
    final_list = final_matrix.list
    point_x = final_list[0][0]
    point_y = final_list[1][0]
    point_z = final_list[2][0]
    return [point_x, point_y, point_z]


###Aplies the translation matrix
def Translate(point, T):
    """Point is a list (x,y,z)
T is a translation matrix"""
    point = Matrix([[point[0]],
                    [point[1]],
                    [point[2]],
                    [1]])
    T = Matrix(T)
    final_matrix = T @ point
    final_list = final_matrix.list
    point_x = final_list[0][0]
    point_y = final_list[1][0]
    point_z = final_list[2][0]
    return [point_x, point_y, point_z]

def Scale(point, S):
    """Point is a list (x,y,z)
S is a scaling matrix"""
    point = Matrix([[point[0]],
                    [point[1]],
                    [point[2]],
                    [1]])
    S = Matrix(S)
    final_matrix = S @ point
    final_list = final_matrix.list
    point_x = final_list[0][0]
    point_y = final_list[1][0]
    point_z = final_list[2][0]
    return [point_x, point_y, point_z]


###Projects the point to screen coordinates
def Project(point):
    """LAST STEP!
APPLY TRANSFORMATIONS AND ROTATIONS BEFORE THIS.
IT ASSUMES THAT THE CAMERA IS FACING POSITIVE Z AND THAT
THE PROGRAM HAS ALREADY CHECKED IF IT IS VISIBLE!

point is a list (x,y,z)
returns a x,y point with the 0,0 being 0,0,1 in 3d space"""
    x = point[0]/point[2]
    y = point[1]/point[2]
    return [x,y]


###Simple test if the point is in the frustum
def InFrustum(point, theta_x, theta_y, degrees=True):
    """Point is a list [x,y,z]. theta_x,y are angles that the planes of the frustum
come out of 0,0,0 along the x and y axis.
By default theta_x,y are in degrees, can be changed by setting degrees to
False which means that theta is in radians.
Returns True if point is on the edge of the frustum"""
    if degrees:
        tan_x = tan_deg(theta_x)
        tan_y = tan_deg(theta_y)
    else:
        tan_x = tan(x)
        tan_y = tan(y)
    x = point[0]
    y = point[1]
    z = point[2]
    if x<=z*tan_x and x>=-z*tan_x:
        if y<=z*tan_y and y>=-z*tan_y:
            return True
    return False

###The matrix multiplication function I found.
def matmul(a, b):
    zip_b = list(zip(*b))
    return ([[sum(map(lambda x, y: x * y, row_a, col_b)) for col_b in zip_b] for row_a in a])

