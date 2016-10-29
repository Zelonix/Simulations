from random import *
import pygame
import math
from pygame import gfxdraw
import sys
pygame.init()

size = [1366, 768]
screen = pygame.display.set_mode(size)#, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
scale = 0.04
offset = [0.0, 0.0]
mouse_pos_old = [0, 0]
font = pygame.font.Font("AvenirLTPro-Black.otf", 20)
#font = pygame.font.SysFont("monospace", 20)
c_seed = randint(0, sys.maxint)
#c_seed = 1133927547836721332
print c_seed
dot_count = 10
dots = []
dots_vel = []
dots_color = []
dots_mass = []
dot_paths = []
dots_original_id = []
dots_alive = []
background_color = [0, 0, 0]
opp_background = [255-background_color[0], 255-background_color[1], 255-background_color[2]]

seed(c_seed)
dots.append([0.0, 0.0])
dots_vel.append([0, 0])
dots_color.append(opp_background)
dots_mass.append(1000000000.0)
dot_paths.append([])
dots_original_id.append(0)
dots_alive.append(True)
for i in range(1, dot_count):
    dots.append([(random()-0.5)*size[0]*20.0, (random()-0.5)*size[1]*20.0])
    dots_vel.append([(random()-0.5)*5000.0, (random()-0.5)*5000.0])
    #dots_vel.append([0.0, 0.0])
    #dots_color.append([randint(0, 255), randint(0, 255), randint(0, 230)])
    dots_color.append([randint(20, 230), randint(100, 150), randint(20, 230)])
    dots_mass.append(random()*4000000.0+4000000.0)
    dot_paths.append([])
    dots_original_id.append(i)
    dots_alive.append(True)

def coor_to_pixel(coors = [0.0, 0.0], i_or_f = False):
    if i_or_f == False:
        return [int(coors[0]*scale+size[0]/2-offset[0]*scale), int(-coors[1]*scale+size[1]/2-offset[1]*scale)]
    else:
        return [coors[0]*scale+size[0]/2-offset[0]*scale, -coors[1]*scale+size[1]/2-offset[1]*scale]
def pixel_to_coor(pixel = [0, 0]):
    return [int((pixel[0]+offset[0]*scale-size[0]/2)/scale), int(-(pixel[1]+offset[1]*scale-size[0]/2)/scale)]
def display_info():
    font = pygame.font.Font("AvenirLTPro-Black.otf", 20)
    label = font.render("Zoom: " + str(round(scale, 3)), 1, opp_background)
    screen.blit(label, [10, 10])
    label = font.render("Planets alive: " + str(sum(dots_alive)) + "/" + str(dot_count), 1, opp_background)
    screen.blit(label, [10, 10+label.get_rect()[3]])
    label = font.render("Seed: " + str(c_seed), 1, opp_background)
    screen.blit(label, [10, 10+label.get_rect()[3]*2])
    label = font.render("Sim. speed: " + str(simulation_speed), 1, opp_background)
    screen.blit(label, [10, 10+label.get_rect()[3]*3])
    label = font.render("G: " + str(acceleration_const), 1, opp_background)
    screen.blit(label, [10, 10+label.get_rect()[3]*4])

