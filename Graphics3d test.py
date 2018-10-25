#Graphics3d test
from Libraries.graphics3d import *
import pygame

pygame.init()
clock = pygame.time.Clock()

cube = [[1,1,1], [1,1,-1], [1,-1,1], [1,-1,-1], [-1,1,1], [-1,1,-1], [-1,-1,1], [-1,-1,-1]]

edges = [[6,4], [0,4], [0,2], [2,6], [7,3], [3,1], [1,5], [5,7], [7,6], [3,2], [1,0], [5,4]]

screen = pygame.display.set_mode([400,400])
screen.fill([255,255,255])

s = Transformation("S", 3,3,3)
t = Transformation("T", 0,0,9)
rx = Transformation("Rx", 0)
ry = Transformation("Ry", 0.05)
rz = Transformation("Rz", 0)

cube_trans = [Translate(Scale(point, s), t) for point in cube]

def graph2pyg(rcube):
    return [[int(x*100+200), int(y*100+200)] for x,y in rcube]
    
def rotate_cube(rcube):
    return [Rotate([0,0,9], point, rx,ry,rz) for point in rcube]

def draw_cube(rcube):
    for point in rcube:
        pygame.draw.circle(screen, [0,0,0], point, 8)

def draw_edges(rcube):
    for s,e in edges:
        pygame.draw.line(screen, [0,0,0], rcube[s], rcube[e])

while True:
    events = pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            pygame.quit()
    rotated = rotate_cube(cube_trans)
    gr = graph2pyg([Project(point) for point in rotated])
    draw_cube(gr)
    draw_edges(gr)
    cube_trans = rotated
    pygame.display.update()
    screen.fill([255,255,255])
    clock.tick(30)
