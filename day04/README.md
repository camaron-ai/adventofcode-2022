# Day 4: Camp Cleanup
## Part 1
In how many assignment pairs do the ranges overlap?
### Solution
let $A$ be the input array, let $n = |A|$ be number of pairs in the input. 

each entry in $A$ is compose of a pair of sections $A[i] = (p_{i1}, p_{i2})$, where $p_{ij} = (s_{ij}, e_{ij})$ is the elves' section . 

the task in part 1 is to count how many pairs fully overlaps with each other to avoid repeated work.

for the pair $(p_{i1}, p_{i2})$ to fully overlap, one section must be within the other, in math:

$$
[[ s_{i1} \le s_{i2} \le e_{i2} \le e_{i1} ]] + [[s_{i2} \le s_{i1} \le e_{i1} \le e_{i2}]]
$$

where $[[\ ]]$ operator turns a boolean to its integer representation. 

we just to apply the expresion above to every pair in the input.  

the final answer would be


$$
\sum_{i=0}^{n-1}[[ s_{i1} \le s_{i2} \le e_{i2} \le e_{i1} ]] + [[s_{i2} \le s_{i1} \le e_{i1} \le e_{i2}]]
$$


### Complexity
the time complexity to determine wheter a pair overlaps in constant, so the time complexity is linear $O(n)$.

the space complexity is constant $O(1)$



## Part 2
In how many assignment pairs do the ranges overlap?
### Solution

now we have to determine if a pair $(p_{i1}, p_{i2})$ overlaps at all.

it is easier to determine if the pair $p_{i1}$ do not overlap with $p_{i2}$, if they dont overlap, then $p_{i1}$ must end before $p_{i2}$ starts or $p_{i1}$ must start after $p_{i2}$ ends, in math:

$$
[[ e_{i1} \lt s_{i2}]] + [[e_{i2} \lt s_{i1}]]
$$

since we are looking for overlapping pairs, we have to negate the expression above


as in part 1, the final answer is:

$$
n - \sum_{i=0}^{n-1}[[ e_{i1} \lt s_{i2}]] + [[e_{i2} \lt s_{i1}]]
$$


### Complexity
the time and space complexity is the same as part 1.