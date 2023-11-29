import tkinter as tk
import random
from tkinter import ttk

class CacheSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator")

        # GUI components
        self.test_case_var = tk.StringVar()
        self.test_case_var.set("a")
        self.setup_gui()

        # Cache parameters
        self.cache_blocks = 32
        self.cache_lines = 16
        self.set_size = 8  # 8-way set-associative cache
        self.memory_blocks = 0

        # Simulation variables
        self.cache = [[] for _ in range(self.cache_blocks)]
        self.access_sequence = []

        # Statistics
        self.memory_access_count = 0
        self.cache_hit_count = 0
        self.cache_miss_count = 0

    def setup_gui(self):
        # Test case selection
        test_case_label = tk.Label(self.root, text="Select Test Case:")
        test_case_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        test_case_a_button = ttk.Radiobutton(self.root, text="Test Case A", variable=self.test_case_var, value="a")
        test_case_b_button = ttk.Radiobutton(self.root, text="Test Case B", variable=self.test_case_var, value="b")
        test_case_c_button = ttk.Radiobutton(self.root, text="Test Case C", variable=self.test_case_var, value="c")

        test_case_a_button.grid(row=0, column=1, padx=10, pady=10)
        test_case_b_button.grid(row=0, column=2, padx=10, pady=10)
        test_case_c_button.grid(row=0, column=3, padx=10, pady=10)

        # Memory blocks input
        mem_blocks_label = tk.Label(self.root, text="Enter Memory Blocks:")
        mem_blocks_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.mem_blocks_entry = tk.Entry(self.root)
        self.mem_blocks_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        run_button = tk.Button(self.root, text="Run Simulation", command=self.run_simulation)
        run_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Statistics
        stats_label = tk.Label(self.root, text="Simulation Statistics:")
        stats_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        self.stats_text = tk.Text(self.root, height=10, width=50, state=tk.DISABLED)
        self.stats_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    def generate_test_case(self):
        n = self.cache_blocks // self.set_size  # Number of sets
        sequence = []

        if self.test_case_var.get() == "a":
            for _ in range(4):
              sequence = list(range(n * self.cache_lines))
        elif self.test_case_var.get() == "b":
            if self.memory_blocks == 0:
                return None
            for _ in range(4 * self.memory_blocks):
                sequence.append(random.randint(0, self.memory_blocks - 1))
        elif self.test_case_var.get() == "c":
          n = self.memory_blocks
          for _ in range(4):
              sequence.extend(range(n))
              sequence.extend(range(1, n-1))
              sequence.extend(range(n, 2 * n))

        print(sequence)
        return sequence

    def run_simulation(self):
        self.memory_blocks = int(self.mem_blocks_entry.get())
        self.access_sequence = self.generate_test_case()

        if self.access_sequence is None:
            return  # Invalid test case

        # Reset simulation variables
        self.cache = [[] for _ in range(self.cache_blocks)]
        self.memory_access_count = 0
        self.cache_hit_count = 0
        self.cache_miss_count = 0

        # Simulate cache access
        for address in self.access_sequence:
            self.memory_access_count += 1
            set_index = address % (self.cache_blocks // self.set_size)
            
            if address in self.cache[set_index]:
                self.cache_hit_count += 1
            else:
                self.cache_miss_count += 1
                # FIFO Replacement
                if len(self.cache[set_index]) == self.set_size:
                    self.cache[set_index].pop(0)
                self.cache[set_index].append(address)

        # Display statistics
        self.display_statistics()

    def display_statistics(self):
        hit_rate = self.cache_hit_count / self.memory_access_count * 100 if self.memory_access_count > 0 else 0
        miss_rate = self.cache_miss_count / self.memory_access_count * 100 if self.memory_access_count > 0 else 0
        avg_access_time = self.compute_average_time()
        total_access_time = self.compute_total_time()

        stats_info = f"Memory Access Count: {self.memory_access_count}\n" \
                    f"Cache Hit Count: {self.cache_hit_count}\n" \
                    f"Cache Miss Count: {self.cache_miss_count}\n" \
                    f"Cache Hit Rate: {hit_rate:.2f}%\n" \
                    f"Cache Miss Rate: {miss_rate:.2f}%\n" \
                    f"Average Memory Access Time: {avg_access_time:.2f} ns\n" \
                    f"Total Memory Access Time: {total_access_time:.2f} ns"

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_info)
        self.stats_text.config(state=tk.DISABLED)

    def compute_total_time(self):
        return self.cache_hit_count + self.cache_miss_count * (10)
    
    def compute_average_time(self):
        total_time = self.cache_hit_count + self.cache_miss_count * (10)
        total = self.cache_hit_count + self.cache_miss_count
        return total_time / total
    


if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulator(root)
    root.mainloop()