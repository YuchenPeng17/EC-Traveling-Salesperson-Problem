# Import Library
import math
import random
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings("ignore")

# Set random seeds for reproducibility
np.random.seed(0)
random.seed(0)

class Problem:
    def __init__(self, dimensions, bounds=None):
        self.dimensions = dimensions
        self.bounds = bounds
    def objective_function(self, x):
        raise NotImplementedError
    
# Define the Ackley Problem
class AckleyProblem(Problem):
    # Dimension fixed  at 10; Bounds fixed at +/- 30
    def __init__(self, dimensions, bounds=None):
        self.dimensions = dimensions
        self.bounds = bounds

    # x: Position of cuttent particle and it can have lots of dimension (x1, x2, ... xn)
    def objective_function(self, x):
        # ∑ xi^2
        sum1 = 0
        for xi in x:
            sum1 += xi ** 2

        # ∑ cos(2π * xi)
        sum2 = 0
        for xi in x:
            sum2 += math.cos(2 * math.pi * xi)

        # 20 · exp(-0.2 · sqrt(1/n) · sum1)
        term1 = 20 * math.exp(-0.2 * math.sqrt(max(0, sum1) / self.dimensions))

        # term1 = 20 * math.exp(-0.2 * math.sqrt(sum1 / self.dimensions))

        # exp · (1/n · sum2)
        term2 = math.exp(sum2 / self.dimensions)

        # f(x) = -20 · exp(-0.2 · sqrt(1/n) · sum1) - exp · (1/n · sum2) + 20 + e
        return - term1 - term2 + 20 + math.exp(1)

# Define Particle Class
class Particle:
    def __init__(self, dimensions, bounds, v_max, fitness_function):
        # current position(coordinates). E.g. 3-d [x, y, z] (dimension ∝ n)
        self.position = [] # current position(coordinates in each dimension). E.g. 3-d [x, y, z] (dimension ∝ n) 
        self.velocity = [] # velocity. E.g. 3-d [vx, vy, vz] (dimension ∝ n)

        self.position = np.random.uniform(-bounds, bounds, dimensions) # Assign random position when initialise a particle
        self.velocity = np.random.uniform(-v_max, v_max, dimensions)   # Assign random velocity
        self.pi = self.position.copy()  # personal best position        
        self.neighbours = []  # Store the neighbours of the particle

        # fitness of personal best position
        self.fitness = fitness_function(self.position)                 # fitness of current position

        self.pi_fitness = fitness_function(self.pi)
        self.fitness_function = fitness_function  # Store the fitness function / AckleyProblem Objective function

    # corresponds to equation (5) on 2.1.2
    # update particle's personal best if current fitness > its historical best fitness
    def evaluate_fitness(self):
        # fitness of current position
        self.fitness = self.fitness_function(self.position)
        if self.fitness < self.pi_fitness:
            self.pi_fitness = self.fitness
            self.pi = self.position.copy()

