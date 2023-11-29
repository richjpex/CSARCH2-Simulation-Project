import random

class Cache:
    def __init__(self, blocks=32, line=16, sets=8):
        self.blocks = blocks
        self.line = line
        self.sets = sets
        self.cache = [[[-1 for _ in range(line)] for _ in range(sets)] for _ in range(blocks)]
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
        block = address % self.blocks
        self.stats['accesses'] += 1
        for i in range(self.sets):
            for j in range(self.line):
                if self.cache[block][i][j] == address:
                    self.stats['hits'] += 1
                    return
        self.stats['misses'] += 1
        index = self.pointer % self.blocks
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
        print(f'Average memory access time: {self.stats["average_access_time"]:.2f}')
        print(f'Total memory access time: {self.stats["total_access_time"]}')

if __name__ == '__main__':
    n = int(input('Enter the number of memory blocks: '))
    cache = Cache()
    for i in range(n * 4):
        address = random.randint(0, cache.blocks * cache.line - 1)
        cache.read(address)
        cache.stats['total_access_time'] += 1
    cache.print_stats()