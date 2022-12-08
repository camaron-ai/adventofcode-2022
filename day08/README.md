Day 8: Treetop Tree House

```python
"""
input: 
    grid: List[List[int]]
return:
    part 1:
        number of visible trees: int
    part 2:
        maximum scenic score: int
"""
```

# Parsing the Input
we will turn the input string into a grid $M$ of shape $(n, m)$, where $M[i][j] = x$ is the element in row $i$ and column $j$


# Part 1
in the first part, we are asked to determine the number of visible trees from any edge of the grid $M$, you can review the definition of "visible" in the problem statement. Instead of considering all four edges, let's begin with figuring out the number of visible trees from the left edge only.

for any tree at position $i, j$ to be visible from the left edge, all the trees in the same row $i$ have to be shorter than its height, a brute force algorithm would be to check if the previous condition is true, in code would be something like:

```python
def is_visible_from_left(i, j):
    return all([M[i][j] > M[i][pj] for pj in range(j)])

```

however, this would be too complex, a better approach would be just to compare $M[i][j]$ with a single value instead of $j's$

let $P(i, j)$ be the maximum height in the prefix $M[i][: j]$, in words, it is the maximum height of all trees in row $i$ before the current column $j$, then a tree would be visible from the left edge if its height $M[i][j]$ is larger than $P(i, j)$, this approach is much faster since we could update $P(i, j)$ as we traverse the grid $M$ and it only takes constant time to perform.


for the next tree in the same row $(i, j + 1)$ the value of $P(i, j + 1)$ is equal to the current maximum $P(i, j)$ and the height of the tree at $i, j$

$$
P(i, j + 1) = max(P(i, j), M[i][j])
$$

our base case is $P(0, j)=-inf$ for any $j=0, ..., m-1$,  that is the case when we have not seen any trees.

let's create a matrix $V$ with the same shape as $M$, $V[i][j]$ will indicate that the tree at location $i, j$ is visible from the left edge, initially $V[i][j] = 0$ for every i, j pair.

```python
for i in (0, ..., n-1):
    for j in (0, ..., n-1):
        # if the current tree is the new maximum, then it is visible
        V[i][j] = M[i][j] > P(i, j)
        # update the maximum for the new tree in the same row
        P(i, j + 1) = max(P(i, j), M[i][j])

```

the sum of all entries in $V$ is equal to the number of trees from the left edge.


nevertheless, we are asked to find the number of visible trees from any edge, not just from the left edge, to do so, we could either transform the matrix so that the algorithm above always works or change the algorithm to work with any direction (left, right, up, down), we will use the first solution.

the algorithm explained finds visible trees from the left, we could:
-  mirror the matrix $M$ so the right edge becomes the left edge
- transpose the matrix $M$ so the top edge becomes the left edge
- transpose and then mirror the matrix $M$ so that the bottom edge becomes the left edge



in python the transformations would look something like the following:
```python
mirror_grid = [row[::-1] for row in grid]
tranpose_grid = list(zip(*grid))
tranpose_mirror_grid = [row[::-1] for row in tranpose_grid]
```

for each transformation, we run the algorithm above and find the visible trees from each edge, let $A$ be a matrix of the same shape as $M$, $A[i][j]$ indicates if the tree located at $i, j$ in the matrix $M$ is visible from any edge, then

$$
A[i][j] = OR(\{ V_{left}[i][j], \ V_{right}[i][m - j - 1], \ V_{top}[j][i], \ V_{bottom}[j][n - i - 1] \})
$$

- to access $i, j$ in the $V_{left}$, we just index at location $i, j$ since no transformation is applied. 
- the $j$ column in the $V_{right}$ is equal to $m-j-1$ since its flipped horizontally.
- $V_{top}$ is transposed, so the $i, j$ are swapped to $j, i$
- $V_{bottom}$ is transposed first, so the $i, j$ are swapped to $j, i$ as before but then are mirrored, so the column is now $n - i - 1$

the final answer will be the sum of all entries in $A$, which denotes the number of visible trees in the grid.


### Complexity
#### Visibles Trees from the left edge
the time complexity of this algorithm is $O(nm)$ since we visit each tree only once and the space complexity is also $O(nm)$ since we store whether each is visible or not. 

since we execute the algorithm above a constant number of times (4), the time and space complexity remains the same


