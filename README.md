# CSARCH2-Simulation-Project
**Cache Simulation Project of Group 10 - CSARCH2 S11**

<br>

**Members:** <br>
Cabinbin, Pierre Genric Navarro <br>
Cada, Louis Ezechiel Limbo <br>
Chong, Hans Kirzen Yu <br>
Pecson, Richard John Jr. Quitain <br>


## 8-way Block Set Associative, First In First Out
<div align="justify"> The program is an 8-way BSA + FIFO cache simulation made in Python. It consists of: 3 test case choices from A to C representing Sequential, Random, and Mid-repeating; An input for the amount of memory blocks the cache will simulate; A button to run the simulation once a valid input is made; the Simulation Statistics where we can observe the memory access count, cache hit and miss counts, cache hit and miss rates, average memory access time, and total memory access time; and the Final Cache Snapshot which we can see how the memory is finally captured, a log of the values used to simulate the case can be seen in the terminal. A video is also made here to present the program's functionalities. </div>

<br><br>

![csarch](https://github.com/richjpex/CSARCH2-Simulation-Project/assets/148311130/ff4c49bc-3252-4b98-95af-8d606e4b8f46)
<br>
This is how the algorithm should work.


# Test Cases
N is the number of cache blocks.

## Test Case A
<div align="justify">The Sequential Sequence uses up to 2n cache blocks and it repeats the sequence 4 times. The way the sequence is accessed will have strong "spatial locality", which means it will likely be a accessed because of the close numbering sequence. Since it's an 8-way Block Set Associative, it contains more blocks and can load more elements. This result to having more hit count. An example would be if n = 4, the sequence would be 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 repeated 4 times.</div>

## Test Case B
<div align="justify">The Random Sequence uses up to 4n cache blocks and it's at random. As such, BSA may not be as good because of its randomness. This also applies to FIFO as it performs worse because the sequence is at random, the blocks that are loaded in may not be replaced again. This will result in a lower hit rate count. An example would be if the if n = 4, the sequence would be at random with 4(4) = 16 unique block addresses.</div>

## Test Case C
<div align="justify">The Mid-Repeat Blocks starts at block 0, then it repeats the sequence in the middle two times up to n-1 blocks, afterwards it continues up to 2n. Then, repeat the sequence four times. BSA is moderately good because of the repeated middle sequence as it allows for the hit rate count to increase. FIFO is also moderate because it will replace the blocks that were loaded in first and repeat the first part of the sequence. An example would be if n = 4, the sequence would be 0, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 repeated 4 times.</div>
