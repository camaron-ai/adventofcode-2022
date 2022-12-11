# Day 10: Cathode-Ray Tube

## Parsing the input

there are two types of command, the ```noop```which takes 1 cycle and does not change the value of the register $X$, and the ```addx V``` command, this one takes 2 cycles and adds the value of $V$ to $X$

we will create an array of instructions $I$, where $I[i] = v_i$ is the value we have to add to the register $X$ in the ith cycle. 

let $i$ be the current cycle, we assume that there is no task being executed

- the ```noop``` does nothing, so $I[i] = 0$
- the ```addx V``` takes two cycles, in the first cycle the register $X$ do not change and in the second cycle we add $V$ to $X$, therefore $I[i] = 0$ and $I[i + 1] = V$ 

for example, if we parse the instructions below:
```python
"""
noop
addx 3
addx -5
"""
```

we will get:
```python
[
    0, 
    0,
    3,
    0,
    -5
]
```

## Part 1

let $R$ be an array such that ith item $R[i] = X_i$ is the cpu's register value at the start of cycle $i$, we are asked to find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.

the signal strength is defined as

$$
S(i) = R[i] * i
$$

first we need to compute the array $R$, which is pretty straightforward given $I$, the register's value at cycle $i$ is equal to the last value $R[i-1]$ plus $I[i]$.

$$
R[i] = R[i - 1] + I[i]
$$



after we've computed $R$, we compute the total signal strength as:

$$
\sum_{c \in C} R[c] * c
$$

where $C = [20, 60, 100, 140, 180, 220]$



### Complexity
the time complexity is equal to the length of $I$, which is bounded by the number of instructions we are given, if we let $N$ be the number of instructions, then the time complexity is $O(N)$

the space complexity is the same since we store the register's value at each cycle



## Part 2
for part 2, we will reuse the algorithm for computing $R$.

let $D$ be a matrix of size (6, 40) which simulates the display, the state (on, off) of the pixel at location $j, k$ is stored at $D[j][k]$

to determine the state of each pixel, we just apply the code below:
```python
for cycle in (0, ..., 240):
    row, col = get_cycle_coor(cycle)
    D[row][col] = abs(R[cycle] - col) <= 1
```

finally, we can print the display by turning $D$ into a string.


### Complexity
the time and space complexity is the same as before.