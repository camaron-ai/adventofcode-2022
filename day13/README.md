# Day 13: Distress Signal
## Parsing the input

with the help of ```json.loads``` function we can turn the input package string into actual python lists :). we just have to apply the function to all packets in the input.


let $P$ be the array of package's pairs (puzzle input), where $P[i] = (l_i, r_i)$ stores the left $l_i$ and right $r_i$ package of the ith pair.

let $n$ be equal to the number of packages $n = |P|$ and $m_p$ be the maximum number of items in a single package across all packages in the input. for example, the next package ```[1,[2,[3,[4,[5,6,7]]]],8,9]``` stores 9 items.


## Part 1
in part 1 we have to determine whether a pair $P[i] = (l_i, r_i)$ is in order. for the rest of part 1, since we only compare $l_i$ and $r_i$ we will denote $l_i$ as $l$ and $r_i$ as $r$ for easy notation :).

let $j$ be the index of current item being compared, if $j=1$ then we are comparing the second item of each package $l$ and $r$.

to determine whether the pair $l, r$ is in the right order, we follow the next rules (initially $j=0$)

- if both $l[j], r[j]$ are integers, then:
    - if $l[j] \lt r[j]$ the packages are IN the right other
    - if $l[j] \gt r[j]$ the packages are NOT IN the right other
    - otherwise, $l[j] = r[j]$, we move to the next item, $j += 1$
- otherwise, at least one of $l[j], r[i]$ is an array so we can't compare them directly, we will transform integers to arrays as the problem statement says (if necessary) and then compare $l[j], r[j]$ recursively, if we can not decide with inner packages $l[j], r[j]$, we will move to the next package $j += 1$

when comparing two items $l[j] = r[j]$ we have 3 possible states, whether they are in order (state=1), they are equal (state=0) or they are not in order (state=-1), let the state $s_j$ be the state of the items $l[j], r[j]$

for example, let's take the following two packages 
$$
l = [1,1,3,1,1], r = [1,1,5,1,1]
$$

if we compare them item by item, we will get:

```python
"""
l = [1, 1, 3, 1, 1]
r = [1, 1, 5, 1, 1]
s = [0, 0, 1, 0, 0]
"""
```

the first two comparisons are not enough to decide since they are equal (status=0), however, at $j=2$ the left item $l[j]$ is less than the right item $r[j]$ so we know that they are in order. let's take a harder example

```python
"""
l = [[1], [2,3,4]]
r = [[1], 4]
"""
```

we first compare the left ```[1]``` with the right ```[1]```, because they are lists we can not compare them directly, so we can recursively solve the same problem with packages ```([1],  [1])``` so we are left with: 


```python
"""
l = [1]
r = [1]
s = [0]
"""
```

since they are equal, we can not determine whether they are in order or not, so going back to the main problem

```python
"""
l = [[1], [2,3,4]]
r = [[1], 4]
s = [0, ]
"""
```

since $s_0=0$, we move to the next item and do the same, however, note that $r[j]=4$ is not an array and $l[j]$ is, so we turn it into one before comparing both items. next we recursively solve the same problem for ```([2,3,4],  [4])```

```python
"""
l = [2,3,4]
r = [4]
s = [1]
```

since $2 \le 4$, we can early stop and return that they are in order (status=1). back to the main problem we have:

```python
"""
l = [[1], [2,3,4]]
r = [[1], 4]
s = [0, 1]
"""
```
as soon we've seen a status $s_j$ different from 0, we can stop and return it, so the original pairs $l$ and $r$ are in the right order.


the algorithm works as follows:

```python
def is_pair_in_right_order(
    p1: PacketType,
    p2: PacketType,
    i: int = 0
    ) -> bool:

    # if we reach the end of any package is because
    # we couldn't make a decision before, therefore 
    # if len(p1) < len(p2), then they are in order
    # if they are equal, we can not make a decision
    # otherwise, they are not in order
    if i == min(len(p1), len(p2)):
        return compare_integers(len(p1), len(p2))
    
    left, right = p1[i], p2[i]
    left_is_int = isinstance(left, int)
    right_is_int = isinstance(right, int)

    if left_is_int and right_is_int:
        status = compare_integers(left, right)
    else:
        left = [left] if left_is_int else left
        right = [right] if right_is_int else right

        # determine if the inner package is in order
        status = is_pair_in_right_order(left, right)
    # not decision can be made so far, move to the next element
    if status == 0:
        return is_pair_in_right_order(p1, p2, i + 1)
    return status
```

the ```is_pair_in_right_order(x, y)``` function will return $1$ if ```x < y```, $0$ if they are equal and $-1$ otherwise.


### Complexity
in the worst case, we have to decide whether two packages are in order based on their length, which happens once we traverse both packages entirely $j=m_p-1$, therefore, the time complexity is $O(m_p)$

the space complexity is also $O(m_p)$ since in the worst case we have to turn each integer in a package $l[j]$ into an array with a single item $[l[j]]$ to compare them correctly.



# Part 2
let $A$ be a list of all packages in the input, $A$ is basically a flat version of $P$, additionaly add the divider packages ```[[2]], [[6]]``` at the end of $A$.

we are asked to sort all packages in $A$ and then find the indices of the divider packages, and the solution is as simple as that.

we will say that $A[i]$ should go first in the sorted order then $A[j]$ if ```is_pair_in_right_order(A[i], [j]) == 1``` (they are in the right order), otherwise, $A[j]$ should go first.

we could use any sorting algorithm we want and use the above condition to sort all the items, then, we just scan the sorted version of $A$ and find the divider packages.

finally, we return the 'decoder key', which is the product of the indices of the divider packages.



### Complexity
if we use merge sort which has time complexity $O(nlogn)$, then the final time complexity is $O(nlogn * n_o)$ since each comparison is bounded by $O(n_o)$ 

the space complexity is $O(n)$ due to the spaced need it to create array $A$.

