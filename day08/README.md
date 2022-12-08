Day 8: Treetop Tree House

```python
"""
input: 
    grid: List[List[int]]
return:
    part 1:
        number of visibles trees: int
    part 2:
        maximum scenic score: int
"""
```

# Parsing the Input
we will turn the input string into a grid $M$ of shape $(n, m)$, where $M[i][j] = x$ is the element in row $i$ and column $j$


# Part 1
in the first part we are asked to determine the number of visible trees from any edge of the grid $M$, you can review the definition of "visible" in the problem statement. Instead of considering all four edges, let's begin with figuring out the number visible trees from the left edge only.

for any tree at position $i, j$ to be visible from the left edge, all the trees in the same row $i$ has to be shorter than its height, so a brute force algorithm is to just to check if the previous condition is true, in code would be something like:

```python
def is_visible_from_left(i, j):
    return all([M[i][j] > M[i][pj] for pj in range(j)])

```

however, this would be too complex, a better approach would be just to compare $M[i][j]$ with a single value instead of $j's$

let $P(i, j)$ be the maximum height in the prefix $M[i][: j]$, in words, it is the maximum height of all trees in row $i$ before the current column $j$, then a tree would visible from the left edge if its height $M[i][j]$ is larger than $P(i, j)$, this approach is much faster since we could update $P(i, j)$ as we traverse the grid $M$ and it only takes constant time to perform.


for the next tree in the same row $(i, j + 1)$ the value of $P(i, j + 1)$ is equal to the current maximum $P(i, j)$ and the height of the tree at $i, j$

$$
P(i, j + 1) = max(P(i, j), M[i][j])
$$

our base case is $P(0, j)=-inf$ for any $j=0, ..., m-1$,  that is the case when we have not seen any trees.

let's create a matrix $V$ with the same shape as $M$, $V[i][j]$ will indicate that the tree at location $i, j$ is visible from the left edge, initially $V[i][j] = 0$ for every i, j pair.

```python
for i in (0, ..., n-1):
    for j in (0, ..., n-1):
        # if current tree is the new maximum, then it is visible
        V[i][j] = M[i][j] > P(i, j)
        # update the maximum for new tree in the sam row
        P(i, j + 1) = max(P(i, j), M[i][j])

```

the sum of all entries in $V$ is equal to the number of trees from the left edge.


nevertheless, we are asked to find the number of visible trees from any edge, not just from the left edge, to do so, we could either transform the matrix so that the algorithm above always works or change the algorithm to work with any direction (left, right, up, down), we will use the first solution.

the algorithm explained finds visible trees from the left, we could:
-  mirror the matrix $M$ so the right edge becomes the left edge
- tranpose the matrix $M$ so the top edge becomes the left edge
- tranpose and then mirror the matrix $M$ so that the bottom edge becomes the left edge



in python the transformations would look something like the following:
```python
mirror_grid = [row[::-1] for row in grid]
tranpose_grid = list(zip(*grid))
tranpose_mirror_grid = [row[::-1] for row in tranpose_grid]
```

for each transformation, we run the algorithm above and find the visibles trees from each edge, let $A$ be a matrix of the same shape as $M$, $A[i][j]$ indicates if the tree located at $i, j$ in the matrix $M$ is visible from any edge, then

$$
A[i][j] = OR(\{ V_{left}[i][j], \ V_{right}[i][m - j - 1], \ V_{top}[j][i], \ V_{bottom}[j][n - i - 1] \})
$$

- to access $i, j$ in the $V_{left}$, we just index at location $i, j$ since no transformation is applied. 
- the $j$ column in the $V_{right}$ is equal to $m-j-1$ since its flipped horizontally.
- $V_{top}$ is tranposed, so the $i, j$ are swaped to $j, i$
- $V_{bottom}$ is tranposed first, so the $i, j$ are swaped to $j, i$ as before but then is mirrored, so the column is now $n - i - 1$

the final answer will be the sum of all entries in $A$, which denotes the number of visible trees in the grid.


### Complexity
#### Visibles Trees from the left edge
the time complexity of this algorithm is O(nm) since we visit each tree only once and the space complexity is also O(nm) since we store for each tree wheter is visible or not. 

since we execute the algorithm above a constant number of times (4), the time and space complexity remains the same


# Part 2
to be continued...

<!-- as in part 2, we are asked to find the maximum scenic score in the grid $M$, you can review the definition of "scenic score" in the problem statement. as in part 1, we will focus first on the number of visible trees to the left.

for any tree at position $i, j$, we will look to the left and find the find first tree that is taller or the same height as the current tree, the number of visible trees is the number of trees in between the two.

the number of visible trees to the left is equal to the number of trees in row $i$ which are less than 



we will focus only on the scenic score from the left of each tree. -->