# Define PSO_Optimizer Class
class PSO_Optimizer:
    def __init__(self, num_particles, dimensions, bounds, v_max, fitness_function, topology):
        # initialize the population of particles
        self.particles = []
        self.dimensions = dimensions
        for _ in range(num_particles):
            particle = Particle(dimensions, bounds, v_max, fitness_function)
            self.particles.append(particle)

        # Initialize pg for each particle as its current position and pg_fitness
        self.pg = [particle.position.copy() for particle in self.particles]
        self.pg_fitness = [fitness_function(
            particle.position) for particle in self.particles]

        self.bounds = bounds
        self.v_max = v_max
        self.fitness_function = fitness_function

        # store the selected topology
        self.topology = topology
        # update neighbours for each particle based on the star topology
        if topology == "star_topology":
            # randomly select a particle as the center particle
            self.index_of_star_particle = random.randint(0, len(self.particles) - 1)
            
        elif topology == "random_neighbourhood_connectivity":
            num_of_neighbours = len(self.particles)//2
            for particle in self.particles:
                # for each particle, random select half of the particles as its neighbours
                neighbour_particles = random.sample(self.particles, num_of_neighbours)
                # # remove itself from the neighbours
                # neighbour_particles.remove(particle)                
                particle.neighbours = neighbour_particles

        # ! record history
        # (5.4 first subplot)
        self.best_fitness_history = []
        # (5.4 Second subplot)
        self.center_of_mass_distances = []
        # (5.4 Third subplot)
        self.std_dev_positions = []
        # (5.4 Fourth subplot)
        self.mean_velocity_lengths = []

        # Question8Update: SETTING UP WEIGHT MIN AND WEIGHT MAX, SETTING UP CURRENT ITERATION
        self.weight_min =  -0.16199           # minimum weight
        self.weight_max = 0.78540            # maximum weight
        self.weight_list = []           # track how weight changes

    # Update velocity and position
    # Question8Update: THREE MORE PARAMETER TO CHOOSE THE METHODS FOR UPDATING VELOCITY AND POSITION
    def update_velocity_and_position(self, option, current_iteration, n = 1.2, c1=2.05, c2=2.05):
        #Question 8 Updated: if option = 1, original way of updating velocity
        #                    if option = 2, introducing non-linear inertia weight adjustment
        #                    n : nonlinear modulation index 0.6(bowl), 1.4(hat)
        # based on the chosen topology, update the 'pg' for each particle
        if self.topology == "fully_connected_swarm":
            self.fully_connected_swarm()
        elif self.topology == "ring_topology":
            self.ring_topology()
        elif self.topology == "star_topology":
            self.star_topology()
        elif self.topology == "random_neighbourhood_connectivity":
            self.random_neighbourhood_connectivity()
        if option == 2:
            
            # calculating for weight
            max_iteration = 1000 
            weight_term1 = ((max_iteration - current_iteration-1)**n) / (max_iteration**n)
            weight_term2 = self.weight_max - self.weight_min
            weight = weight_term1 * weight_term2 + self.weight_min
            self.weight_list.append(weight)

        for index, particle in enumerate(self.particles):
            p1 = np.random.uniform(0, 1)
            p2 = np.random.uniform(0, 1)
            # use the pg corresponding to the particle
            local_pg = self.pg[index]
            if option == 1 : 
                personal_attraction = c1 * p1 * (particle.pi - particle.position)
                social_attraction = c2 * p2 * (local_pg - particle.position)
                particle.velocity =0.72984*( particle.velocity + personal_attraction + social_attraction)
            
            elif option == 2:
                # calculating for weight  
                c1 = 2
                c2 = 2              
                term1 = p1 *c1 * (particle.pi - particle.position)
                term2 = p2 *c2 * (local_pg - particle.position)
                particle.velocity = weight*particle.velocity + term1 + term2

            # ensure velocity is within bounds
            particle.velocity = np.clip(
                particle.velocity, -self.v_max, self.v_max)

            # update position
            # x_i(t) = x_i(t-1) + v_i(t)
            particle.position = particle.position + particle.velocity
            # ensure position is within bounds
            particle.position = np.clip(
                particle.position, -self.bounds, self.bounds)
            # calculate fitness
            particle.evaluate_fitness()
        # update fitness history
        self.get_best_fitness()
        self.get_distance_to_optimum()
        self.get_position_standard_deviation()
        self.get_mean_velocity_length()

    # 5.3 topology
    def fully_connected_swarm(self):
        # Initialize with a large fitness value as a reference, ensuring it's larger than any potential fitness value
        best_swarm_fitness = float('inf')
        best_swarm_position = None

        # Iterate through each particle to find the one with the smallest fitness value
        for particle in self.particles:
            current_fitness = particle.fitness
            if current_fitness < best_swarm_fitness:
                best_swarm_position = particle.position.copy()
                best_swarm_fitness = current_fitness

        # Update each particle's pg and pg_fitness with the found best position and fitness value
        for i in range(len(self.pg)):
            self.pg[i] = best_swarm_position
            self.pg_fitness[i] = best_swarm_fitness

    def star_topology(self):
        # 1. initialize the center particle
        centre_particle = self.particles[self.index_of_star_particle]
        
        # 2. center particle's speed and position are updated based on its own historical best position and the current global best position
        for index, particle in enumerate(self.particles):
            
            # check if the current particle is the center particle
            if particle is centre_particle:
                
                # then find the optimal position and fitness in the group
                best_swarm_fitness = float('inf')
                best_swarm_position = None
                for p in self.particles:
                    if p.fitness < best_swarm_fitness:
                        best_swarm_position = p.position.copy()
                        best_swarm_fitness = p.fitness
                
                # update the center particle's pg and pg_fitness
                self.pg[index] = best_swarm_position
                self.pg_fitness[index] = best_swarm_fitness
                continue  # keep moving

            # 3. about non-center particles just update their pg and pg_fitness to the center particle's current position and fitness
            self.pg[index] = centre_particle.position.copy()
            self.pg_fitness[index] = self.fitness_function(centre_particle.position)

    def ring_topology(self):
        # use ring topology to update each particle
        for index, particle in enumerate(self.particles):
            # get the previous and next particle
            if index == 0:
                previous_particle = self.particles[len(self.particles) - 1]
            else:
                previous_particle = self.particles[index - 1]
            if index == len(self.particles) - 1:
                next_particle = self.particles[0]
            else:
                next_particle = self.particles[index + 1]
            

            # find the best fitness between the previous, current and next particle
            best_fitness = float('inf')
            best_particle = None
            for current_particle in [previous_particle, particle, next_particle]:
                current_fitness = self.fitness_function(current_particle.position)
                if current_fitness < best_fitness:
                    best_fitness = current_fitness
                    best_particle = current_particle

            # update the pg and pg_fitness
            self.pg[index] = best_particle.position.copy()
            self.pg_fitness[index] = best_particle.fitness

    def random_neighbourhood_connectivity(self, percentage=0.5):
        # percentage : how many percent particles become neighbours, by default is 0.5
        # use random topology to update each particle
        for index, particle in enumerate(self.particles):
            # if first time run / no neighbours found for current particle : generate fixed neighbours
            if not particle.neighbours:
                num_of_neighbours = len(self.particles) * percentage
                remaining_particles = [p for p in self.particles if p != particle]
                particle.neighbours = random.sample(remaining_particles, num_of_neighbours)

            # find the best fitness in between neighbours
            best_fitness = float('inf')
            best_particle = None
            for current_particle in particle.neighbours:
                current_fitness = current_particle.fitness
                if current_fitness < best_fitness:
                    best_fitness = current_fitness
                    best_particle = current_particle

            # update pg and pg fitness
            self.pg[index] = best_particle.position.copy()
            self.pg_fitness[index] = best_particle.fitness

    # 5.4
    def get_best_fitness(self):
        """
        return a list representing the best fitness value at each iteration.
        [f_0, f_1, ..., f_N-1],
        where f_i is the best fitness value at the i-th iteration.
        """
        current_best_fitness = float('inf')
        for particle in self.particles:
            if particle.fitness < current_best_fitness:
                current_best_fitness = particle.fitness

        self.best_fitness_history.append(current_best_fitness)

        return self.best_fitness_history

    def get_distance_to_optimum(self):
        """
        return a list representing the distance from the swarm centroid to the global optimum at each iteration.
        [d_0, d_1, ..., d_N-1],
        where d_i is the distance at the i-th iteration.
        """
        # define global optimum coordinates
        global_optimum = [0] * self.dimensions

        # calculate centre of mass, mean positions
        centre_of_mass = [0] * self.dimensions
        for particle in self.particles:
            for i in range(self.dimensions):
                centre_of_mass[i] = centre_of_mass[i] + particle.position[i]
        for i in range(self.dimensions):
            centre_of_mass[i] = centre_of_mass[i] / len(self.particles)

        # calculate the Euclidean distance between the centre of mass and the global optimum
        distance = 0
        for i in range(self.dimensions):
            distance = distance + (centre_of_mass[i] - global_optimum[i])**2
        
        distance = max(0, distance) # to prevent negative numbers
        distance = math.sqrt(abs(distance))

        self.center_of_mass_distances.append(distance)
        return self.center_of_mass_distances

    def get_position_standard_deviation(self):
        """
        return a list representing the standard deviation of particle positions relative to the centroid at each iteration.
        [sd_0, sd_1, ..., sd_N-1],
        where sd_i is the standard deviation at the i-th iteration.
        """
        # get positions of particles and compute the squared deviation
        positions = np.array([particle.position for particle in self.particles])
        centroid = np.mean(positions, axis = 0)
        deviations = positions - centroid
        squared_deviations = deviations**2
        
        # compute and store the standard deviation of particle positions from the mean squared deviation
        mean_squared_deviation = np.mean(squared_deviations)
        scalar_std_deviation = np.sqrt(mean_squared_deviation)
        self.std_dev_positions.append(scalar_std_deviation)
        
        return self.std_dev_positions

    def get_mean_velocity_length(self):
        """
        return a list representing the average length of the velocity vectors of particles at each iteration.
        [v_0, v_1, ..., v_N-1],
        where v_i is the average velocity length at the i-th iteration.
        """
        total_velocity_length = 0
        for particle in self.particles:
            # calculate the length (magnitude) of the velocity vector
            velocity_length = np.linalg.norm(particle.velocity)  #  we use L2 norm
            total_velocity_length += velocity_length

        # calculate the mean velocity length for all particles
        mean_velocity_length = total_velocity_length / len(self.particles)
        self.mean_velocity_lengths.append(mean_velocity_length)
        return self.mean_velocity_lengths

