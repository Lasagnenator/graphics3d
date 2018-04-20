# 3dto2d
A library that manipulates 3d points and projects them to screen coordinates.

# Installation
To install this library, you simply just download it into you python library folder or work folder.

# Use
To use this library, you will need to know that this library relies on matrices. However it does not use Numpy, it uses its own class called Matrix. The user/programmer does not need to know matrices as that is all handle by the library.
You create a matrix object by:
```
Matrix([[[], ...], [[], [], []...], ...]) -> Matrix
```

For our purposes, we are going to mostly use 4x4 and 1x4 matrices for representing 3d coordinates and manipulationg them.
The matrix class has its own matrix multiplication algorithm that computes it as it should be. Use Matrix @ Matrix to perform a matrix multiplication

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

# Acknowledgments
All of my work is free to use and create with however you must credit me and provide a link to this repository when used.
This whole library is my own work and I came up with the algorithms by my own.
