import random

class Cache:
    def __init__(self, blocks=32, line=16, sets=8):
        self.blocks = blocks
        self.line = line
        self.sets = sets
        self.words_per_block = line  # Adjusted to use the line size as words per block
        self.cache = [[[-1 for _ in range(self.words_per_block)] for _ in range(sets)] for _ in range(blocks)]
        self.queue = [0 for _ in range(blocks)]
        self.pointer = 0
        self.stats = {
            'accesses': 0,
            'hits': 0,
            'misses': 0,
            'hit_rate': 0,
            'miss_rate': 0,
            'average_access_time': 0,
            'total_access_time': 0,
        }

    def read(self, address):
        block = address // self.words_per_block  # Adjusted to use words_per_block for block calculation
        self.stats['accesses'] += 1
        for i in range(self.sets):
            for j in range(self.words_per_block):
                if self.cache[block][i][j] == address:
                    self.stats['hits'] += 1
                    self.stats['total_access_time'] += 1
                    return
        self.stats['misses'] += 1
        self.stats['total_access_time'] += 10
        index = self.pointer % self.words_per_block  # Adjusted to use words_per_block for indexing
        self.cache[block][index // self.line][index % self.line] = address
        self.pointer += 1

    def print_stats(self):
        total_accesses = self.stats['accesses']
        total_hits = self.stats['hits']
        total_misses = self.stats['misses']
        self.stats['hit_rate'] = (total_hits / total_accesses) * 100 if total_accesses != 0 else 0
        self.stats['miss_rate'] = (total_misses / total_accesses) * 100 if total_accesses != 0 else 0
        self.stats['average_access_time'] = self.stats['total_access_time'] / total_accesses if total_accesses != 0 else 0

        print(f'Total memory accesses: {total_accesses}')
        print(f'Total cache hits: {total_hits}')
        print(f'Total cache misses: {total_misses}')
        print(f'Cache hit rate: {self.stats["hit_rate"]:.2f}%')  # Display as percentage with two decimal places
        print(f'Cache miss rate: {self.stats["miss_rate"]:.2f}%')  # Display as percentage with two decimal places
        print(f'Average memory access time: {self.stats["average_access_time"]}')
        print(f'Total memory access time: {self.stats["total_access_time"]}')

if __name__ == '__main__':
    n = int(input('Enter the number of memory blocks: '))
    cache = Cache()

    # Test case 1: Sequential memory access sequence
    print("1. Sequential memory access sequence")
    for _ in range(4):  # Repeat the sequence four times
        for i in range(n * 2):
            address = i % (n * 2)  # Generate addresses from 0 to 2n-1
            cache.read(address)
    cache.print_stats()

    # Reset stats
    cache.stats = {
        'accesses': 0,
        'hits': 0,
        'misses': 0,
        'hit_rate': 0,
        'miss_rate': 0,
        'average_access_time': 0,
        'total_access_time': 0,
    }

    # Test case 2: Random memory access sequence
    print("\n2. Random memory access sequence")
    sequence = [random.randint(0, 2 * (n // 2) - 1) for _ in range(4 * (n // 2))]
    for address in sequence:
        cache.read(address)
    cache.print_stats()

    # Reset stats
    cache.stats = {
        'accesses': 0,
        'hits': 0,
        'misses': 0,
        'hit_rate': 0,
        'miss_rate': 0,
        'average_access_time': 0,
        'total_access_time': 0,
    }

    # Test case 3: Mid-repeat blocks sequence
    print("\n3. Mid-repeat blocks sequence")
    sequence = [0]
    sequence += [i for i in range(1, n - 1)] * 2
    sequence += [x for x in range(n, (n * 2) - 1)]
    sequence *= 4
    for address in sequence:
        cache.read(address)
    cache.print_stats()



