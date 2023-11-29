# CSARCH2-Simulation-Project

**Cache Simulation Project of Group 10 - CSARCH2 S11**

**Members:** <br>
Cabinbin, Pierre Genric Navarro <br>
Cada, Louis Ezechiel Limbo <br>
Chong, Hans Kirzen Yu <br>
Pecson, Richard John Jr. Quitain <br>

## What is 8-way Block Set Associative, First In First Out (8-way BSA + FIFO)

<div align="justify">An 8-way Block Set Associative (8-way BSA) cache is a sophisticated cache organization in computer architecture. In this design, the cache is partitioned into sets, each holding a fixed number of lines or blocks. The "8-way" in "8-way BSA" signifies that each set accommodates 8 lines.

Here's a concise breakdown of the terminology:

- **Block/Set:** Data is stored in blocks within a cache. A set-associative cache, like the 8-way BSA cache, features sets, and each set comprises multiple blocks (8 blocks per set in this case).

- **Associativity:** Refers to the number of lines or blocks in a set. The cache is 8-way set-associative, meaning there are 8 blocks in each set.

Adding "First In First Out" (FIFO) to the mix implies that within each set, blocks are managed in a First In First Out manner. When a new block enters a set, it displaces the oldest block in that set. FIFO serves as a replacement policy for blocks within a set.

In summary, the 8-way Block Set Associative, First In First Out (8-way BSA + FIFO) cache is an organizational approach where the cache is divided into sets, each containing 8 blocks. The replacement policy within each set follows a First In First Out order. This design aims to balance the benefits of associativity (reducing cache conflicts) with the simplicity of a FIFO replacement policy.</div>

![csarch](https://github.com/richjpex/CSARCH2-Simulation-Project/assets/148311130/ff4c49bc-3252-4b98-95af-8d606e4b8f46)

<br>

*This is how the algorithm should work.*

## Program Overview

<div align="justify">The program is an 8-way BSA + FIFO cache simulation implemented in Python. It includes:
- Three test case choices: Sequential, Random, and Mid-repeating.
- Input for the number of memory blocks the cache will simulate.
- A button to run the simulation with valid input.
- Simulation Statistics: Displays memory access count, cache hit and miss counts, cache hit and miss rates, average memory access time, and total memory access time.
- Sequence Display: Shows the values injected into the cache.
- Final Cache Snapshot: Displays how the memory is captured, with a log of values used for simulation visible in the terminal. A video presentation of the program's functionalities is also available.</div>

<br><br>

# Detailed Analysis of Test Cases

*N is the number of cache blocks.*

## Test Case A

<div align="justify">The Sequential Sequence utilizes up to 2n cache blocks, repeating the sequence 4 times. The sequence access pattern exhibits strong "spatial locality," favoring an 8-way Block Set Associative structure. With a closer numbering sequence, more elements can be loaded, resulting in a higher hit count. For instance, if n = 4, the sequence would be 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, repeated 4 times.</div>

## Test Case B

<div align="justify">The Random Sequence utilizes up to 4n cache blocks with a random access pattern. The randomness challenges the effectiveness of 8-way BSA and FIFO, leading to a lower hit rate. For example, if n = 4, the sequence would be randomly generated with 4(4) = 16 unique block addresses.</div>

## Test Case C

<div align="justify">The Mid-Repeat Blocks start at block 0, repeat the sequence in the middle twice up to n-1 blocks, and continue up to 2n. The 8-way BSA performs moderately well due to the repeated middle sequence, enhancing the hit rate. FIFO also shows moderate efficiency, replacing initially loaded blocks and repeating the first part of the sequence. For example, if n = 4, the sequence would be 0, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, repeated 4 times.</div>