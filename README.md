# graphics3d
A library that manipulates 3d points and projects them to screen coordinates.

# Dependencies
None. This is a standalone library for python 3.x. It uses the builtin math module just for the trigonometric functions.

# Installation
To install this library, you simply just download it into you python library folder or work folder.

# Use
To start off go ahead and import it using
```
import graphics3d
from graphics3d import *
```

To use this library, you will need to know that this library relies on matrices. However it does not use Numpy or any other matrix library, it uses its own class called Matrix. The user/programmer does not need to know matrices as that is all handled by the library. The library will generate the matrices for you.
You create a matrix object by:
```
Matrix([[[], ...], [[], [], []...], ...]) -> Matrix
Matrix.list -> [[[], ...], [[], [], []...], ...]
```

For our purposes, we are going to mostly use 4x4 and 1x4 matrices for representing 3d coordinates and manipulationg them.
The matrix class has its own matrix multiplication algorithm that computes it as it should be. Use `Matrix @ Matrix` to perform a matrix multiplication.

There is a Tranformation function which will generate matrices for you based on the type you want. The use of this function is:
```
Transformation(type, *args) -> Matrix
```
type is a string that is either 'T', 'S', 'Rx', 'Ry', 'Rz'. T is translation. S is scaling. R is rotation (along specific axis)
args is going to be x,y,z (NOT A LIST) when t or s is chosen.
When the rotation is chosen, it is a single variable theta in radians.

There are seperate functions for translation and rotation that compute the matrices for you and turn it back to 3d points however you can do it yourself by using the matrix multiplication operand. The use of the functions is below.
```
Translate(point, T) -> [x,y,z]
Rotate(pivot_point, point, Rx, Ry, Rz) -> [x,y,z]
Scale(point, S) -> [x,y,z]
```
In both functions, point is a list of `[x,y,z]`. pivot_point is also a list of `[x,y,z]`.
T, S, R are all matrices but do not have to be a Matrix class. They will be converted automatically to be used.

There is a function called InFrustum which detects if a point is in the frustum described by the angles that the faces meet with the x and y axis. It is used as follows.
```
InFrustum(point, theta_x, theta_y, degrees=True) -> bool
```
Here point is a list `[x,y,z]` and `theta_x,y` is the angle horizontally (x) or vertically (y) that the camera can see. It will return False for when the point is technically inside the frustum but on the face. `degrees` is a variable that when true will make the function interprete theta as a degree while when it is false, it will be interpreted as radians. THe benefit to using degrees is that I have defined them for every 5 degrees so there are no floating-point errors. This should be enough for any use however you can expand this to whatever precision you want later.

A function called Multi_Transform is availiable that will perform many transformations in the order described by the order of the arguments. For rotation, only rotation around 0,0,0 is availiable currently. To use it use:
```
Multi_Transform(point, args) -> [x,y,z]
```
Here point is a list `[x,y,z]` and args is a list of transformations to be done in the specified order.

And finally, the last step. Projection onto the screen. There is a function called Project which will project a 3d point onto the 2d screen. This assumes that the camera is facing towards the positive z axis, is fixed at (0,0,0) and that InFrustum has already been checked. Apply all transformations before this function as you cannot change them afterwards. 
```
Project(point) -> [x,y]
```
The input of Project is a list `[x,y,z]`.
The point (0,0) on the returned value is the middle of the screen and is equivalent to the point (0,0,1)

# Acknowledgments

The matrix multiplication function was found here: https://stackoverflow.com/a/10508239/6572831

All of my work is free to use and create with however you must credit me and provide a link to this repository when used.
This whole library is my own work.
