1.  We choose to use the nonlinear inertia weight adjust function suggest by Chatterjee and Siarry.
    the inertia weight w is calculated as follows:
    w = ((max_iter - iter) / max_iter)^n * (w_max-w_min) + w_min
    where w_max = 0.78540 and w_min = -0.16199 and n=1.2 which was suggested in the paper.
    n = 1.2 can make the inertia weight decrease slower at the beginning iterations and decrease faster at the later iterations.
    Other settings are same as the standard PSO algorithm.

2.  The result shows that after 1000 iterations, the fitness can converge to 0.01~0.17.
    The distance of swarm center to the global best position drops dramatically at the beginning iterations and then slows down after 300 iterations.
    The graph of standard deviation of particle positions and the mean length of velocity vector shows similar trend.
    They also shows a increment at the very end of the iterations. Which is caused by the minimum inertia weight is set to -0.16199.

3.  Compare with the standard PSO algorithm, the inertia weight adjust PSO algorithm has a better performance.
    The standard PSO landed was more likely to be trapped in local optimum while the inertia weight adjust PSO algorithm can avoid this situation.
    This is because the inertia weight adjust PSO algorithm can make the particles move faster at the beginning iterations to aggressively explore the area.
    And then the inertia weight adjust PSO algorithm can make the particles move slower at the later iterations to exploit the area.
    This can help the inertia weight adjust PSO algorithm to avoid the local optimum
    
    Compare with the standard PSO with swarm size experiments, the inertia weight adjust PSO has a similar performance with the swarm size 100.
    They both result under 2. and despite the increment at the end of inertia weight adjust PSO, the graph looks similar.

4. In conclusion, the inertia weight adjust PSO algorithm has a better performance.
	
