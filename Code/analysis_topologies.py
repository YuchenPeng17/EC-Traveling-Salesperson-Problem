
# Topology                                v_max  Average Final Best Fit   Min Best Fitness     Max Best Fitness     Average Convergence  

# fully_connected_swarm                   10     1.828224439723924        0.0001077403497587   2.8143500407471618   863.7 iterations     

# random_neighbourhood_connectivity       10     0.1646223667354648       3.99680288865056e-15  1.646223633103109   915.4 iterations     

# ring_topology                           10     0.585084752961609        0.0198919461195115   1.6466195878067258   1000.0 iterations    

# star_topology                           10     2.5124241574631627       0.8673146243305223   4.360107190880495    1000.0 iterations    



1. Which connectivity performs best?
From our observations, 'random_neighbourhood_connectivity' always had the lowest average final score, at 0.165. By randomly picking neighbours for each particle, 
it likely creates a mix of local solutions, helping to find a better overall solution.

2. Which one leads to a wider swarm?
The 'fully_connected_swarm' showed big changes in scores, with the top score being 2.814 and the bottom one only 0.0001—a big gap of 2.814. 
Since all particles follow the best overall solution, which might be very different from where they are now, this can lead to many different choices across the swarm.

3. Which one converges faster?
'fully_connected_swarm' found the solution fastest, needing only 863.7 tries on average. 
This happens because every particle impacts the others, likely creating a teamwork-like setting, speeding up the search for the best answer.

4. Which one produces the closest result?
'random_neighbourhood_connectivity' offered the most accurate results, as it had the lowest average final best score. 
As mentioned earlier, this setup could be looking at many options. This means they might sometimes get answers that are very close to the perfect one.

5. Which one runs fastest and why?
'fully_connected_swarm' was the speediest, finishing in just 24.59 seconds. 
This might be because each particle always looks at the best answer up to that point. 
This could reduce the number of calculations needed each time, making the process faster.