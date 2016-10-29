from random import *
import pygame
import math
from pygame import gfxdraw
pygame.init()

size = [1400, 700]
screen = pygame.display.set_mode(size)
scale = 150.0
x_offset = 0.0
y_offset = 0.0
mouse_pos_old = [0, 0]
font = pygame.font.Font("AvenirLTPro-Black.otf", 30)


def coor_to_pixel(coors = [0.0, 0.0], f_or_i = False):
    if f_or_i == False:
        return [int(coors[0]*scale+size[0]/2-x_offset*scale), int(-coors[1]*scale+size[1]/2-y_offset*scale)]
    else:
        return [coors[0]*scale+size[0]/2-x_offset*scale, -coors[1]*scale+size[1]/2-y_offset*scale]

def pixel_to_coor(pixel = [0, 0]):
    return [int((pixel[0]+x_offset*scale-size[0]/2)/scale), int(-(pixel[1]+y_offset*scale-size[0]/2)/scale)]

path = []
path.append([])
path_len = 0

old_vx = 0.5
one_p_x = -2.0
one_p_y = 1.0
ion_one_x = -2.0
ion_one_y = 1.0
ion_one_vx = 0.5
ion_one_vy = 0.0
ion_one_z = 1.0

two_p_x = 0.0
two_p_y = 0.0
ion_two_x = 0.0
ion_two_y = 0.0
ion_two_vx = 0.0
ion_two_vy = 0.0
ion_two_z = 79.0

bounding_box = [-3.5, 2.5, 7.0, 5.0]

e_2 = 14.4
a = 0.529*0.8834/math.sqrt(ion_one_z**(2.0/3.0)+ion_two_z**(2.0/3.0))

quit_p = False
clock = pygame.time.Clock()
elapsed = 0.0
mouse_left_down = False
while not quit_p:
    #seconds = elapsed/1000.0
    seconds = 0.01/(ion_one_vx**2+ion_one_vy**2)**(1/2.0)
    screen.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit_p = True
            break
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                quit_p = True
                break
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 5 and scale > 0.1:
                scale /= 1.1
            if e.button == 4:
                scale *= 1.1
            if e.button == 1:
                mouse_left_down = True
                mouse_pos_old[0] = pygame.mouse.get_pos()[0]
                mouse_pos_old[1] = pygame.mouse.get_pos()[1]
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                mouse_left_down = False
        if e.type == pygame.MOUSEMOTION and mouse_left_down:
            mouse_pos = []
            mouse_pos.append(pygame.mouse.get_pos()[0])
            mouse_pos.append(pygame.mouse.get_pos()[1])
            x_offset += (mouse_pos_old[0]-mouse_pos[0])/scale
            y_offset += (mouse_pos_old[1]-mouse_pos[1])/scale
            mouse_pos_old[0] = mouse_pos[0]
            mouse_pos_old[1] = mouse_pos[1]
    r = math.sqrt((ion_one_x-ion_two_x)**2+(ion_one_y-ion_two_y)**2)
    F = -ion_one_z*ion_two_z*e_2*math.e**(-r/a)*(a+r)/(a*r**2)
    a_one = F/ion_one_z
    a_two = F/(ion_two_z*2)
    d_x = ion_one_x-ion_two_x
    d_y = ion_one_y-ion_two_y
    angle = 0.0
    try:
        angle = math.atan(abs(d_y/d_x))
    except:
        angle = math.pi/2
    if d_x < 0.0:
        ion_one_vx += a_one*math.cos(angle)*seconds
       # ion_two_vx -= a_two*math.cos(angle)*seconds
    else:
        ion_one_vx -= a_one*math.cos(angle)*seconds
       # ion_two_vx += a_two*math.cos(angle)*seconds
    if d_y < 0.0:
        ion_one_vy += a_one*math.sin(angle)*seconds
       # ion_two_vy -= a_two*math.sin(angle)*seconds
    else:
        ion_one_vy -= a_one*math.sin(angle)*seconds
       # ion_two_vy += a_two*math.sin(angle)*seconds

    ion_one_x += ion_one_vx*seconds
    ion_one_y += ion_one_vy*seconds
    ion_two_x += ion_two_vx*seconds
    ion_two_y += ion_two_vy*seconds

    path[path_len].append([ion_one_x, ion_one_y])

    p_one_c = coor_to_pixel([one_p_x, one_p_y])
    p_two_c = coor_to_pixel([two_p_x, two_p_y])
    one_p_x = ion_one_x
    one_p_y = ion_one_y
    two_p_x = ion_two_x
    two_p_y = ion_two_y
    ion_one_c = coor_to_pixel([ion_one_x, ion_one_y])
    ion_two_c = coor_to_pixel([ion_two_x, ion_two_y])
    if len(path[path_len]) > 1:
        for p in range(path_len+1):
            pygame.draw.aalines(screen, (255, 0, 0), False, [coor_to_pixel(x, True) for x in path[p]], 1)
    gfxdraw.aacircle(screen, ion_one_c[0], ion_one_c[1], int(ion_one_z**(1.0/3.0)*scale/45.0), (255, 0, 0))
    gfxdraw.filled_circle(screen, ion_one_c[0], ion_one_c[1], int(ion_one_z**(1.0/3.0)*scale/45.0), (255, 0, 0))
    gfxdraw.aacircle(screen, ion_two_c[0], ion_two_c[1], int(ion_two_z**(1.0/3.0)*scale/45.0), (0, 0, 255))
    gfxdraw.filled_circle(screen, ion_two_c[0], ion_two_c[1], int(ion_two_z**(1.0/3.0)*scale/45.0), (0, 0, 255))
    try:
        angle = math.atan(abs(ion_one_vy/ion_one_vx))
    except:
        angle = math.pi/2.0

    bounding_box_coordinates = coor_to_pixel([bounding_box[0], bounding_box[1]])
    bounding_box_size = [bounding_box[2]*scale, bounding_box[3]*scale]
    pygame.draw.rect(screen, (0, 0, 0), [bounding_box_coordinates[0], bounding_box_coordinates[1], bounding_box_size[0], bounding_box_size[1]], 1)

    label = font.render("V_x: " + str(old_vx), 1, (0, 0, 0))
    screen.blit(label, [10, 10])
    label = font.render("Ang. radians: " + str(angle), 1, (0, 0, 0))
    screen.blit(label, [10, label.get_rect()[3]+10])

    if ion_one_x > bounding_box[0]+bounding_box[2] or ion_one_y < bounding_box[1]-bounding_box[3] or ion_one_y > bounding_box[1]:
        print old_vx, ", ", angle
        path.append([])
        path_len += 1
        old_vx += 0.25
        ion_one_vx = old_vx
        ion_one_vy = 0.0
        ion_one_x = -2.0
        ion_one_y = 1.0
        one_p_x = -2.0
        one_p_y = 1.0
    pygame.display.update()
    #elapsed = clock.tick(60)