def plot_figures(metrics, color, run_number): 
    # Subplot 1: Current best fitness value over iterations
    plt.subplot(2, 2, 1)
    line, = plt.plot(metrics["best_fitness_history"], color=color, label=f"Run {run_number}") 
    min_idx1 = np.argmin(metrics["best_fitness_history"])
    min_val1 = metrics["best_fitness_history"][min_idx1]
    plt.title('Current Best Fitness Over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Best Fitness')
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)

    # Subplot 2: Distance of swarm center of mass to the global optimum
    plt.subplot(2, 2, 2)
    plt.plot(metrics["center_of_mass_distances"], color=color, label=f"Run {run_number}") 
    min_idx2 = np.argmin(metrics["center_of_mass_distances"])
    min_val2 = metrics["center_of_mass_distances"][min_idx2]
    plt.title('Distance of Swarm Center of Mass to Global Optimum')
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)

    # Subplot 3: Standard deviation of particle positions around the center of mass
    plt.subplot(2, 2, 3)
    plt.plot(metrics["std_dev_positions"], color=color, label=f"Run {run_number}") 
    min_idx3 = np.argmin(metrics["std_dev_positions"])
    min_val3 = metrics["std_dev_positions"][min_idx3]
    plt.title('Standard Deviation of Particle Positions')
    plt.xlabel('Iteration')
    plt.ylabel('Standard Deviation')
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)

    # Subplot 4: Mean length of the velocity vectors
    plt.subplot(2, 2, 4)
    plt.plot(metrics["mean_velocity_lengths"], color=color, label=f"Run {run_number}") 
    min_idx4 = np.argmin(metrics["mean_velocity_lengths"])
    plt.title('Mean Length of Velocity Vectors')
    plt.xlabel('Iteration')
    plt.ylabel('Mean Velocity')
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)

    return line

