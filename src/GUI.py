import random
import tkinter as tk
from tkinter import ttk
from src.Simulation import CacheSimulator

class CacheSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator")

        self.memory_block_label = ttk.Label(root, text="Number of Memory Blocks:")
        self.memory_block_entry = ttk.Entry(root)
        self.memory_block_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.memory_block_entry.grid(row=2, column=1, padx=5, pady=5)

        self.step_by_step_var = tk.IntVar()
        self.step_by_step_checkbutton = ttk.Checkbutton(
            self.root, text="Step-by-Step Tracing", variable=self.step_by_step_var
        )
        self.step_by_step_checkbutton.grid(row=3, column=0, columnspan=2, pady=5)

        self.start_button = ttk.Button(
            self.root, text="Simulate Cache", command=self.start_simulation
        )
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.cache_simulator = None

        self.output_labels = []
        labels_text = [
            "Block Size:",
            "Cache Hit Count:",
            "Cache Miss Count:",
            "Cache Hit Rate:",
            "Cache Miss Rate:",
            "Average Memory Access Time:",
            "Total Memory Access Time:",
        ]
        for i, label_text in enumerate(labels_text):
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=i + 5, column=0, padx=5, pady=5, sticky="e")
            self.output_labels.append(label)

        self.text_log = tk.Text(self.root, height=10, width=40, state=tk.DISABLED)
        self.text_log.grid(row=12, column=0, columnspan=2, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(12, weight=1)

        self.memory_access_sequence = []
        self.memory_blocks = 0
        self.cache_blocks = 0

    def start_simulation(self):
        try:
            memory_block = int(self.memory_block_entry.get())
            self.memory_blocks = memory_block
            self.cache_simulator = CacheSimulator()
            self.cache_blocks = 32
            memory_access_sequence = [
                random.randint(0, 2 * (memory_block // 2) - 1) for _ in range(4 * (memory_block // 2))
            ]
            self.memory_access_sequence = memory_access_sequence
            results = self.cache_simulator.run_simulation(memory_access_sequence)
            self.output_labels[0]["text"] = f"Block Size (n): {32 // memory_block}"
            self.output_labels[1]["text"] = f"Cache Hit Count: {results['hits']}"
            self.output_labels[2]["text"] = f"Cache Miss Count: {results['misses']}\n"
            self.output_labels[3]["text"] = f"Cache Hit Rate: {results['cache_hit_rate']:.2%}"
            self.output_labels[4]["text"] = f"Cache Miss Rate: {results['cache_miss_rate']:.2%}"
            self.output_labels[5]["text"] = f"Average Memory Access Time: {results['average_memory_access_time']:.2f}"
            self.output_labels[6]["text"] = f"Total Memory Access Time: {results['total_memory_access_time']:.2f}"
            self.display_cache_log()

        except ValueError as e:
            pass

    def display_cache_log(self):
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
        cache_memory_log = []
        for i, memory_address in enumerate(self.memory_access_sequence):
            cache_block = (memory_address // self.memory_blocks) % self.cache_blocks + 1
            cache_memory_log.append(f"Memory Address Block {memory_address} in Cache: {i % self.cache_blocks + 1}")

        return cache_memory_log

