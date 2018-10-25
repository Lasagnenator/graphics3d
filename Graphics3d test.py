#Graphics3d test
from Libraries.graphics3d import *
import pygame

pygame.init()
clock = pygame.time.Clock()
#Verticies of cube
cube = [[1,1,1], [1,1,-1], [1,-1,1], [1,-1,-1], [-1,1,1], [-1,1,-1], [-1,-1,1], [-1,-1,-1]]
#Indicies of edges of cube
edges = [[6,4], [0,4], [0,2], [2,6], [7,3], [3,1], [1,5], [5,7], [7,6], [3,2], [1,0], [5,4]]

#Normal startup
screen = pygame.display.set_mode([400,400])
screen.fill([255,255,255])

#Making matricies
s = Transformation("S", 3,3,3) #Scale
t = Transformation("T", 0,0,9) #Translate
rx = Transformation("Rx", 0)   #Rotation on x axis
ry = Transformation("Ry", 0.05)#Rotation on y axis
rz = Transformation("Rz", 0)   #Rotation on z axis

#initial transformation
cube_trans = [Translate(Scale(point, s), t) for point in cube]

def graph2pyg(rcube):
    #converts output of graphics to pygame scren coords
    return [[int(x*100+200), int(y*100+200)] for x,y in rcube]

def rotate_cube(rcube):
    #Rotates cube by Rx,Ry,Rz
    return [Rotate([0,0,9], point, rx,ry,rz) for point in rcube]

def draw_cube(rcube):
    #Draws cube verticies onto screen
    for point in rcube:
        pygame.draw.circle(screen, [0,0,0], point, 8)

def draw_edges(rcube):
    #Draws edges of the cube
    for s,e in edges:
        pygame.draw.line(screen, [0,0,0], rcube[s], rcube[e])

while True:
    #Main event loop
    events = pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            pygame.quit()
    #apply rotation
    rotated = rotate_cube(cube_trans)
    #Project points then convert to pygame screen coords
    gr = graph2pyg([Project(point) for point in rotated])
    #Draw
    draw_cube(gr)
    draw_edges(gr)
    #advance rotation
    cube_trans = rotated
    #update screen
    pygame.display.update()
    screen.fill([255,255,255])
    #fps
    clock.tick(30)
