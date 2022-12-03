# Day 2: Rock Paper Scissors
Compute the score based on the elves' guide.
```python
"""
input:
    strategies: List[Tuple[str, str]]
return:
    score: int
"""
```
let $N$ be the number of plays.

# Part 1

for part1 and part2, we will encode the input string A, B, C and X, Y, Z to an integer for easier manipulation.

```python
HAND_SHAPE_TO_INT = {
    # rock, paper, scissors
    "A": 0, "B": 1, "C":2,
    "X": 0, "Y": 1, "Z": 2
}
```

given my oponent move $op$ and my response $move$, we build a matrix $M$ to compute the outcome score $score = M[op][move]$.

finally, the answer is equal to

$$
\sum_{i=0}^{n-1} (M[op_i][move_i] + move_i + 1)
$$


### Complexity
the time complexity is linear on the number of plays $O(N)$, the space complexity is also linear because the character encoding from string to integers, but we could improve to constant $O(1)$ if we do the encoding only when we access the matrix.


# Part 2
part2 is not much different from the previous problem, given my opponent move $op$ and the outcome of the game $outcome$, we just have to figure out what move we should play to accomplish the outcome, for that, we build another matrix $MO$ to access the response $move$ in constant time. 

$$
move = MO[op][outcome]
$$

finally, the answer is equal to

$$
\sum_{i=0}^{n-1} (2 * outcome_i + MO[op][outcome] + 1)
$$

since we already know what the outcome is and $outcome \in \{0, 1, 2 \}$, we multiply the outcome by 2 to get the game score and add the response score $(move + 1)$ 

### Complexity
the complexity is the same as the first part.
