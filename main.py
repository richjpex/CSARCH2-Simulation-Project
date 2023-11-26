import tkinter as tk
from tkinter import ttk, messagebox

class CacheSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator")
        self.root.geometry("400x500")

        self.cache_blocks = 0
        self.cache_line_size = 0
        self.memory_blocks = 0

        self.create_widgets()

    def create_widgets(self):
        # Labels and entry widgets for input
        self.label_cache_blocks = ttk.Label(self.root, text="Number of Cache Blocks:")
        self.entry_cache_blocks = ttk.Entry(self.root)
        self.label_cache_blocks.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_cache_blocks.grid(row=0, column=1, padx=5, pady=5)

        self.label_cache_line = ttk.Label(self.root, text="Cache Line Size (words):")
        self.entry_cache_line = ttk.Entry(self.root)
        self.label_cache_line.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_cache_line.grid(row=1, column=1, padx=5, pady=5)

        self.label_memory_blocks = ttk.Label(self.root, text="Number of Memory Blocks:")
        self.entry_memory_blocks = ttk.Entry(self.root)
        self.label_memory_blocks.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_memory_blocks.grid(row=2, column=1, padx=5, pady=5)

        # Checkbutton for step-by-step tracing
        self.step_by_step_var = tk.IntVar()
        self.step_by_step_checkbutton = ttk.Checkbutton(
            self.root, text="Step-by-Step Tracing", variable=self.step_by_step_var
        )
        self.step_by_step_checkbutton.grid(row=3, column=0, columnspan=2, pady=5)

        # Button to simulate cache
        self.simulate_button = ttk.Button(
            self.root, text="Simulate Cache", command=self.simulate_cache
        )
        self.simulate_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Output labels
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
            label.grid(row=i + 5, column=0, padx=5, pady=5, sticky="e")
            self.output_labels.append(label)

        # Text log for cache memory trace
        self.text_log = tk.Text(self.root, height=10, width=40, state=tk.DISABLED)
        self.text_log.grid(row=12, column=0, columnspan=2, pady=10)

        #TODO: add snapshot of cache memory

        # Configure column and row weights
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(12, weight=1)

    def simulate_cache(self):
        try:
            self.cache_blocks = int(self.entry_cache_blocks.get())
            self.cache_line_size = int(self.entry_cache_line.get())
            self.memory_blocks = int(self.entry_memory_blocks.get())

            # TODO: Simulation logic (replace this with actual simulation code)
            memory_access_count = 1
            cache_hit_count = 2
            cache_miss_count = 3
            cache_hit_rate = 4
            cache_miss_rate = 5
            average_memory_access_time = 6
            total_memory_access_time = 7

            # Update output labels
            self.output_labels[0]["text"] = f"Memory Access Count: {memory_access_count}"
            self.output_labels[1]["text"] = f"Cache Hit Count: {cache_hit_count}"
            self.output_labels[2]["text"] = f"Cache Miss Count: {cache_miss_count}"
            self.output_labels[3]["text"] = f"Cache Hit Rate: {cache_hit_rate:.2%}"
            self.output_labels[4]["text"] = f"Cache Miss Rate: {cache_miss_rate:.2%}"
            self.output_labels[5]["text"] = f"Average Memory Access Time: {average_memory_access_time} cycles"
            self.output_labels[6]["text"] = f"Total Memory Access Time: {total_memory_access_time} cycles"

            # Display cache memory log
            self.display_cache_log()

        except ValueError:
            # Handle invalid input
            tk.messagebox.showerror("Error", "Please enter valid numerical values.")

    def display_cache_log(self):
        # TODO: Simulation logic for cache memory log (replace this with your actual simulation code)
        cache_memory_log = self.generate_cache_log()

        # Clear existing text log
        self.text_log.config(state=tk.NORMAL)
        self.text_log.delete(1.0, tk.END)

        # Display cache memory log
        for step, log in enumerate(cache_memory_log):
            if self.step_by_step_var.get():
                self.text_log.insert(tk.END, f"Step {step + 1}:\n")
            self.text_log.insert(tk.END, log)
            self.text_log.insert(tk.END, "\n")

        # Disable text log editing
        self.text_log.config(state=tk.DISABLED)

    def generate_cache_log(self):
        # Placeholder logic for generating cache memory log
        cache_memory_log = []
        for i in range(self.memory_blocks):
            cache_memory_log.append(f"Memory Block {i + 1} in Cache: {i % self.cache_blocks + 1}")

        return cache_memory_log

    #TODO: snapshot of cache memory

if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorGUI(root)
    root.mainloop()
