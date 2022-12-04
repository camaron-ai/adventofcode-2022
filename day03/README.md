# Day 3: Rucksack Reorganization

```python
"""
input:
    rucksacks: List[str]
output:
    priority_score: int
"""
```

## Part 1
Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?


let $A$ be the input array ```rucksacks```, let $n = |A|$ and let $A[i] = s_i$ be a single elves' rucksack. 


### Solution

for every $s_i$, we must find the common character between the first and second half of the string, for that, we will build a HashSet $H_{i_1}$ and $H_{i_2}$ to get the unique items in each halves and find the intersection between the two sets. 

We could also use a DAA instead of a HashSet since we are dealing with character strings but its easier to work with HashSet and the complexity is in average, the same.

the interstection $t_i$ between the two sets is defined as

$$
t_i = H_{i_1} \cap H_{i_2} 
$$

after we computed $t_i$, we just have to compute the priority score $sp_i$ as follows

$$
sp_i = ord(L(t_i)) - ord("a") + 1 + 26U(t_i)
$$

where
- $L(t_i)$ returns the lowercase version of $t_i$, $L(A) = a$
- $U(t_i)$ returns 1 if $t_i$ is a uppercase character, otherwise returns 0. 

$$
U(t_i) = [[ \text{ $t_i$ is uppercase }  ]]
$$

- $ord(t_i)$ returns an integer representing the Unicode character of $t_i$

 
 finally, we just to apply sum all priority score $sp_i$ for each rucksack string $s_i$

 $$
\sum_{i=0}^{n-1} sp_i 
 $$

 ### Complexity
 let $k$ be the lenght of the longest string $s_i$ in the input $A$, the time complexity to compute the intersection $t_i$ is bounded by $O(k)$, therefore, since we have to compute the intersection for all strings, the time complexity is $O(nk)$

the space complexity is $O(k)$ that is the cost of creating the HashSets $H_{i_1}, H_{i_2}$


## Part 2
### Solution
part 2 is the same as part 1 but now we have to compute the intersection between group of rucksacks $g_i$. let $g_i$ be equal to

$$
g_i = [s_{3 * i}, s_{3 * i + 1}, s_{3 * i + 2}], \text{ for i=0, 1, 2, n/3 - 1}
$$

now, we will create 3 hashSets $H_{i_1}, H_{i_2}, H_{i_3}$ to get the unique characters in each rucksack within the group $i$, and the intersection $t_i$ is defined as 

$$
t_i = H_{i_1} \cap H_{i_2} \cap H_{i_3} 
$$

we can compute the score $sp_i$ as we did in part 1, and the final answer is the sum of all $sp_i$ for each group $g_i$

 $$
\sum_{i=0}^{n//3-1} sp_i 
 $$

### Complexity
the space and time complexity is the same as in part1