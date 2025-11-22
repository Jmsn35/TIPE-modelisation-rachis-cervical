import pygame
import pymunk
import pymunk.pygame_util
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

def setup_space():
    space = pymunk.Space()
    space.gravity = (0,9810)
    return space

def add_crane(space, position,color):
    #definition de la masse
    masse = 0.1
    #definition de la forme du crane en respectant l'echelle 1cm -> 10 pixels
    vertices = [(0, -76),(-20, -73),(-50, -56),(-70, -28),(-75, 0),(-70, 30),(-60, 54),(-50, 72),(-30, 98),(-10, 110),(0,112),(10, 110),(30, 98),(50, 72),(60, 54),(70, 30),(75, 0),(70, -28),(50, -56),(20, -73),(0, -76),]

    #calcule du moment d'inertie
    moment = pymunk.moment_for_poly(masse, vertices)

    #creation du crane
    body = pymunk.Body(masse, moment, body_type=pymunk.Body.DYNAMIC,)
    body.position = position
    shape = pymunk.Poly(body, vertices,)

    #definition des intereactions
    shape.filter = pymunk.ShapeFilter(categories=0x01, mask=0x04)

    # friction pour des interactions réalistes
    shape.friction = 0.5
    shape.color = color
    space.add(body, shape)
    return body


def add_vertebre(space, position, fixed=False):
    mass = 0.0001
    radius = 10
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body_type = pymunk.Body.STATIC if fixed else pymunk.Body.DYNAMIC
    body = pymunk.Body(mass, moment, body_type=body_type)
    body.position = position
    shape =pymunk.Circle(body, radius)
    shape.filter = pymunk.ShapeFilter(categories=0x02, mask=0x00)
    space.add(body, shape)
    return body

def add_joint(space, body1, body2, min_angle, max_angle,anchor1,anchor2):

    joint = pymunk.PinJoint(body1, body2, anchor1, anchor2)
    space.add(joint)
    # Convertir degrees a radians pour les contraintes
    min_angle_rad = math.radians(min_angle)
    max_angle_rad = math.radians(max_angle)
    rotary_limit = pymunk.RotaryLimitJoint(body1, body2, min_angle_rad, max_angle_rad)
    space.add(rotary_limit)


def add_rectangle(space, position, size):
    width, height = size
    mass = 0
    moment = pymunk.moment_for_box(mass, (width, height))
    body_type = pymunk.Body.STATIC
    body = pymunk.Body(mass, moment, body_type=body_type)
    body.position = position
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.filter = pymunk.ShapeFilter(categories=0x0, mask=0x002)
    space.add(body, shape)
    return body


def add_muscle(space, body1, body2, rest_length, raideur, amortissement,position1,position2):
    muscle = pymunk.DampedSpring(body1, body2, position1, position2, rest_length, raideur, amortissement)
    space.add(muscle)

def add_muscle(space, body1, body2, rest_length, raideur, amortissement, position1, position2):
    def force_function(spring, dist):
        if dist > rest_length:
            return spring.damping * (dist - rest_length)
        else:
            return 0

    muscle = pymunk.DampedSpring(body1, body2, position1, position2, rest_length, raideur, amortissement)
    muscle.spring_force_func = force_function
    space.add(muscle)

def add_projectile(space, position):
    mass = 1
    radius = 40
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, pymunk.Body.DYNAMIC)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.filter = pymunk.ShapeFilter(categories=0x04, mask=0x01)
    shape.friction = 0.5
    space.add(body, shape)
    return body

