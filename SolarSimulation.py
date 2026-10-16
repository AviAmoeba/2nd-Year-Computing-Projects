import numpy as np
import matplotlib.pyplot as plt

class Star:
    def __init__(self, Star_Mass, G_Constant, del_t):       # Defines all initial values of the Star
        self.M = Star_Mass       # defines Mass of the Star
        self.G = G_Constant     # Defines the Gravitational Constant
        self.dt = del_t     # defines dt
    
    def find_force(self, planet):       # A function to find the force between the sun and planet

        length = (planet.x[0]**2 + planet.x[1]**2)**1.5
        A = self.M * planet.m * self.G
        const = A/length

        f = - const * planet.x
        return f


class Planet:
    def __init__(self, Planet_Mass, x_initial, v_initial):      # Defines all the initial values of the Planet
        self.m = Planet_Mass                                    # Defines Mass of the planet
        self.x = np.array(x_initial, dtype=float)               # Defines initial position
        self.v = np.array(v_initial, dtype=float)               # Defines initial velocity


class Simulation:
    def __init__(self, system, planet, method):                 # Initialises all values of the simulation
        self.system = system
        self.planet = Planet(planet.m, planet.x.copy(), planet.v.copy())
        self.method = method
        self.positions = []
        self.velocities = []
        self.times = []
        self.t = 0
    
    def update(self):
        if self.method == "Euler":                                      # if method used is Euler
            dt = self.system.dt             
            self.planet.x += self.planet.v * dt                         # x = dt * v
            force = self.system.find_force(self.planet)                 # finds force
            self.planet.v += (1 / self.planet.m) * force * dt           # v = dt * (1/m)f
            self.t += dt

        elif self.method == "LeapFrog":                                     # if method is LeapFrog
            dt = self.system.dt * 0.5
            self.planet.x += self.planet.v * dt                             
            self.t += dt
            force = self.system.find_force(self.planet)
            self.planet.v += (1 / self.planet.m) * force * (2 * dt)
            self.planet.x += self.planet.v * dt
            self.t += dt
        
        self.positions.append(self.planet.x.copy())                                # Adds the current position of the planet into an array which contains all positions in time order
        self.velocities.append(self.planet.v.copy())                                # Same as positions but for velocity
        self.times.append(len(self.times) * dt)                                     # Updates time
        
    def run(self, N):                                                               # Loops the method N times
        for i in range(N):
            self.update()
        return np.array(self.positions), np.array(self.velocities), np.array(self.times)                # Returns the position, velocity and time arrays

class Properties:                                                                   # This class finds properties such as Energy and Momentum
    def __init__(self, system, planet, positions, velocities):
        self.system = system
        self.m = planet.m
        self.positions = positions
        self.velocities = velocities
    
    def Energy(self):
        pos = np.sqrt((self.positions[:,0]**2 + self.positions[:,1]**2))
        vel = np.sqrt((self.velocities[:,0]**2 + self.velocities[:,1]**2))
        KE = 0.5 * self.m * (vel**2)
        A = (self.m) * (self.system.M) * (self.system.G)
        PE = - A/pos
        E = KE + PE
        return KE, PE, E
    
    def Momentum(self):
        print()


# dictionary in the form dict = {"Curve1": (A, B), "Curve2": (C,D)}
def plot_graph(dictionary, x_axis, y_axis, title):              # Plots multiple trajectories on the same graph
    for label, (x, y) in dictionary.items():                    # Loops throught the dictionary plotting all trajectories
        plt.plot(x, y, label=label)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.legend()
    plt.title(title)
    plt.grid()
    plt.axis("equal")
    plt.show()



# Main program

System = Star(10, 1, 0.01)
N = 200000

# Differing the direction of the initial velocities

Rock = Planet(1, [100., 70.], [0.1, -0.1])
solver = Simulation(System, Rock, method="Euler")

X1, V1, T1 = solver.run(N)


Rock = Planet(1, [100., 70.], [-0.0811, 0.1175])
solver = Simulation(System, Rock, method="Euler")

X2, V2, T2 = solver.run(N)

Rock = Planet(1, [100., 70.], [0.135, -0.046])
solver = Simulation(System, Rock, method="Euler")

X3, V3, T3 = solver.run(N)

Dict = {
    "vel = [0.1, -0.1]": (X1[:,0], X1[:,1]), 
    "vel = [-0.0811, 0.1175]": (X2[:,0], X2[:,1]),
    "vel = [0.135, -0.046]": (X3[:,0], X3[:,1])
        }

plot_graph(Dict, "x", "y", "Different Direction of Initial Velocities")




# Second Differing Magnitude of Velocities

System = Star(10, 1, 0.01)
N = 200000

Rock = Planet(1, [100., 70.], [0.1, -0.1])
solver = Simulation(System, Rock, method="Euler")

X1, V1, T1 = solver.run(N)


Rock = Planet(1, [100., 70.], [0.2, -0.2])
solver = Simulation(System, Rock, method="Euler")

X2, V2, T2 = solver.run(N)

Rock = Planet(1, [100., 70.], [0.05, -0.05])
solver = Simulation(System, Rock, method="Euler")

X3, V3, T3 = solver.run(N)

Dict = {
    "vel = [0.1, -0.1]": (X1[:,0], X1[:,1]), 
    "vel = [0.05, -0.05]": (X2[:,0], X2[:,1]),
    "vel = [0.2, -0.2]": (X3[:,0], X3[:,1])
        }

plot_graph(Dict, "x", "y", "Different Magnitudes of Initial Velocities")



