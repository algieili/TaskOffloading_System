import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PerformanceMonitor:
    """
    Handles the creation and updating of performance graphs using Matplotlib.
    """
    def __init__(self, parent_frame):
        self.fig, self.axs = plt.subplots(2, 2, figsize=(6, 5))
        self.fig.patch.set_facecolor('#1e1e1e')  # Dark theme background
        
        # Data storage for segments
        self.data = {
            'latency': [],
            'throughput': [],
            'energy': [],
            'utilization': []
        }
        
        self.labels = ['Latency (ms)', 'Throughput (tps)', 'Energy (W)', 'Resource (%)']
        self.titles = ['Latency', 'Throughput', 'Energy Consumption', 'Resource Utilization']
        
        self.setup_plots()
        
        # Integration with Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def setup_plots(self):
        """Initialize plot styles and labels."""
        flat_axs = self.axs.flatten()
        for i, ax in enumerate(flat_axs):
            ax.set_facecolor('#2d2d2d')
            ax.set_title(self.titles[i], color='white', fontsize=10)
            ax.tick_params(colors='white', labelsize=8)
            for spine in ax.spines.values():
                spine.set_color('#444444')
            ax.grid(True, color='#444444', linestyle='--')

    def update_graphs(self, metrics):
        """Update data and redraw plots."""
        # Append new values
        self.data['latency'].append(metrics.get('latency', 0))
        self.data['throughput'].append(metrics.get('throughput', 0))
        self.data['energy'].append(metrics.get('energy', 0))
        self.data['utilization'].append(metrics.get('utilization', 0))
        
        # Limit data points to last 20 for visibility
        for key in self.data:
            if len(self.data[key]) > 20:
                self.data[key].pop(0)

        flat_axs = self.axs.flatten()
        colors = ['#007acc', '#4ec9b0', '#ce9178', '#c586c0']
        
        for i, key in enumerate(['latency', 'throughput', 'energy', 'utilization']):
            ax = flat_axs[i]
            ax.clear()
            self.setup_plots() # Re-apply style after clear
            ax.plot(self.data[key], color=colors[i], marker='o', markersize=3, linewidth=2)
            
        self.canvas.draw()
