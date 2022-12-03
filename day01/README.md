# Day 1: Calorie Counting

## Part 1
Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
```python
"""
input:
    calories: List[List[int]]
return:
    maximum number of calories in the input
"""
```

let $n$ be number of calories, and $N$ be the number of elves.


### Solution
we first sum over each elves' calories to get the total calories carried by an individual elf, then we take the maximum over all elves.

### Complexity
the time complexity is linear $O(n)$ and constant space $O(1)$


## Part 2
Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?

### Solution
again, we first sum over each elves' calories to get the total calories carried by an individual elf, to avoid using extra space, we will reuse the input array `calories[i] = sum(calories[i])`.
then we could sort the entire array and get the last 3 elements but this will take $O(NlogN)$, so to avoid sorting, we use a heap of size 3 and keep track of the 3 largest element, this will take $O(Nlog3)=O(N)$ 

finally, we sum the elements in the heap, which takes constant time.

### Complexity
the time complexity is $O(n)$ and space complexity is constant $O(1)$