# number_of_particles, dimension, bounds_in_each_dimension, bounds_in_velocity, topology_chosen, early_stopping_condition
# Question8Update: TWO MORE PARAMETER TO CHOOSE THE METHODS FOR UPDATING VELOCITY AND POSITION & NONLINEAR MUDULATION INDEX N
def run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, topology, update_VandP_option, early_stopping_rounds=100):
    # 1. create the problem instance and PSO optimizer
    ackley_problem = AckleyProblem(dimensions, bounds)
    pso_optimizer = PSO_Optimizer(
        num_particles, dimensions, bounds, v_max, ackley_problem.objective_function, topology)

    # initialize early stopping variables
    stagnant_rounds = 0
    best_so_far = float('inf')

    for iteration in range(max_iterations):
        # 2. update velocity and position of each particle
        pso_optimizer.update_velocity_and_position(option=update_VandP_option, current_iteration=iteration)

        # 3. evaluate the fitness of each particle
        # for particle in pso_optimizer.particles:
        #     particle.evaluate_fitness()

        # 4. get the best fitness in the current iteration and check for early stopping
        best_swarm_fitness = min(pso_optimizer.pg_fitness)
        if best_swarm_fitness < best_so_far:
            best_so_far = best_swarm_fitness
            stagnant_rounds = 0
        else:
            stagnant_rounds += 1
        if stagnant_rounds >= early_stopping_rounds:
            print(f"Early stopping at iteration {iteration + 1} due to no improvement after {stagnant_rounds} iterations.")
            break

    # 5. collect metrics after the execution of optimizer
    metrics = {
        "best_fitness_history": pso_optimizer.best_fitness_history,
        "center_of_mass_distances": pso_optimizer.center_of_mass_distances,
        "std_dev_positions": pso_optimizer.std_dev_positions,
        "mean_velocity_lengths": pso_optimizer.mean_velocity_lengths
    }
    
    return metrics  # return the collected metrics for after plotting

