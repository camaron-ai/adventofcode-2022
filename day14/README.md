# Day 14: Regolith Reservoir

I lost a lot of time trying to solve the problem efficiently, however, a brute-force approach is good enough!

# Part 1

We just simulate the game following the given rules, let $H$ be a hashSet storing the initial blocks, let the sand fall from position (500, 0) until it settles, and adds its final position in $H$ such that any sand can be placed there again, we keep playing until the sand falls beyond the deepest block.


# Part 2
for part 2, we add the bottom line to the hashSet $H$ and keep simulating until we have filled the entire space, this happens when all positions (500, 1), (499, 1), and (501, 1) have been taken:).


I am sure there is a clever way to solve this problem, I'll update the solution once I've found it.

