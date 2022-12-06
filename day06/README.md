# Day 6: Tuning Trouble

```python
"""
input:
    buffer: str
return:
    start-marker: int
"""
```

## Part 1
How many characters need to be processed before the first start-of-packet marker is detected?

### Solution
let the input string ```buffer``` be $S$ and let $n = |S|$ be the lenght of $S$ 

a start of packet is indicated as a sequence of $k=4$ distinct characters, our goal is to find the index $j$ such that the characters in $S[j-k + 1: j + 1]$ are all unique. 

A brute force approach is to try all possible index $\text {for }i=k, k+1, ..., n-1$ and check if it is a start-of-packet marker, however, the time complexity will be $O(nk)$ and we do not want to depend on $k$.

lets focus on the first $k$ characters of $S$, how can we know how many unique characters there are? exactly, we just count them, we will init a HashTable $H$ to map characters to its count, after we add the first $k$ elements to $H$, if the lenght of $H$ is equal to $k$, all the characters are unique, however, if the lenght of $H$ is less than $k$, there are some repeat characters and we know that $S[: k]$ is not start-of-packet marker. we can do the same for the characters in $S[1: k + 1]$, but we do not have to count them again, we simply decrease the count of character $S[0]$ by 1 and if $H[S[0]] == 0$, we remove $S[0]$ from $H$, finally we increase the count of character $S[k + 1]$ by 1 and check if it is a start-of-packet marker $(|H| == k)$


this is a sliding window approach, we will mantain a lenght $k$ window from index $i-k+1$ up to index $i$ (inclusive) for $i=k-1, ..., n-1$, at each iteration, we decrease the count of the item $S[i - k]$ (remove it from $H$ if $H[S[i-k]]==0$ ) and increase the count of $S[i]$, if the lenght of $H$ is equal to $k$, we will return $i + 1$, otherwise, we keep going.


### Complexity
the only operation we are doing is increasing or decreasing the count of characters in the HashTable $H$ which takes constant time $O(1)$ and perform this operation for each character in $S$, therefore, the time complexity is $O(n)$

the space complexity is $O(k)$ that is the maximum size of the HashTable $H$, we assume that $k$ is less or equal than the total number of possible characters and that $n \ge k$



## Part 2
part 2 is the same but we increase $k$ from 4 to 14.


### Complexity
same as for part 1.