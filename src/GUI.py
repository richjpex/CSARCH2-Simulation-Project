import random
import tkinter as tk
from tkinter import ttk
from src.Simulation import CacheSimulator

class CacheSimulatorGUI:
    def __init__(self, root):
        # Initialize the GUI window
        self.root = root
        self.root.title("Cache Simulator")

        # GUI elements for memory blocks input
        self.memory_block_label = ttk.Label(root, text="Number of Memory Blocks:")
        self.memory_block_entry = ttk.Entry(root)
        self.memory_block_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.memory_block_entry.grid(row=2, column=1, padx=5, pady=5)


        self.test_case_label = ttk.Label(root, text="Test Cases:")
        self.test_case_values = ['Sequential', 'Random', 'Mid-Repeating']
        self.selected_test_case = tk.StringVar(value=self.test_case_values[0])  # Set default value
        for i, test_case in enumerate(self.test_case_values):
            row_position = i + 3  # Start from row 3 and alternate every 2 radio buttons
            radio_button = ttk.Radiobutton(root, text=test_case, variable=self.selected_test_case, value=test_case)
            radio_button.grid(row=row_position, column=0, padx=5, pady=5, sticky="w")
        
        # Checkbox for step-by-step tracing
        self.step_by_step_var = tk.IntVar()
        self.step_by_step_checkbutton = ttk.Checkbutton(
            self.root, text="Step-by-Step Tracing", variable=self.step_by_step_var
        )
        self.step_by_step_checkbutton.grid(row=6, column=0, columnspan=2, pady=5)

        # Button to start cache simulation
        self.start_button = ttk.Button(
            self.root, text="Simulate Cache", command=self.start_simulation
        )
        self.start_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Cache simulator instance
        self.cache_simulator = None

        # Labels for simulation results
        self.output_labels = []
        labels_text = [
            "Memory Access Count:",
            "Cache Hit Count:",
            "Cache Miss Count:",
            "Cache Hit Rate:",
            "Cache Miss Rate:",
            "Average Memory Access Time:",
            "Total Memory Access Time:",
        ]
        for i, label_text in enumerate(labels_text):
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=i + 8, column=0, padx=5, pady=5, sticky="e")
            self.output_labels.append(label)

        # Text area for cache simulation log
        self.text_log = tk.Text(self.root, height=10, width=40, state=tk.DISABLED)
        self.text_log.grid(row=15, column=0, columnspan=2, pady=10)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(15, weight=1)

        # Initialize memory access sequence and cache block counts
        self.memory_access_sequence = []
        self.memory_blocks = 0
        self.cache_blocks = 0

    def start_simulation(self):
        try:

            selected_test_case = self.selected_test_case.get()

            # Get the number of memory blocks from the user input
            memory_block = int(self.memory_block_entry.get())
            self.memory_blocks = memory_block

            # Initialize the cache simulator
            self.cache_simulator = CacheSimulator()
            self.cache_blocks = 32 # the default 

                # Generate a random memory access sequence
            memory_access_sequence = [
                random.randint(0, 2 * (memory_block // 2) - 1) for _ in range(4 * (memory_block // 2))
            ]
            self.memory_access_sequence = memory_access_sequence
                
            if selected_test_case == 'Sequential': 
                #up to 2n Cache blocks, repeat four times without refreshin or something
                pass

            elif selected_test_case == 'Random':
                #4n Cache block?
                self.cache_blocks *= 4

                #put in logic for repeating four times inside
                results = self.cache_simulator.run_simulation(memory_access_sequence)
                pass

            elif selected_test_case == 'Mid-Repeating':
                # start at 0, then repeat middle sequence to n-1 blocks, then contunue to 2n, then repeat 4 times.
                # ie. n=8 == 0, 1,2,3,4,5,6, 1,2,3,4,5,6, 7,8,9,10,11,12,13,14,15 {4x}
                pass

            # Update the GUI labels with simulation results
            self.output_labels[0]["text"] = f"Memory Access Count: {results['hits'] + results['misses']}"
            self.output_labels[1]["text"] = f"Cache Hit Count: {results['hits']}"
            self.output_labels[2]["text"] = f"Cache Miss Count: {results['misses']}\n"
            self.output_labels[3]["text"] = f"Cache Hit Rate: {results['cache_hit_rate']:.2%}"
            self.output_labels[4]["text"] = f"Cache Miss Rate: {results['cache_miss_rate']:.2%}"
            self.output_labels[5]["text"] = f"Average Memory Access Time: {results['average_memory_access_time']:.2f}"
            self.output_labels[6]["text"] = f"Total Memory Access Time: {results['total_memory_access_time']:.2f}"

            # Display the cache simulation log
            self.display_cache_log()

        except ValueError as e:
            # Handle the case where the user enters invalid input
            pass

    def display_cache_log(self):
        # TODO: Simulation logic for cache memory log (replace this with your actual simulation code)
        # Display the cache simulation log in the text area
        cache_memory_log = self.generate_cache_log()
        self.text_log.config(state=tk.NORMAL)
        self.text_log.delete(1.0, tk.END)

        for step, log in enumerate(cache_memory_log):
            if self.step_by_step_var.get():
                self.text_log.insert(tk.END, f"Step {step + 1}:\n")
            self.text_log.insert(tk.END, log)
            self.text_log.insert(tk.END, "\n")
        self.text_log.config(state=tk.DISABLED)

    def generate_cache_log(self):
        # Generate the cache simulation log
        cache_memory_log = []
        for i, memory_address in enumerate(self.memory_access_sequence):
            cache_block = (memory_address // self.cache_simulator.block_size) % self.cache_blocks + 1
            cache_memory_log.append(f"Memory Address Block {memory_address} in Cache: {i % self.cache_blocks + 1}")

        return cache_memory_log

    # TODO: snapshot of cache memory