# Part 2
in this part we are asked to find the maximum scenic score in the grid $M$, you can review the definition of "scenic score" in the problem statement. as in part 1, we will start by the left edge.

for any tree at position $i, j$, we will look to the left and find the first tree that is taller or the same height as the current tree (if any), the left view distance is the number of trees in between the two, let $k$ be the index of such tree so that the view distance $D[i][j] = j - k$, in the case, that the current tree is that largest so far, then $k = 0$ and $D[i][j] = j - 0 = j$.

A brute-force to compute $D[i][j]$ is just to find $k$ by iterating from $k=j-1, ..., 0$ and stop when $M[i][k] >= M[i][j]$, in words, when we found a tree larger or equal than the current one, however, this is too complex!.


to explain the solution better, let us work with a single row of the grid. let ```M[i] = [3, 5, 3, 4, 5]```. we will iterate from $j=0$ up to the right end.

- $j=0$, since we have not seen any tree before, the view distance $D[i][0]=0$
- $j=1$, the current tree is taller than the only tree we've seen, therefore is the tallest so far and as explained before, $D[i][1] = 1 - 0 = 1$
- $j=2$, ha! now the previous tree is taller, so we can not see beyond the previous tree (5), therefore $k=1$ and $D[i][2] = 2 - 1 = 1$
- $j=3$, the previous tree (3) is shorter than the current one (4), however, it is not taller than the tree (5) at $j=1$, so $k=1$ and the view distance is $D[i][3] = 3 - 1 = 2$ 


we start to notice a pattern here, the tree $M[i][j]$ will only block the view of shorter trees to its right but as soon we encounter a tree $M[i][l]$ such that $l > j$ and $M[i][j] \ge M[i][j]$ we do not care about the current tree $M[i][j]$
since any tree far to right of column $l$ will be blocked first by tree $M[i][l]$, therefore, we will mantain a strictly decreasing monotonic stack $S_i$ for each row $i=0, ..., n-1$, where $M[i][S_i[j']] > M[i][S_i[j' + 1]]$ for any $j'$ in the stack.


the stack $S_i=[]$ will initially be empty which means there isn't any tree blocking the view, we start as before

- $j=0, S_i=[]$, the stack $S_i$ is empty, therefore $D[i][0]=0$ and we add the current index $j=0$ to the stack.

- $j=1, S_i=[0]$, the current height is 5 since it is larger than $M[i][S_i[-1]]=3$, we don't need to keep track of that tree anymore, we will remove it from the stack $S_i$, and append the current $j$. as in the previous step, $D[i][1]=1$

- $j=2, S_i=[1]$, the current height is 3, which is smaller than $M[i][S_i[-1]]=5$, so there is a tree blocking the view and it's located at index $S_i[-1]$, therefore $D[i][2]=j - S_i[-1] = 2 - 1 = 1$, finally, add the current index $j$ to the stack
- ...

we could translate the above as:
```python
# fixed i
for j in range(m):
    while S_i and M[i][j] > M[i][S_i[-1]]:
        S_i.pop()
                    
    last_index = S_i[-1] if len(S_i) > 0 else 0
    D[i][j] = j - last_index
    S_i.append(j)
```

we just have to do the algorithm above for every row, let $S = [S_0, ..., S_{n-1}]$ be an array of stacks, where $S[i] = S_i$ stores the stack for row $i$, then we could add another for loop to the code above as follows

```python
for i in range(n):
    S_i = S[i]
    # fixed i
    for j in range(m):
        while S_i and M[i][j] > M[i][S_i[-1]]:
            S_i.pop()
                        
        last_index = S_i[-1] if len(S_i) > 0 else 0
        D[i][j] = j - last_index
        S_i.append(j)
```

and we are done! we know how to compute the view distance from the left but..., this is only one of the directions we are asked for, however, we could use the matrix transformation trick of part 1 and use the algorithm multiple times.


let $A$ be a matrix of the same shape as $M$ where $A[i][j]$ indicates the scenic score of tree $i, j$, after computing the view distance from each direction (left, right, up, and down), we can compute $A[i][j]$ as follows:

$$
A[i][j] = D_{left}[i][j] * \ D_{right}[i][m - j - 1] * \ D_{top}[j][i] * \ D_{bottom}[j][n - i - 1]
$$

the final answer would be the maximum item in $A$


### Complexity
the time and space complexity is the same as part 1. $$O(nm)$$

