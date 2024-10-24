Our PSO library is designed by the following object-oriented principles, and contain several modular components. We aim to ensure this libaray is 
modular and extensible. To achieve this, we focus on serveral key components: "OptimizationProblem", "Particle" and "Swarm", we breaked them into
several classes which are showing as below:
1. AckleyProblem class:
We built this class to implement Optimization Problem. We decided to use dimensions and bounds as attributes, and use an objective function to evaluate 
the particle's fitness. By doing this, dimensions and bounds are allowed to vary, which is convinent for following research.
2. Particle class:
To represent a particle, we focus on serveral attributes: position of the particle, velocity of the particle, personal best position and personal best 
fitness. Besides, we will use a function to evaluate the fitness of the particle and updates personal best if necessary.
3. PSO_Optimizer class:
In this class, we will focus on initialise particles and implement four topologies. Besides, we need to update particle velocities and positions based
on PSO equations. In order to update global best position, we provide topology methods to choose. For data collection, we will design calculation methods.
Based on demands, we set early stopping mechanism. For better monitoring the optimization process, visualization is essensial, so we will implement
function to plot figures.
This architecture allows users to easily extend the libaray bt customizing an existing optimization problems, and can experiment different topologies.