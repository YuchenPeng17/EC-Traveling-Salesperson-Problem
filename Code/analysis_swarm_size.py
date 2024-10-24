1. How Variable Are the Runs for Different Swarm Sizes?
When using small swarm size, each run generates different best fitness and distance to global optimum. 
It is also obvious to see the fluctuation in the standard deviation and mean velocity diagrams. The results are inconsistent. 
However, for larger swarm size, results tend to be identical and consistent across four metrics. 

2. How many iterations are needed to converge approximately? Which swarm size converges faster? 
The following data represents the range of number of iterations required for the worst five runs out of ten for each swarm size to properly converge:
20 Swarm Size: (300, 500)
100 Swarm Size: (550,750)
200 Swarm Size: (700,850)
Larger swarm sizes require generally require more number of iterations to converge. 

3. Which swarm size gets closer to the global optimum?
By comparing “Distance of Swarm Center of Mass to Global Optimum” metric across 3 different swarm size, 
larger swarm size generally tends to generate a closer result to global minimum in 10 run. 

4. How might those differences be caused by the swarm size? Which swarm size would you choose? 
Smaller swarms is that they have fewer particles to explore the search space. With limited exploration, they are more likely to get stuck in different local optimum, 
result in a wider range of outcomes in different runs and leads to high variability. 
On the other hand, larger swarms benefit from wider search space and makes it less likely to get stuck, leading to more consistent results by finding the global optimum.
With regards to convergence, small swarm sizes tend to converge more quickly(require fewer iterations) compared with larger swarm sizes. 
This is typically because smaller swarms explore limited solution spaces, which can lead to faster convergence but they might stuck in local optimum. 
The greater exploration(more particles searching in wider regions simultaneously) gives a better chance to locate the global optimum 
but this extensive exploration also demands additional time (iterations). This also explains why results from larger swarm size gets closer to the global optimum.