def general_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology, save_path, update_VandP_option = 1):
    # 0. bulid a set of lighter colors for distinguish each other when overlapped
    colors = [
        (1, 0, 0, 0.5), (0, 1, 0, 0.5), (0, 0, 1, 0.5), 
        (1, 1, 0, 0.5), (0.5, 0, 0.5, 0.5), (1, 0.5, 0, 0.5), 
        (0, 1, 1, 0.5), (1, 0, 1, 0.5), (0.6, 0.3, 0, 0.5), (0, 0.5, 0, 0.5)
    ]

    # 1. create a figure for plotting
    plt.figure(figsize=(15, 10)) 
    lines = [] # store the line objects Eg. color of line, type...
    labels = [] # store the text labels that describe each line

    # 2. run the PSO optimizer and plot each result with a different color
    for i, color in enumerate(colors):
        metrics = run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, topology, update_VandP_option)
        print(f"Run {i+1}: Global Best Fitness = {min(metrics['best_fitness_history'])}") 
        
        # plot the metrics and store the line and label information for the legend
        line = plot_figures(metrics, color, i+1)  
        lines.append(line)
        labels.append(f"Run {i+1}")

    # 3. check if the 'results' directory exists, if not, create a new one
    if not os.path.exists('results'):
        os.makedirs('results')

    # 4. add legends to each subplot with a fixed position and font size
    for i in range(1, 5):
        plt.subplot(2, 2, i)
        plt.legend(lines, labels, loc='upper right', prop={'size': 8})

    # 5. adjust layout and save it to the specified path
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def Q6_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology):
    save_path = "results/metrics_std_pso.png"
    general_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology, save_path)

def Q7_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology):
    save_path = f"results/metrics_std_pso_swarm{num_particles}.png"
    general_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology, save_path)

def Q8_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology):
    save_path = "results/metrics_std_pso_weight_adjust.png"
    update_VandP_option = 2 
    general_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology, save_path, update_VandP_option)

def Q9_plot(num_particles, dimensions, bounds, v_max, max_iterations, topologies):
    for topology in topologies:
        save_path = f"results/metrics_std_pso_topo_{topology}.png"
        print(f"Topology: {topology}")
        general_plot(num_particles, dimensions, bounds, v_max, max_iterations, topology, save_path)
        
def test_combination(num_particles, dimensions, bounds, v_max, max_iterations, option, topology, filepath):
    # results = [] # used to store the complete results of multiple combinations of option, topology, v_max
    run_results = [] # used to store the results of each individual (dictionary) E.g. run:1, final best fitness:xxx, convergence_speed:xxx...
    best_fitnesses = [] # used to store the best fitness value obtained in each individual run E.g [best_of_run1, best_of_run2, ...]

    # check the entered path if it's not exist just create a new one
    dir_path = os.path.dirname(filepath)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    print(f"Testing combination: option = {option}, topology = {topology}, v_max = {v_max}")

    # 1. open the file with the entered filepath and write our selected parameters at begining of the file
    with open(filepath, "w") as file:
        file.write(f"Option: {option}\n")
        file.write(f"Topology: {topology}\n")
        file.write(f"v_max: {v_max}\n")

        # 2. execute 10 runs same as before
        for run in range(10):
            metrics = run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, topology, option)

            # 2.1 get the best fitness among all iterations each run
            final_best_fitness = min(metrics['best_fitness_history'])
            best_fitnesses.append(final_best_fitness)
            # 2.2 store the results of each individual run in to dictionary 
            run_results.append({
                'run': run + 1,
                'final_best_fitness': final_best_fitness,
                'convergence_speed': len(metrics['best_fitness_history']),
                'best_fitness_history': metrics['best_fitness_history']  # Add the entire fitness history for each run
            })
            # 2.3 write the metrics of each run, run number, final best fitness...
            file.write(f"Run {run + 1}:\n")
            file.write(f"Final Best Fitness: {final_best_fitness}\n")
            file.write(f"Convergence Speed: {len(metrics['best_fitness_history'])} iterations\n")

        # 3. calculate and write some metrics from all runs that helps in observing performance of each algorithm
        average_fitness = np.mean(best_fitnesses)
        file.write(f"\nAverage Final Best Fitness: {average_fitness}\n")
        
        min_best_fitness = np.min(best_fitnesses) 
        file.write(f"Minimum Best Fitness: {min_best_fitness}\n")
        
        max_best_fitness = np.max(best_fitnesses) 
        file.write(f"Maximum Best Fitness: {max_best_fitness}\n")
        
        average_convergence_speed = np.mean([len(run_result['best_fitness_history']) for run_result in run_results])
        file.write(f"Average Convergence Speed: {average_convergence_speed} iterations\n")

