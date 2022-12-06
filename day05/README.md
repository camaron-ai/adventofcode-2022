# Day 5: Supply Stacks


# Parsing the input
the hardest part of this problem is to parse the input into stacks :).

```python
"""
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
"""
```
we first split the string at each line to form a matrix
```python
"""
[
    [    [D]    ],
    [[N] [C]    ],
    [[Z] [M] [P]],
    [ 1   2   3 ],
]
"""
```
let $L$ be the number of lines in the input string, in this case $L=4$. 

we know that the last line $L-1$ is composed of indices marking the stack id, my implementations locates this indices to know in what column the stack's values should be, for example, the index ```"1"``` is located at column 1, since its the second character in the last line, therefore all values in stack 1 should be in column 1, so we just iterate bottom up (from line $L-2$ up to 0) and add the corresponding characters to the first stack (if any). we repeat the process for each stack in the input.

thankfully, parsing the crane's instructions is pretty straightforward :).

the input to our algorithm is an array of stacks $S=[s_0, s_1, ..., s_{m-1}]$, where $m$ is the total number of stacks and $s_i$ stores the characeters in the ith stack. Also we are given a sequences of instructions:

$$
I=[(c_0, from_0, to_0), (c_1, from_1, to_1), ..., (c_{n-1}, from_{n-1}, to_{n-1})]
$$

where $n$ is the total number of instructions and $I[i] = (c_i, from_i, to_i)$ indicates the number of crates $c_i$ to move from stack $from_i$ to stack $to_i$.

# Part 1
in part 1 we have to execute all the input instructions $I$ to the stacks $S$, this crane can only move one crate at a time, so for any instruction $(c_i, from_i, to_i)$, we pop the last item from stack $x=S[from_i]$ and add it at the end of stack $S[to_i]$, we repeat this process $c_i$ times.

```python
for _ in range(c_i):
    S[to_i].append(
        S[from_i].pop() 
        )

```

after we apply all the instructions in $I$, we create a string with the last item in each stack $S$.


### Complexity
since popping and appending a value to a stack takes amortized $O(1)$ time, the time complexity is bounded by the total number of moves carried by the crane $N$.

$$
N = \sum_{i=0}^{n-1}c_i
$$

finally, the time complexity to create the output string with the last value in each stack is $O(|S|)=O(m)$, so the final time complexity is $O(N + m)$

if we do not take in consideration the space need it to create the output string, then the space complexity is $O(1)$

## Part 2

now we have updated the crane and we are able to move multiple crates at once, so for any instruction $(c_i, from_i, to_i)$, we copy the last $c_i$ crates from stack $S[from_i]$ to stack $S[to_i]$ and then remove them from $S[from_i]$

```python
# add last c_i items in same order
S[to_id].extend(
    S[from_i][-c_i: ]
)
# remove last c_i items
for _ in range(c_i):
    S[from_i].pop()
```

as in part 1, after we apply all the instructions in $I$, we create a string with the last item in each stack $S$.

### Complexity
the time and space complexity is the same as in part 1