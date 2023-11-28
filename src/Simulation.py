from collections import deque

class CacheSimulator:
    def __init__(self):
        # Fixed cache size and block size as per instructions
        self.cache_size = 32
        self.block_size = 64

        # Fixed cache line size in words as per instructions
        self.cache_line_size = 16

        # Change the number of lines per set from 4 to 8
        self.lines_per_set = 8

        # Calculate the number of cache blocks and sets
        self.num_blocks = max(self.cache_size // self.block_size, 1)  # Ensure num_blocks is at least 1
        self.num_sets = max(self.num_blocks // self.lines_per_set, 1)  # Ensure num_sets is at least 1

        # Calculate the number of words per block based on the cache line size
        self.num_words_per_block = self.block_size // self.cache_line_size

        # Initialize the cache as a list of sets, each containing 8 lines (blocks)
        self.cache = [
            [{'valid': False, 'tag': None, 'data': [None] * self.num_words_per_block} for _ in range(self.lines_per_set)]
            for _ in range(self.num_sets)
        ]

        # Initialize a FIFO queue for each set
        self.fifo_queues = [deque(maxlen=self.lines_per_set) for _ in range(self.num_sets)]

        # Variables to store the cache memory trace
        self.cache_memory_trace = []

        # Variables to store simulation results
        self.hits = 0
        self.misses = 0

    def run_simulation(self, memory_access_sequence):
        for address in memory_access_sequence:
            block_address, offset = divmod(address, self.block_size)
            set_index = (block_address // self.block_size) % self.num_sets
            tag = block_address // self.num_blocks

            # Check each line in the set for a hit
            hit = False
            for i in range(self.lines_per_set):
                if self.cache[set_index][i]['valid'] and self.cache[set_index][i]['tag'] == tag:
                    # Cache hit
                    self.hits += 1
                    hit = True
                    break

            if not hit:
                # Cache miss
                self.misses += 1
                # Find the index of the next available slot in the FIFO queue
                fifo_index = len(self.fifo_queues[set_index])
                # Add the new block to the FIFO queue
                self.fifo_queues[set_index].append(fifo_index)
                # Replace the line at the front of the FIFO queue with the new block
                self.cache[set_index][self.fifo_queues[set_index][0]] = {'valid': True, 'tag': tag, 'data': [None] * self.num_words_per_block}

            # Log the cache memory state for each memory access
            self.cache_memory_trace.append([line.copy() for line in self.cache])

        # Calculate cache hit rate, cache miss rate, average memory access time, and total memory access time
        cache_hit_rate = self.hits / len(memory_access_sequence)
        cache_miss_rate = self.misses / len(memory_access_sequence)
        average_memory_access_time = cache_hit_rate * 1 + cache_miss_rate * 10  # Placeholder values for access times
        total_memory_access_time = len(memory_access_sequence) * average_memory_access_time

        # Return simulation results
        return {
            'hits': self.hits,
            'misses': self.misses,
            'cache_hit_rate': cache_hit_rate,
            'cache_miss_rate': cache_miss_rate,
            'average_memory_access_time': average_memory_access_time,
            'total_memory_access_time': total_memory_access_time
        }

    # Add a method to reset the FIFO queues after each simulation
    def reset_fifo_queues(self):
        self.fifo_queues = [deque(maxlen=self.lines_per_set) for _ in range(self.num_sets)]
