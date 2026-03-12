import tkinter as tk
from tkinter import ttk, messagebox
import random
from algorithms.gbfs import compute_gbfs_score
from algorithms.pso import compute_pso_score
from simulation.server_simulator import ServerSimulator
from monitoring.performance_graphs import PerformanceMonitor

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Task Offloading & Performance Monitor")
        self.root.geometry("1100x800")
        self.root.configure(bg='#121212') # Dark gray / black background

        self.simulator = ServerSimulator()
        
        # Define styles
        self.setup_styles()
        
        # Main container with two columns
        self.main_container = tk.Frame(self.root, bg='#121212', padx=10, pady=10)
        self.main_container.pack(fill='both', expand=True)
        
        self.left_col = tk.Frame(self.main_container, bg='#121212', width=400)
        self.left_col.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self.right_col = tk.Frame(self.main_container, bg='#121212')
        self.right_col.grid(row=0, column=1, sticky='nsew')
        
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Build Panels
        self.create_task_generation_panel()
        self.create_decision_engine_panel()
        self.create_server_execution_panel()
        self.create_monitoring_panel()
        self.create_logs_panel()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark theme for treeview
        style.configure("Treeview", 
                        background="#2d2d2d", 
                        foreground="white", 
                        fieldbackground="#2d2d2d", 
                        bordercolor="#444444",
                        font=('Segoe UI', 9))
        style.map("Treeview", background=[('selected', '#007acc')])
        style.configure("Treeview.Heading", background="#333333", foreground="white", bordercolor="#444444")

    def create_panel_frame(self, parent, title):
        frame = tk.LabelFrame(parent, text=title, bg='#1e1e1e', fg='white', 
                              font=('Segoe UI', 10, 'bold'), padx=10, pady=10, 
                              highlightthickness=1, highlightbackground='#444444')
        frame.pack(fill='x', pady=(0, 10))
        return frame

    def create_task_generation_panel(self):
        panel = self.create_panel_frame(self.left_col, "1. IOT TASK GENERATION PANEL")
        
        fields = [
            ("Machine ID", "MCH-001"),
            ("Temperature (°C)", "50"),
            ("CPU Load (%)", "65"),
            ("Net Latency (ms)", "25"),
            ("Power Usage (W)", "12"),
            ("Task Queue", "5")
        ]
        
        self.inputs = {}
        for i, (label_text, default_val) in enumerate(fields):
            lbl = tk.Label(panel, text=label_text + ":", bg='#1e1e1e', fg='white', anchor='w')
            lbl.grid(row=i, column=0, sticky='w', pady=5)
            
            entry = tk.Entry(panel, bg='#2d2d2d', fg='white', insertbackground='white', borderwidth=0)
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=5)
            self.inputs[label_text] = entry
            
        # Dropdown for Task Type
        tk.Label(panel, text="Task Type:", bg='#1e1e1e', fg='white', anchor='w').grid(row=6, column=0, sticky='w', pady=5)
        self.task_type = ttk.Combobox(panel, values=["Computation-Intensive", "Latency-Sensitive", "Balanced"])
        self.task_type.set("Computation-Intensive")
        self.task_type.grid(row=6, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        panel.grid_columnconfigure(1, weight=1)
        
        # Button
        btn = tk.Button(panel, text="Generate & Offload Task", bg='#007acc', fg='white', 
                        activebackground='#005999', activeforeground='white',
                        font=('Segoe UI', 10, 'bold'), command=self.on_offload_click)
        btn.grid(row=7, column=0, columnspan=2, sticky='ew', pady=(15, 5))

    def create_decision_engine_panel(self):
        panel = self.create_panel_frame(self.left_col, "2. DECISION ENGINE PANEL")
        
        self.decision_labels = {}
        fields = ["Params Summary", "GBFS Priority Score", "PSO Optimization Score", "Final Decision", "Decision Reason"]
        
        for i, text in enumerate(fields):
            lbl = tk.Label(panel, text=text + ":", bg='#1e1e1e', fg='white', font=('Segoe UI', 9))
            lbl.grid(row=i, column=0, sticky='w', pady=2)
            
            val_lbl = tk.Label(panel, text="-", bg='#1e1e1e', fg='#4ec9b0' if i < 3 else '#ff8c00', font=('Segoe UI', 9, 'bold'))
            val_lbl.grid(row=i, column=1, sticky='w', padx=10)
            self.decision_labels[text] = val_lbl

    def create_server_execution_panel(self):
        panel = self.create_panel_frame(self.left_col, "3. SERVER EXECUTION PANEL")
        
        self.execution_labels = {}
        fields = ["Selected Server", "Simulated Proc Time", "Energy Consumption"]
        
        for i, text in enumerate(fields):
            lbl = tk.Label(panel, text=text + ":", bg='#1e1e1e', fg='white', font=('Segoe UI', 9))
            lbl.grid(row=i, column=0, sticky='w', pady=2)
            
            val_lbl = tk.Label(panel, text="-", bg='#1e1e1e', fg='white', font=('Segoe UI', 9, 'bold'))
            val_lbl.grid(row=i, column=1, sticky='w', padx=10)
            self.execution_labels[text] = val_lbl
            
        self.status_bar = tk.Label(panel, text="Task Status: Idle", bg='#333333', fg='white', font=('Segoe UI', 10, 'italic'))
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(10, 0))

    def create_monitoring_panel(self):
        panel = tk.LabelFrame(self.right_col, text="4. PERFORMANCE MONITORING PANEL", 
                              bg='#1e1e1e', fg='white', font=('Segoe UI', 10, 'bold'), 
                              padx=5, pady=5, highlightthickness=1, highlightbackground='#444444')
        panel.pack(fill='both', expand=True, pady=(0, 10))
        
        self.monitor = PerformanceMonitor(panel)

    def create_logs_panel(self):
        panel = tk.Frame(self.right_col, bg='#1e1e1e')
        panel.pack(fill='x')
        
        tk.Label(panel, text="Execution Logs:", bg='#1e1e1e', fg='white', font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(0, 5))
        
        columns = ("Machine ID", "Task Type", "Server", "Latency (ms)", "Energy (W)")
        self.logs_table = ttk.Treeview(panel, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.logs_table.heading(col, text=col)
            self.logs_table.column(col, width=100)
            
        self.logs_table.pack(fill='x', expand=True)

    def on_offload_click(self):
        try:
            # 1. Read input fields
            task_params = {
                'machine_id': self.inputs["Machine ID"].get(),
                'temperature': float(self.inputs["Temperature (°C)"].get()),
                'cpu_load': float(self.inputs["CPU Load (%)"].get()),
                'net_latency': float(self.inputs["Net Latency (ms)"].get()),
                'power_usage': float(self.inputs["Power Usage (W)"].get()),
                'queue': int(self.inputs["Task Queue"].get()),
                'type': self.task_type.get()
            }
            
            self.status_bar.config(text="Task Status: Processing...", fg='#007acc')
            self.root.update_idletasks()
            
            # 2. Call algorithms
            gbfs_score = compute_gbfs_score(task_params)
            pso_score = compute_pso_score(task_params)
            
            # 3. Update Decision Panel
            self.decision_labels["Params Summary"].config(text=f"{task_params['type']} @ {task_params['machine_id']}")
            self.decision_labels["GBFS Priority Score"].config(text=str(gbfs_score))
            self.decision_labels["PSO Optimization Score"].config(text=str(pso_score))
            
            # 4. Choose server
            best_server = self.simulator.get_best_server(gbfs_score, pso_score)
            self.decision_labels["Final Decision"].config(text=best_server)
            self.decision_labels["Decision Reason"].config(text=f"Score balance: G={gbfs_score}, P={pso_score}")
            
            # 5. Simulate Execution
            execution_data = self.simulator.simulate_execution(best_server)
            
            # Update Execution Panel
            self.execution_labels["Selected Server"].config(text=execution_data['server'])
            self.execution_labels["Simulated Proc Time"].config(text=f"{execution_data['proc_time']} ms")
            self.execution_labels["Energy Consumption"].config(text=f"{execution_data['energy']} W")
            self.status_bar.config(text="Task Status: Completed", fg='#4ec9b0')
            
            # 6. Add to logs table
            self.logs_table.insert('', 0, values=(
                task_params['machine_id'],
                task_params['type'],
                execution_data['server'],
                execution_data['latency'],
                execution_data['energy']
            ))
            
            # 7. Update graphs
            metrics = {
                'latency': execution_data['latency'] + execution_data['proc_time'],
                'throughput': round(1000 / (execution_data['latency'] + execution_data['proc_time'] + 1), 2),
                'energy': execution_data['energy'],
                'utilization': random.randint(20, 90)
            }
            self.monitor.update_graphs(metrics)
            
            # Log to file (simple append)
            with open("iot_task_offloading/logs/simulation.log", "a") as f:
                f.write(f"Task: {task_params['machine_id']}, Server: {best_server}, Latency: {metrics['latency']}ms\n")

        except ValueError as e:
            messagebox.showerror("Input Error", "Please ensure all numeric fields contain valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
