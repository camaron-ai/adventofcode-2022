# Day 7: No Space Left On Device

## Parsing the input
as day05, the hardest part of the problem is to parse the input string into something we can work with, this time we will parse the raw input text into a Tree structure, and we'll define a TreeNode as follows:

```python
class TreeNode:
    def __init__(self,
        size: int = 0,
        parent: 'TreeNode' = None):
        """
        input:
            size: the size of the current node, for directories we assume it is 0
            parent: pointer to the parent node  
        it creates two more attributes
            children: pointers to the node's children.
            _total_size: stores the total size of the subtree rooted at this node,
            initially -1
        """
        self.size = size
        self.parent = parent
        self.children = list()
        self._total_size = -1
```

we will split the input string $S$ into lines, let $l_i$ be the ith line of $S$

the input string has the following structure: 
- every command line starts with a ```$```
- there are two types of command ```cd``` and ```ls```.
- the ```cd``` string is followed by the folder name or ```'..'```
- the next lines after a ```ls``` command are the files within the current directory
- files are listed as ```'{size} {name}'``` 
- directories are listed as ```'dir {name}'```

the first line $l_0$ is always  ```cd /```, this directory will be our root $R$, which has no parent $P[R]=null$ and has no size $R.size = 0$

we will assume that only directories will have a size of 0, which is not always true but it worked for the test case :). 

we will init a hashtable $H$ that maps folder names to TreeNodes so we can access nodes when we execute the ```cd``` command

starting at the second line $i=1$ and the root $R$ pointing to ```/``` directory, we will apply the algorithm below:

```python
while i < len(S):
    l_i = S[i] # get the ith line, this line will always be a command
    if is_a_cd_command(l_i):
        next_dir = get_next_dir(l_i)
        if next_dir == '..':
            # update the current root to its parent
            R = R.parent
        else:
            # set the current root to {next_dir}'s node
            R = H[next_dir]
        # move to the next line
        i += 1
    else:
        for size, name in upcoming_listed_files(i):
            # create a new node with size {size}
            # and parent equal to the current root R
            node = Node(size, parent=R)
            # add the current node to the root's children
            R.chidren.append(node)

            # if the current item is a directory
            # we will execute the cd command later
            # so save in H
            if size == 0:
                H[name] = node
        i = move_to_next_command_line()
```

note that all files in the tree are leaves, which is what we expect.


## Part 1
for part 1, we have to find all directories that have sizes under 100k and compute the sum of the total sizes of those directories.

### Compute the size of directories

let $T(N)$ be the total size of a directory located at node $N$, which is equal to the sum of sizes of all files within the subtree rooted as node $N$. 

in math, we can define $T(N)$ as follows:
$$
T(N) = N.size + \sum_{C_i \in N.children} T(C_i)
$$

for any leaf $L$,  $T(N) = L.size$ since leaves have no children.  this will be our base case

for any folder $N$, $T(N)$ will recurse on every file $L$ within the subtree rooted at $N$.

this is called a subtree property, knowing the answer to $T(C_i)$ for every child will allow us to compute the answer $T(N)$ of the current node $N$ in time bounded by the number of children.

we only have to do this computation once and store the $T(N)$ in each node so we can reuse them later.

### get the size of directories
we will store the sizes for each directory in an array $SZ$ and we will do so by traversing each node $N$ in the tree, starting at the root $R$ and if $N$ is a directory, we will append $T(N)$ to $SZ$.


### Solution
after we have computed $SZ$, we just sum all sizes in the array $SZ$ that are under 100k.

### Complexity
the time complexity is linear on the number of nodes in the tree $O(n)$, which is the same as the number of files and folders in the filesystem.


## Part 2
for part 2 we also need the array $SZ$

we will define the free space as $E = 70000000-T(R)$

finally, we will choose the minimum size $ sz \in SZ$ such that $E + sz \ge 30000000$

### Complexity
the time complexity is the same as in part 1