def main():
    # Option For Swarm size 20, 100, and 200 given by Assignment Description
    swarm_sizes = [20, 100, 200]
    std_swarm_size = 50         # standard PSO swarm size is defined as 50
    std_swarm_topology = "ring_topology" # standard PSO topology is defined as ring topology
    dimensions = 10             # This Dimension is Fixed at 10 Given By Assignment Description
    # This +/- 30 Bounds is Fixed at 30 Given By Assignment Description
    bounds = 30
    v_max = 10                  # This v_max gives bounds to particle.velocity
    max_iterations = 1000      # "Use 1000 iterations and an early stopping criterion."

   # run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, 'fully_connected_swarm')
    # print("---------------------------------- TEST fully connected swarm END----------------------------------")

    # run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, 'ring_topology')
    # run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, 'star_topology', 1)
    # print("---------------------------------- TEST star topology END----------------------------------")

    # # Testing Objective 3 : ...
    # run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, 'random_neighbourhood_connectivity')
    # print("----------------------------------TEST random topology & Plot2 END----------------------------------")

    # # Testing Objective 4 : run_pso_optimizer TWO MORE PARAMETER TO CHOOSE THE METHODS FOR UPDATING VELOCITY AND POSITION & NONLINEAR MUDULATION INDEX N
    # run_pso_optimizer(num_particles, dimensions, bounds, v_max, max_iterations, 'fully_connected_swarm', 2)
    # print("----------------------------------TEST4 END----------------------------------")
    
    #################### Q6 plot #####################
    # Q6_plot(std_swarm_size, dimensions, bounds, v_max, max_iterations, std_swarm_topology)
    
    # #################### Q7 plot #####################
    # for swarm_size in swarm_sizes:
    #     print(f"Running PSO with swarm size {swarm_size}")
    #     Q7_plot(swarm_size, dimensions, bounds, v_max, max_iterations, std_swarm_topology)
    
    # ##################### Q8 plot #####################
    # Q8_plot(std_swarm_size, dimensions, bounds, v_max, max_iterations, std_swarm_topology)
    # topologies_q8 = ['ring_topology']
    # swarm_size_q8 = 50
    # v_max_q8 = [10]
    # option_q8 = [1] 
    
    # for vmax in v_max_q8:
    #     for option in option_q8:
    #         for topology in topologies_q8:
    #             start_time = time.time()
                
    #             filename = f"results/metrics_{topology}_q8.py"
    #             results = test_combination(swarm_size_q8, dimensions, bounds, vmax, max_iterations, option, topology, filename)
    #             end_time = time.time()
    #             elapsed_time = end_time - start_time
                
    #             print(f"The topology {topology} took {elapsed_time:.2f} seconds to run.")
    
    # #################### Q9 plot #####################
    # topologies = ['fully_connected_swarm', 'ring_topology', 'star_topology', 'random_neighbourhood_connectivity']
    # topologies = ['star_topology']
    # Q9_plot(std_swarm_size, dimensions, bounds, v_max, max_iterations, topologies)
    # swarm_size_q9 = 50
    # v_max_q9 = [10]
    # option_q9 = [1] 
    # topologies_q9 = ['fully_connected_swarm', 'ring_topology', 'star_topology', 'random_neighbourhood_connectivity'] 

    # for vmax in v_max_q9:
    #     for option in option_q9:
    #         for topology in topologies_q9:
    #             start_time = time.time()
                
    #             filename = f"results/metrics_{topology}_q9.py"
    #             results = test_combination(
    #                 swarm_size_q9, dimensions, bounds, vmax, max_iterations, option, topology, filename
    #             )
                
    #             end_time = time.time()
    #             elapsed_time = end_time - start_time
                
    #             print(f"The topology {topology} took {elapsed_time:.2f} seconds to run.")
    
    ##################### Q10 plot ####################
    # swarm_size_q10 = 200
    # v_max_q10 = [12]
    # option_q10 = [1, 2] 
    # topologies_q10 = ['fully_connected_swarm', 'ring_topology'] 

    # for vmax in v_max_q10:
    #     for option in option_q10:
    #         for topology in topologies_q10:
    #             filename = f"results/metrics_comb_o{option}_{topology}_vmax{vmax}.py"
    #             results = test_combination(swarm_size_q10, dimensions, bounds, vmax, max_iterations, option, topology, filename)

if __name__ == "__main__":
    main()