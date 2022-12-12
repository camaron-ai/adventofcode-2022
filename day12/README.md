# Day 12: Hill Climbing Algorithm

## Parsing the input
we will turn the input string into a grid of numbers, where the characters ```a, b, ..., z``` will be mapped to ```0, 1, ..., 26```, let $M$ be this new matrix, also, we will find the coordinates of the current position $s_i, s_j$ and the coordinates of the position we should get $e_i, e_j$.


let $n, m$ be the number of rows and columns in the matrix $M$

# Part 1
we can think of this problem as a graph where the vertices are all the coordinates within the grid

$$
V = \{\text{$(i, j)$ for i in (0, .., n-1) for j in (0, ..., m-1)} \}
$$

there is a direct edge between two adjacent coordinates $v=(i, j)$ and $w=(i', j')$ if the elevation of coordinate $w$ is less or at most one unit higher than the elevation at coordinate $v$, so we can define outgoing neighbor set as:

$$
adj^+(i, j) = \{\text{(i', j') for i', j' in neighbors(i, j) if $M[i'][j'] - M[i][j] \le 1$} \}
$$

now that we have our graph $G(V, E)$, we can run breadth first search to find the shortest distance from the start position $(s_i, s_j)$ to the goal position $(e_i, e_j)$


### Complexity
in the worse case, the total number of edges is four times (4 directions) the number of vertices $|E| = |V| * 4$, since the number of vertices is equal to $m*n$, the time complexity and space complexity are $O(n*m)$



# Part 2
for part 2, we have to find the shortest path from any position with elevation ```a``` to the goal position $(e_i, e_j)$, to do so, we will run BFS again but instead of starting at a single position $(s_i, s_j)$, we will start at every vertex such that elevation is equal to ```a```, therefore, if we reach the goal position it must be from a valid path that started at the lowest elevation.

this is the same as creating a super vertex $S$, which has only direct edges from $S$ to every vertex $v$ such elevation is ```a```, every path from $S$ to the goal position must look as:

$$
(S, v_a, ..., T)
$$

where $T$ is the final position and $v_a$ is a vertex with the lowest elevation, so running BFS starting at $S$ will find the shortest path possible to the goal destination with the right conditions.


### Complexity
the time and space complexity is the same as in part 1.