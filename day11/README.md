# Day 11: Monkey in the Middle

this one took me a while but it was fun!

# Parsing the input

the information for a single monkey looks like:

```python
"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
"""
```

I won't enter into details of how we should parse the input, however, we will introduce some notation, let: 

- $A_i$ be the items of the ith monkey, where $A_i[j]=w$ is the worry level of jth item.  
- $g_i(old)$ be the operation performed by the ith monkey
- $D_i$ be the divisor of the ith monkey
- $T_i$ be the id of the monkey that we will pass the current item to if the condition is true
- $F_i$ be the id of the monkey that we will pass the current item to if the condition is false

for example, given the input monkey above, then

$$
A_0=[79, 98]\\
D_0 = 23\\ 
T_0 = 2\\ 
F_0 = 3\\
g_0(old) = old * 19\\
$$


# Part 1
part 1 is trivial since we just have to execute the game's rules, so we'll skip to the interesting part. Also, the next solution works for part 1


# Part 2
As we keep playing the game, the worry levels start to grow very fast reaching ridiculous amounts, and operations like sum, multiply or modulus takes longer, so we need to keep our worry levels manageable.

the goal is to find the number of inspected items by each monkey, so the first thing to notice is that we do not care about the actual values of the worry levels, given some worry level $w$, we apply an operation $g_i(w)$ and then decide to what monkey we should throw the current item, let's work with an example

let's say $D_i=3$ and $g_i(old) = old + 2$, we receive the worry level $w=4$, then apply $w=g_i(w)=6$ and then we check if $w \mod D_i == 0 \rarr 6 \mod 3 == 0$, since the condition is true, we throw the item to monkey $T_i$. however, if the intial worry level was $w=10$, or $w=13$ or $w=139390$ then the outcome would be the same.

the monkey's decision is based on whether $w$ is divisible by $D_i$, so what if we could find a transformation $f(w)$ such that the remainder of $w$ and $D_i$ is the same after we apply $f(w)$, $w \mod D_i == f(w) \mod D_i$, for now, let us assume we already know this function. 

My next worry was if the operation $g_i(w)$ will change the remainder after we apply $f(w)$, but monkeys can only add or multiply the current worry level $w$ and after some math, we realize the following:

$$
(w + b) \mod D_i = \bigg( w \mod D_i + b \mod D_i  \bigg) \mod D_i \\
(w * a) \mod D_i =  \bigg( w \mod D_i \bigg) * \bigg( a \mod D_i  \bigg)
$$

so if the transformation $f(w)$ keeps the remainder the same, then $g_i(w) \mod D_i$ is the same as $g_i(f(w)) \mod D_i$

so we can reduce the problem to finding the function $f(w)$, which is equal to 

$$
f(w) = w \mod C
$$ 

where $C$ is any common multiple of all monkey's divisors.

let's say we have 2 monkeys with divisors $D_0=2, D_1=3$, then the simplest common multiple is the product between the 2, $C=6$, lets apply the transformation and check that the remainder is the same before and after the transformation.


```python
"""
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] (raw worry levels)
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,   1,  0,  1,  0,  1] (w mod 2)
[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1,   2,  0,  1,  2,  0] (w mod 3)


after we apply f(w) = w % 6
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] (raw worry levels)
[0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4,   5,  0,  1,  2,  3] (f(w) = w % 6)
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,   1,  0,  1,  0,  1] (f(w) mod 2)
[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1,   2,  0,  1,  2,  0] (f(w) mod 3)

"""
```

because $f(w)$ will map $w$ to the range from $0$ to $C - 1$, we will always keep the worry levels manageable and operation on it will be as fast as possible.

back to the problem, we will let the common multiple between the divisors equal to their multiplication

$$
C = \prod_{i=0}^{n - 1}D_i
$$

to play a round of the game, we will iterate for each monkey $i$ and for each item $w$ that the current monkey holds, we will:
- apply the operation $g_i(w)$
- bound the worry level, $w = w \mod C$
- divide the worry level by 3 (only in part 1)
- decide to what monkey we should throw the current item
- increase the number of inspected items of the current monkey by 1


we will play for 10_000 rounds while keeping track of the number of inspected items by each monkey, finally, we return to the level of monkey business at the end of the game.



### Complexity
let $n$ be the number of monkeys, $m$ be the number of items and $R$ be the number of rounds played.


in the worst case scenario, the first monkey holds all the items and throws them to the second monkey, then the second monkey throws them to the third and the third to the fourth and so on., therefore, we will inspect each item $n$ times, so the total number of operation in a single round is $nm$

since we play multiple rounds, the time complexity of the game is $O(Rnm)$, however, we still need to get the top two numbers of inspected items, which takes $O(nlogn)$ time (we use sorting), thus the final time complexity is $O(Rnm + nlogn)$


besides storing all information for each monkey, we create an array to keep track of the inspected items by each monkey, therefore, the space complexity is linear on the number of monkeys $O(n)$