def launch_projectile( projectile, position, velocity):
    projectile.position = position
    projectile.velocity = velocity
    projectile.angle = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    space = setup_space()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    epaules = add_rectangle(space, (300, 470), (100, 20))

    crane = add_crane(space, (300, 290),pygame.Color('SteelBlue1'))

    vertebres = [add_vertebre(space, (300, 450 - i * 20)) for i in range(7)]

    add_joint(space, crane, vertebres[6], -10, 10, (0, 30), (0, -10))  # Occiput-C1
    add_joint(space, vertebres[5], vertebres[6], -10, 10, (0, -10), (0, 10))
    for i in range(len(vertebres) - 2):
        add_joint(space, vertebres[i], vertebres[i + 1], -15, 15, (0, -10), (0, 10))  #angle limits de base
    add_joint(space, epaules, vertebres[0], -20, 20, (0, -10), (0, 10))

    raideur = 100
    amortissement = 0.5
    #### Muscles sternocléidomastoïdiens
    add_muscle(space, crane, epaules, 161.5, raideur, amortissement, (-60, 30), (0, 0))
    add_muscle(space, crane, epaules, 161.5, raideur, amortissement, (60, 30), (0, 0))

    ### muscles plenius
    add_muscle(space, crane, epaules, 159, raideur, amortissement, (-15, 21), (-15, 0))
    add_muscle(space, crane, epaules, 159, raideur, amortissement, (15, 21), (15, 0))

    add_muscle(space, crane, epaules, 160, raideur, amortissement, (-15, 21), (0, 0))
    add_muscle(space, crane, epaules, 160, raideur, amortissement, (15, 21), (0, 0))


    ### Muscles scalene gauche
    add_muscle(space,vertebres[5],epaules,122,raideur,amortissement,(-10,0),(-50,-5))
    add_muscle(space,vertebres[4],epaules,103,raideur,amortissement,(-10,0),(-50,-5))
    add_muscle(space,vertebres[3], epaules, 85, raideur, amortissement, (-10, 0), (-50, -5))
    add_muscle(space, vertebres[2], epaules, 68, raideur,  amortissement, (-10, 0), (-50, -5))
    add_muscle(space, vertebres[1], epaules, 53, raideur, amortissement, (-10, 0), (-50, -5))
    add_muscle(space, vertebres[0], epaules, 43, raideur, amortissement, (-10, 0), (-50, -5))
    #droite
    add_muscle(space, vertebres[5], epaules, 122, raideur, amortissement, (10, 0), (50, -5))
    add_muscle(space, vertebres[4], epaules, 103, raideur, amortissement, (10, 0), (50, -5))
    add_muscle(space, vertebres[3], epaules, 85, raideur, amortissement, (10, 0), (50, -5))
    add_muscle(space, vertebres[2], epaules, 68, raideur, amortissement, (10, 0), (50, -5))
    add_muscle(space, vertebres[1], epaules, 53, raideur, amortissement, (10, 0), (50, -5))
    add_muscle(space, vertebres[0], epaules, 43, raideur, amortissement, (10, 0), (50, -5))

    ### Muscles trapeze
    add_muscle(space,crane, epaules, 159, raideur, amortissement, (-10, 21), (-50, -5))
    add_muscle(space, crane, epaules, 159, raideur, amortissement, (10, 21), (50, -5))

    projectile = add_projectile(space, (190, 310))  #1 milieu
    #projectile = add_projectile(space, (210, 222))   #2 haut
    # projectile = add_projectile(space, (230, 400))  #3 bas
    launch_projectile(projectile, (190, 310), (1000, 0))
    data_log = []

    # vertebres = [add_vertebre(space, (300, 450 - i * 20)) for i in range(7)]
    # epaules = add_rectangle(space, (300, 470), (100, 20))
    # add_muscle(space, vertebres[4], epaules, 103, 500, 50, (-10, 0), (-50, -5))


    current_time = 0
    deltaT = 1 / 1000.0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        x = 1#((crane.position.x)-300)/1000
        y = 1#-((crane.position.y)-460)/1000
        norme = math.sqrt((x**2)+(y**2))

        data_log.append([current_time, x, y, norme])
        current_time += deltaT

        screen.fill((255, 255, 255))
        space.step(deltaT)
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(1000)

    #calcule de la vitesse de la norme ?
    data_log[0].append(0)
    for i in range(len(data_log)-1):
        data_log[i+1].append((data_log[i+1][3]-data_log[i][3])/(data_log[i+1][0]-data_log[i][0]))


    #calcule de l'acceleration
    data_log[0].append(0)
    data_log[1].append(0)
    for i in range(len(data_log) - 2):
        data_log[i + 2].append((data_log[i+2][4] - data_log[i + 1][4]) / (data_log[i+2][0] - data_log[i + 1][0]))


    # fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    # fig.suptitle('Graphiques de Mouvement')
    #
    # times = [row[0] for row in data_log]
    # normes = [row[3] for row in data_log]
    # vitesses = [row[4] for row in data_log]
    # accelerations = [row[5] for row in data_log]
    #
    # axs[0].plot(times, normes, label='Norme')
    # axs[0].set_title("Norme")
    # axs[0].set_xlabel('Temps (s)')
    # axs[0].set_ylabel('Norme')
    #
    # axs[1].plot(times, vitesses, label='Vitesse')
    # axs[1].set_title("Vitesse")
    # axs[1].set_xlabel('Temps (s)')
    # axs[1].set_ylabel('Vitesse')
    #
    # axs[2].plot(times, accelerations, label='Accélération')
    # axs[2].set_title("Accélération")
    # axs[2].set_xlabel('Temps (s)')
    # axs[2].set_ylabel('Accélération')
    # plt.show()

        # Sauvegarde des informations
    with open('head_movement_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time (s)', 'Position_X', 'Position_Y','norme','vitesse','acceleration'])
        writer.writerows(data_log)

    pygame.quit()

if __name__ == "__main__":
    main()

