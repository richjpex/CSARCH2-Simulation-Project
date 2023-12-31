import tkinter as tk
import random
from tkinter import ttk

class CacheSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator by Group 10 - CSARCH2 S11")

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

        # Step-by-step snapshot variables
        self.snapshot_canvas = tk.Canvas(self.root, width=400, height=150, bg="black")
        self.snapshot_canvas.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        # Text widget to display terminal output with scrollbar
        self.terminal_output_frame = tk.Frame(self.root)
        self.terminal_output_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        self.terminal_output = tk.Text(self.terminal_output_frame, height=5, width=48, wrap=tk.WORD, state=tk.DISABLED)
        self.terminal_output.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        scroll_y = tk.Scrollbar(self.terminal_output_frame, command=self.terminal_output.yview)
        scroll_y.grid(row=0, column=1, sticky='nsew')
        self.terminal_output['yscrollcommand'] = scroll_y.set

    def setup_gui(self):
        # Test case selection
        test_case_label = tk.Label(self.root, text="Select Test Case:")
        test_case_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        test_case_a_button = ttk.Radiobutton(self.root, text="Sequential Sequence", variable=self.test_case_var, value="a")
        test_case_b_button = ttk.Radiobutton(self.root, text="Random Sequence", variable=self.test_case_var, value="b")
        test_case_c_button = ttk.Radiobutton(self.root, text="Mid-repeat Sequence", variable=self.test_case_var, value="c")

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
            sequence = list(range(self.memory_blocks)) * 4
        elif self.test_case_var.get() == "b":
            if self.memory_blocks == 0:
                return None
            sequence = [random.randint(0, self.memory_blocks - 1) for _ in range(64)]
        elif self.test_case_var.get() == "c":
            n = self.memory_blocks
            for _ in range(4):
                sequence.extend(range(n - 1))
                sequence.extend(range(1, n))
                sequence.extend(range(n, 2 * n))

        # Clear the existing content in the sequence textbox
        self.terminal_output.config(state=tk.NORMAL)
        self.terminal_output.delete(1.0, tk.END)

        # Display the sequence in the GUI
        self.terminal_output.config(state=tk.NORMAL)
        self.terminal_output.insert(tk.END, str(sequence) + "\n")
        self.terminal_output.config(state=tk.DISABLED)

        return sequence

    def run_simulation(self):
        try:
            self.memory_blocks = int(self.mem_blocks_entry.get())
        except ValueError:
            self.terminal_output.config(state=tk.NORMAL)
            self.terminal_output.delete(1.0, tk.END)
            self.terminal_output.insert(tk.END, "Error: Please enter a valid number for Memory Blocks!\n")
            self.terminal_output.config(state=tk.DISABLED)
            return  # Invalid input

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

        # Display cache snapshot
        self.display_cache_snapshot()

        # Display statistics
        self.display_statistics()

        # Reset memory blocks entry
        self.mem_blocks_entry.delete(0, tk.END)

    def display_cache_snapshot(self):
        self.snapshot_canvas.delete("all")  # Clear previous drawings

        block_width = 30
        block_height = 20
        x_offset = 65
        y_offset = 40

        # Display "Final Cache Snapshot:" text
        self.snapshot_canvas.create_text(x_offset - 45, y_offset - 20, text="Final Cache Snapshot:", anchor=tk.W,
                                         fill="gold", font=("Consolas", 10, "bold"))

        non_empty_cache_sets = [(i, cache_set) for i, cache_set in enumerate(self.cache) if cache_set]

        for i, cache_set in non_empty_cache_sets:
            # Draw set label
            label_x = x_offset - 10
            label_y = y_offset + i * (block_height + 5) + block_height // 2
            self.snapshot_canvas.create_text(label_x, label_y, text=f"Set {i}", anchor=tk.E, fill="white",
                                             font=("Consolas", 10))

            for j in range(self.set_size):
                x = x_offset + j * (block_width + 10)
                y = y_offset + i * (block_height + 5)
                if j < len(cache_set):
                    address = cache_set[j]
                    self.snapshot_canvas.create_rectangle(x, y, x + block_width, y + block_height, fill="lightgreen",
                                                          outline="black")
                    self.snapshot_canvas.create_text(x + block_width // 2, y + block_height // 2, text=str(address),
                                                     font=("Consolas", 10))
                else:
                    # Empty block, indicate "N/A"
                    self.snapshot_canvas.create_rectangle(x, y, x + block_width, y + block_height, fill="gray",
                                                          outline="black")
                    self.snapshot_canvas.create_text(x + block_width // 2, y + block_height // 2, text="N/A",
                                                     font=("Consolas", 10))

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
        return (self.cache_hit_count * self.cache_lines) + self.cache_miss_count*self.cache_lines*11 + self.cache_miss_count

    def compute_average_time(self):
        total = self.cache_hit_count + self.cache_miss_count
        return self.cache_hit_count / total + (1 + self.cache_lines * 10 + 1 * self.cache_miss_count) / total


if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulator(root)
    root.resizable(width=False, height=False)
    root.mainloop()
