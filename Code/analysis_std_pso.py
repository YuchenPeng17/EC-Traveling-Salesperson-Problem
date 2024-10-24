1. How variable are the runs for different initialisations?
Observation: It shows considerable variability of the runs with different initialisations. 
Analysis: This variability may due to the randomness of the PSO algorithm. Different initialisations can impact the way that particles’ explorations of solution space. 
Besides, topological and parametric algorithms can affect the speed ad accuracy of convergence. For runs 2, 4, 5, 7, 9 and 10, the particles may be initialised closer to the 
global optimal, resulting in faster convergence and lower final fitness values.

2. How many iterations are needed to converge approximately?
Observation: Convergence occurs on different iteration counts, ranging from 614 to 907 iterations.
Analysis: Particles require different iteration times to effectively explore and utilise the solution space.  An optimal solution or better parameter settings can result 
in faster convergences. Slower convergent runs may take longer time to explore before converting to the global minimum.

3. Does the whole swarm converge towards the global optimum?
Observation: Most runs converge towards global optimality. 
Analysis: PSO encourages communication and information sharing between particles and promotes group-wide fusion. In most runs, shared early stopping points confirmed 
population convergence. However, delayed convergence in runs 1,3,6, and 8 may because of the particle get stuck on local optimal so it can’t escape and reach 
global optimal.

4. How close do the optimisations get?
Observation: In some better performing runs, fitness values can very close to 0, and slightly higher in some runs. 
Analysis: In the optimisation process, the speed converge to the global optimal depends on the position of the particle. Rapid convergence in some runs results in 
fitness values very close to 0, indicating very close to the optimal solution. Slower convergence runs have higher fitness values may because of particles converge to a 
local optimal before finding the global optimal.