clock = pygame.time.Clock()
elapsed = 0
quit_p = False
pressed = False
mouse_pos = [0, 0]
mouse_left_down = False
pause = False
accumulator = 0.0
seconds = 0.01
simulation_speed = 1.0
acceleration_const = 100.0
selected = -1
while not quit_p:
    v_seconds = elapsed/1000.0*simulation_speed
    accumulator += v_seconds
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_p = True
                break
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    quit_p = True
                    break
                if e.key == pygame.K_p:
                    pause = not pause
                if e.key == pygame.K_KP_PLUS:
                    if simulation_speed < 0.1:
                        simulation_speed += 0.1
                    else:
                        sim_add = 10**math.floor(math.log10(simulation_speed)+1.0)/10.0
                        simulation_speed += sim_add
                    #if simulation_speed >= 1.0:
                     #   simulation_speed += 1.0
                    #else:
                     #   simulation_speed += 0.1
                if e.key == pygame.K_KP_MINUS:
                    sim_add = 10**math.floor(math.log10(simulation_speed)+1.0)/10.0
                    if sim_add == simulation_speed:
                        simulation_speed -= sim_add/10.0
                    else:
                        simulation_speed -= sim_add
                    if sim_add < 0.1:
                        sim_add = 0.0
                    #if simulation_speed > 1.0:
                     #   simulation_speed -= 1.0
                    #elif simulation_speed > 0.0:
                     #   simulation_speed -= 0.1
                if e.key == pygame.K_KP_MULTIPLY:
                    acceleration_const *= 1.1
                if e.key == pygame.K_KP_DIVIDE:
                    acceleration_const /= 1.1
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 5:
                    scale /= 1.1
                if e.button == 4 and scale < 37.0:
                    scale *= 1.1
                if e.button == 1:
                    mouse_left_down = True
                    mouse_pos_old[0] = pygame.mouse.get_pos()[0]
                    mouse_pos_old[1] = pygame.mouse.get_pos()[1]
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    mouse_left_down = False
            if e.type == pygame.MOUSEMOTION and mouse_left_down:
                #mouse_pos = []
                #mouse_pos.append(pygame.mouse.get_pos()[0])
                #mouse_pos.append(pygame.mouse.get_pos()[1])
                mouse_pos = pygame.mouse.get_pos()
                offset[0] += (mouse_pos_old[0]-mouse_pos[0])/scale
                offset[1] += (mouse_pos_old[1]-mouse_pos[1])/scale
                mouse_pos_old[0] = mouse_pos[0]
                mouse_pos_old[1] = mouse_pos[1]
        if pause == False:
            break

    while accumulator >= seconds:
        join = []
        for i in range(dot_count):
            if dots_alive[i]:
                for j in range(dot_count):
                    if dots_alive[j]:
                        if i == j:
                            continue
                        if (dots[i][0]-dots[j][0])**2+(dots[i][1]-dots[j][1])**2 < ((dots_mass[i])**(1.0/3.0)+(dots_mass[j])**(1.0/3.0))**2:
                            if len(join) > 0:
                                for x in range(len(join)):
                                    if i in join[x] and not (j in join[x]):
                                        join[x].append(j)
                                        break
                                    if not (j in join[x]):
                                        join.append([i, j])
                                        break
                            else:
                                join.append([i, j])
                            continue
                        d_y = dots[i][1]-dots[j][1]
                        d_x = dots[i][0]-dots[j][0]
                        r = math.sqrt(d_x**2+d_y**2)
                        s_a = d_y/1.0/r
                        c_a = d_x/1.0/r
                        acceleration = acceleration_const/(d_y**2+d_x**2)*dots_mass[j]
                        dots_vel[i][0] -= acceleration*d_x/1.0/r*seconds
                        dots_vel[i][1] -= acceleration*d_y/1.0/r*seconds

                dot_paths[i].append([dots[i][0], dots[i][1]])
                while len(dot_paths[i]) > 500:
                    del dot_paths[i][0]
        for i in range(dot_count):
            dots[i][0] += dots_vel[i][0]*seconds
            dots[i][1] += dots_vel[i][1]*seconds

        total_velocities = sum([abs(i[0]) for i in dots_vel])
        seconds = min(1.0/60.0, 100.0/total_velocities)

        for x in range(len(join)):
            try:
                for y in range(1, len(join[x])):
                    dots_color[join[x][0]][0] = int((dots_color[join[x][0]][0]*dots_mass[join[x][0]]+dots_color[join[x][y]][0]*dots_mass[join[x][y]])/1.0/(dots_mass[join[x][0]]+dots_mass[join[x][y]]))
                    dots_color[join[x][0]][1] = int((dots_color[join[x][0]][1]*dots_mass[join[x][0]]+dots_color[join[x][y]][1]*dots_mass[join[x][y]])/1.0/(dots_mass[join[x][0]]+dots_mass[join[x][y]]))
                    dots_color[join[x][0]][2] = int((dots_color[join[x][0]][2]*dots_mass[join[x][0]]+dots_color[join[x][y]][2]*dots_mass[join[x][y]])/1.0/(dots_mass[join[x][0]]+dots_mass[join[x][y]]))
                    if dots_mass[join[x][y]] > dots_mass[join[x][0]]:
                        dots[join[x][0]][0] = dots[join[x][y]][0]
                        dots[join[x][0]][1] = dots[join[x][y]][1]
                    dots_mass[join[x][0]] += dots_mass[join[x][y]]
                    dots_vel[join[x][0]][0] = (dots_vel[join[x][0]][0]*(dots_mass[join[x][0]]-dots_mass[join[x][y]])+dots_vel[join[x][y]][0]*dots_mass[join[x][y]])/dots_mass[join[x][0]]
                    dots_vel[join[x][0]][1] = (dots_vel[join[x][0]][1]*(dots_mass[join[x][0]]-dots_mass[join[x][y]])+dots_vel[join[x][y]][1]*dots_mass[join[x][y]])/dots_mass[join[x][0]]
                    dots_alive[join[x][y]] = False
                    dot_paths[join[x][y]] = []
            except:
                continue
        accumulator -= seconds

    #screen.fill((255, 255, 255))
    screen.fill(background_color)
    for i in range(dot_count):
        if len(dot_paths[i]) > 1:
            pygame.draw.aalines(screen, dots_color[i], False, [coor_to_pixel(x) for x in dot_paths[i]])

    for i in range(dot_count):
        if dots_alive[i]:
            pixel_points = coor_to_pixel(dots[i])
            radius = int((dots_mass[i])**(1.0/3.0)*scale)
            if not (pixel_points[0]+radius < 0 or pixel_points[0]-radius > size[0] or pixel_points[1] < 0 or pixel_points[1] > size[1]):
                gfxdraw.filled_circle(screen, pixel_points[0], pixel_points[1], radius, dots_color[i])
                if radius > 1:
                    gfxdraw.aacircle(screen, pixel_points[0], pixel_points[1], radius, dots_color[i])
                #font = pygame.font.Font("AvenirLTPro-Black.otf", int(scale*radius/10.0))
                #label = font.render(str(i), 1, (0, 0, 0))
                #screen.blit(label, [pixel_points[0]-label.get_rect()[2]/2, pixel_points[1]-label.get_rect()[3]/2])
            temp_mouse_pos = pygame.mouse.get_pos()
            if (pixel_points[0]-temp_mouse_pos[0])**2+(pixel_points[1]-temp_mouse_pos[1])**2 < radius**2:
                if pygame.mouse.get_pressed()[2]:
                    selected = i

    #font = pygame.font.Font("AvenirLTPro-Black.otf", 20)
    if selected > -1:
        label = font.render("Mass: " + str(dots_mass[selected]), 1, opp_background)
        screen.blit(label, [10, size[1]-label.get_rect()[3]])
        label = font.render("X: " + str(round(dots[selected][0], 2)) + ", Y: " + str(round(dots[selected][1], 2)), 1, opp_background)
        screen.blit(label, [10, size[1]-label.get_rect()[3]*2])
        label = font.render("X vel: " + str(dots_vel[selected][0]) + ", Y vel: " + str(dots_vel[selected][1]), 1, opp_background)
        screen.blit(label, [10, size[1]-label.get_rect()[3]*3])
        if dots_alive[selected]:
            label = font.render("Alive", 1, opp_background)
        else:
            label = font.render("Dead", 1, opp_background)
        screen.blit(label, [10, size[1]-label.get_rect()[3]*4])
        label = font.render("Planet id: " + str(selected), 1, opp_background)
        screen.blit(label, [10, size[1]-label.get_rect()[3]*5])

    display_info()
    pygame.display.update()
    elapsed = clock.tick(60)