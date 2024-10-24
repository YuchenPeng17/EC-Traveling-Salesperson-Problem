We've chosen the following parameters for our particle swarm optimisation (PSO):

Swarm Size: We chose 200 particles because in a previous analysis (question 7) we found that having more particles allows for better exploration and 
improves the chances of finding the global optimum.

Topologies: Fully connected and ring. The choice is based on the results from question 9, where fully connected topology gives the lowest best fitness 
and ring topology is the standard choice in PSO.

Vmax: [2,12,20] Vmax of 2 performs well in our experiments, 12 is the standard choice, and we tried 20 to see the effect of higher velocity limits.

Adjust Velocity Option: There are two options for adjusting velocity: default and non-linear inertia weight adjustment.

Eventually, the combination we would choose is as follows:

- Swarm Size: 200 particles
- Topology: Fully Connected
- Vmax: 2
- Adjust Velocity Option: Non-linear inertia weight adjustment

Because this combination generated the best results with:

- Average Final Best Fitness: 5.4178883601707636e-15
- Minimum Best Fitness: 3.9968028886505635e-15
- Maximum Best Fitness: 7.549516567451064e-15

In regards to combinations where interactions worsen the performance, there are several observations:
When Vmax increases, the final results tend to get worse.
High Vmax can leads to more exploration but this increased exploration may lead to a loss of convergence because 
particles can go beyond optimal solutions potentially(overshoot).
In most cases, the ring topology outperformed the fully connected topology.
Although fully connected topology yields the best results, ring topology can be a more efficient and ideal choice in most of time.