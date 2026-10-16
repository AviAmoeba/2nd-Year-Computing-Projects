import random
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Defines the Box (The boundary values)
class Box:
    def __init__(self, x0, y0, x1, y1):
        # x0, y0: coordinates of bottom-left corner
        # x1, y1: coordinates of top-right corner
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


# Defines a Wall (A piston like object) It can move sinusoidally
class Wall:
    def __init__(self, x, u, A, w):
        self.x = x          # The current position of the wall
        self.u = u          # The current velocity of the wall
        self.A = A          # Amplitude of the sinusoidal motion
        self.w = w          # Angular frequency of the sinusoidal motion
    
    # Calculates the new position of the wall after time dt
    def move_wall_linear(self, dt):
        self.x += self.u * dt
    
    # Updates the sinusoidal velocity of the wall at time t
    def calc_sin_u(self, t):
        self.u = self.A * self.w * math.sin(self.w * t)

# Defines a mass
class Mass:
    def __init__(self, x, u, m):
        self.x = x          # The Current position of the Mass
        self.u = u          # The Current position of the Mass
        self.m = m          # The mass of the Mass
    
    def update(self, dt):
        self.x += self.u * dt       # Calculates the position of the mass after a time dt

    def collide_wall(self, u):
        self.u = (2*u) - self.u         # Calsulates the velocity of the particle after colliding the moving wall
    
    def transfer_momentum(self, other):         # Calculates the new velocity of a mass after collision using conservation of momentum and energy

        u1 = self.u
        u2 = other.u

        m1 = self.m
        m2 = other.m

        self.u = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
        other.u = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)


    def check_collide_left(self, x0, right_mass, wall):         # Only for the left most particle
        if self.u > 0 and self.x > right_mass.x:                # Checks if it passes the mass on the right
            self.transfer_momentum(right_mass)
        elif wall.u > self.u and self.x < wall.x:               # Checks if it passes the wall to its left
            self.collide_wall(wall.u)
    
    def check_collide_right(self, x1, left_mass):               # Only for the right most particle
        if self.u > 0 and self.x > x1:                          # Checks if it passes the mass on the left
            self.collide_wall(0)
        elif self.u < 0 and self.x < left_mass.x:               # Checks if it passes the wall to its right
            self.transfer_momentum(left_mass)
    
    def check_collide_middle(self, left_mass, right_mass):      # For all other masses
        if self.u > 0 and self.x > right_mass.x:                # Checks if it passes mass on its right
            self.transfer_momentum(right_mass)
        elif self.u < 0 and self.x < left_mass.x:               # Checks if it passes mass on its left
            self.transfer_momentum(left_mass)





box = Box(0, -0.5, 10, 0.5)

wall = Wall(0, 0, 2, 1)

# Makes an array with all the Mass objects, all are uniformly spread with a random speed between -10 and 10 and a random mass between 1 and 2
masses = [Mass(x, np.random.uniform(-10, 10), np.random.uniform(1, 2)) for x in range(1, 10)]


fig, (ax_sim, ax_plot) = plt.subplots(1, 2, figsize=(10, 4))
ax_sim.set_xlim(box.x0, box.x1)
ax_sim.set_ylim(box.y0, box.y1)

times = []
energies = []
energy_line, = ax_plot.plot([], [], 'b-')
ax_plot.set_xlim(0, 10)
ax_plot.set_ylim(0, 50)
ax_plot.set_xlabel("Time (units)")
ax_plot.set_ylabel("Kinetic Energy (units)")

colours = np.random.rand(len(masses), 3)

positions = np.array([[mass.x, 0] for mass in masses])
scat = ax_sim.scatter(positions[:,0], positions[:,1], s=50, color=colours)
wall_line, = ax_sim.plot([box.x0, box.x0], [box.y0, box.y1], 'r-', linewidth=3)         # 

def init():
    positions = np.array([[mass.x, 0] for mass in masses])
    scat.set_offsets(positions)
    wall_line.set_xdata([wall.x, wall.x])
    energy_line.set_data([], [])

    return scat, wall_line, energy_line

dt = 0.01
t = 0

def animate(i):
    global t
    t += dt

    wall.calc_sin_u(t)
    wall.move_wall_linear(dt)

    masses[0].update(dt)
    masses[0].check_collide_left(wall.x, masses[1], wall)

    for i in range(1, len(masses) - 1):
        masses[i].update(dt)
        masses[i].check_collide_middle(masses[i - 1], masses[i + 1])

    masses[-1].update(dt)
    masses[-1].check_collide_right(box.x1, masses[-2])

    positions = np.array([[mass.x, 0] for mass in masses])
    scat.set_offsets(positions)
    wall_line.set_xdata([wall.x, wall.x])    
    
    KE = sum(0.5 * m.m * m.u**2 for m in masses)

    times.append(t)
    energies.append(KE)

    energy_line.set_data(times, energies)
    ax_plot.set_xlim(0, max(10, t))
    ax_plot.set_ylim(0, max(energies) * 1.1)

    return scat, wall_line, energy_line

ani = FuncAnimation(
    fig, animate, frames=200, init_func=init, blit=True, interval=5
)

plt.show()