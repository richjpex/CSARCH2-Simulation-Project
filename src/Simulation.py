from collections import deque

class CacheSimulator:
    def __init__(self):
        # Cache configuration parameters
        self.cache_size = 32
        self.block_size = 64
        self.cache_line_size = 16
        self.lines_per_set = 8

        # Derived parameters
        self.num_blocks = max(self.cache_size // self.block_size, 1)
        self.num_sets = max(self.num_blocks // self.lines_per_set, 1)
        self.num_words_per_block = self.block_size // self.cache_line_size

        # Cache data structure initialization
        self.cache = [
            [{'valid': False, 'tag': None, 'data': [None] * self.num_words_per_block}
             for _ in range(self.lines_per_set)] for _ in range(self.num_sets)
        ]

        # FIFO queues for each set
        self.fifo_queues = [deque(maxlen=self.lines_per_set) for _ in range(self.num_sets)]

        # Memory access trace and counters
        self.cache_memory_trace = []
        self.hits = 0
        self.misses = 0

    def run_simulation(self, memory_access_sequence):
        # Simulate memory access sequence
        for address in memory_access_sequence:
            block_address, offset = divmod(address, self.block_size)
            set_index = (block_address // self.block_size) % self.num_sets
            tag = block_address // self.num_blocks

            # Check for cache hit
            hit = False
            for i in range(self.lines_per_set):
                if self.cache[set_index][i]['valid'] and self.cache[set_index][i]['tag'] == tag:
                    self.hits += 1
                    hit = True
                    break

            # Cache miss handling
            if not hit:
                self.misses += 1
                fifo_index = len(self.fifo_queues[set_index])
                self.fifo_queues[set_index].append(fifo_index)
                self.cache[set_index][self.fifo_queues[set_index][0]] = {
                    'valid': True, 'tag': tag, 'data': [None] * self.num_words_per_block
                }

            # Update memory access trace
            self.cache_memory_trace.append([line.copy() for line in self.cache])

        # Calculate performance metrics
        cache_hit_rate = self.hits / len(memory_access_sequence)
        cache_miss_rate = self.misses / len(memory_access_sequence)
        average_memory_access_time = cache_hit_rate * 1 + cache_miss_rate * 10
        total_memory_access_time = len(memory_access_sequence) * average_memory_access_time

        return {
            'hits': self.hits,
            'misses': self.misses,
            'cache_hit_rate': cache_hit_rate,
            'cache_miss_rate': cache_miss_rate,
            'average_memory_access_time': average_memory_access_time,
            'total_memory_access_time': total_memory_access_time
        }

    def reset_fifo_queues(self):
        # Reset FIFO queues to initial state
        self.fifo_queues = [deque(maxlen=self.lines_per_set) for _ in range(self.num_sets)]
