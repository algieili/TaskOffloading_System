import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# Imports
from algorithms.gbfs import compute_gbfs_score
from algorithms.pso import compute_pso_score
from simulation.server_simulator import ServerSimulator
from monitoring.performance_graphs import PerformanceMonitor

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Task Offloading Decision System - Use Case Flow Prototype")
        self.root.geometry("1800x1100")
        self.root.configure(bg='#121212')
        
        self.simulator = ServerSimulator()
        self.setup_styles()
        
        self.record_counter = 0
        
        # Setup scrollable canvas for the main layout to ensure everything fits
        self.canvas = tk.Canvas(self.root, bg='#121212', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.main_container = tk.Frame(self.canvas, bg='#121212')
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.main_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        
        for i in range(4):
            self.main_container.grid_columnconfigure(i, weight=1, minsize=400)

        self.create_row1()
        self.create_row2()
        self.create_row3()
        self.create_row4()
        self.create_row5()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                        background="#2d2d2d", 
                        foreground="white", 
                        fieldbackground="#2d2d2d", 
                        bordercolor="#444444",
                        rowheight=25,
                        font=('Segoe UI', 10))
        style.map("Treeview", background=[('selected', '#007acc')])
        style.configure("Treeview.Heading", background="#333333", foreground="white", bordercolor="#444444", font=('Segoe UI', 11, 'bold'))

    def create_panel_frame(self, parent, title, bg_color='#1e1e1e', fg_color='white', border_color='#444444', expand=True):
        frame = tk.LabelFrame(parent, text=title, bg=bg_color, fg=fg_color, 
                              font=('Segoe UI', 14, 'bold'), padx=15, pady=15, 
                              highlightthickness=2, highlightbackground=border_color, bd=2)
        frame.pack(fill='both', expand=expand, pady=10, padx=10)
        return frame

    def create_row1(self):
        row_frame = tk.Frame(self.main_container, bg='#121212')
        row_frame.grid(row=0, column=0, columnspan=4, sticky='nsew', pady=5)
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=1)

        c0 = tk.Frame(row_frame, bg='#121212'); c0.grid(row=0, column=0, sticky='nsew')
        c1 = tk.Frame(row_frame, bg='#121212'); c1.grid(row=0, column=1, sticky='nsew')

        self.create_task_generation_panel(c0)
        self.create_task_offloading_eval_panel(c1)

    def create_row2(self):
        row_frame = tk.Frame(self.main_container, bg='#121212')
        row_frame.grid(row=1, column=0, columnspan=4, sticky='nsew', pady=5)
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=1)

        c0 = tk.Frame(row_frame, bg='#121212'); c0.grid(row=0, column=0, sticky='nsew')
        c1 = tk.Frame(row_frame, bg='#121212'); c1.grid(row=0, column=1, sticky='nsew')

        self.create_task_assignment_panel(c0)
        self.create_result_transmission_panel(c1)

    def create_row3(self):
        row_frame = tk.Frame(self.main_container, bg='#121212')
        row_frame.grid(row=2, column=0, columnspan=4, sticky='nsew', pady=5)
        self.create_monitoring_panel(row_frame)

    def create_row4(self):
        row_frame = tk.Frame(self.main_container, bg='#121212')
        row_frame.grid(row=3, column=0, columnspan=4, sticky='nsew', pady=5)
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=1)

        c0 = tk.Frame(row_frame, bg='#121212'); c0.grid(row=0, column=0, sticky='nsew')
        c1 = tk.Frame(row_frame, bg='#121212'); c1.grid(row=0, column=1, sticky='nsew')

        self.create_gbfs_panel(c0)
        self.create_pso_panel(c1)

    def create_row5(self):
        row_frame = tk.Frame(self.main_container, bg='#121212')
        row_frame.grid(row=4, column=0, columnspan=4, sticky='nsew', pady=5)
        self.create_logs_panel(row_frame)

    # --- ROW 1 PANELS ---

    def create_task_generation_panel(self, parent):
        panel = self.create_panel_frame(parent, "1. IOT TASK GENERATION", fg_color='white', border_color='#ffffff')
        
        self.fields = [
            ("Machine ID", "MCH-001"),
            ("Temperature (°C)", "50"),
            ("CPU Load (%)", "70"),
            ("Net Latency (ms)", "25"),
            ("Power Usage (W)", "12"),
            ("Task Queue", "5")
        ]
        
        self.inputs = {}
        input_frame = tk.Frame(panel, bg='#1e1e1e')
        input_frame.pack(fill='x', pady=5)
        
        for i, (label_text, default_val) in enumerate(self.fields):
            lbl = tk.Label(input_frame, text=label_text + ":", bg='#1e1e1e', fg='white', anchor='w', font=('Segoe UI', 11))
            lbl.grid(row=i, column=0, sticky='w', pady=4)
            entry = tk.Entry(input_frame, bg='#2d2d2d', fg='white', insertbackground='white', borderwidth=0, font=('Segoe UI', 11))
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=4)
            self.inputs[label_text] = entry
            
        tk.Label(input_frame, text="Task Type:", bg='#1e1e1e', fg='white', anchor='w', font=('Segoe UI', 11)).grid(row=6, column=0, sticky='w', pady=4)
        self.task_type = ttk.Combobox(input_frame, values=["Computation-Intensive", "Latency-Sensitive", "Balanced"], font=('Segoe UI', 11))
        self.task_type.set("Computation-Intensive")
        self.task_type.grid(row=6, column=1, sticky='ew', padx=(10, 0), pady=4)
        input_frame.grid_columnconfigure(1, weight=1)
        
        btn = tk.Button(panel, text="Generate & Offload Task", bg='#4ec9b0', fg='black', 
                        activebackground='#3da892', activeforeground='black',
                        font=('Segoe UI', 12, 'bold'), pady=8, command=self.on_offload_click)
        btn.pack(fill='x', pady=(15, 10))

        # Status Flow Display
        flow_frame = tk.LabelFrame(panel, text="Use Case Flow Status", bg='#252526', fg='#a0a0a0', font=('Segoe UI', 10, 'italic'), padx=10, pady=10)
        flow_frame.pack(fill='x', expand=True, pady=5)
        
        self.flow_labels = {}
        flow_steps = ["Task Generated", "Task Transmitted", "Algorithms Applied", "Task Assigned", "Results Transmitted"]
        for step in flow_steps:
            frame = tk.Frame(flow_frame, bg='#252526')
            frame.pack(fill='x', pady=2)
            lbl_name = tk.Label(frame, text=step, bg='#252526', fg='white', font=('Segoe UI', 11))
            lbl_name.pack(side='left')
            lbl_status = tk.Label(frame, text="Waiting...", bg='#252526', fg='#777777', font=('Segoe UI', 11, 'bold'))
            lbl_status.pack(side='right')
            self.flow_labels[step] = lbl_status

    def create_algo_panel(self, parent, title, color):
        panel = self.create_panel_frame(parent, title, fg_color=color, border_color=color)
        labels = {}
        fields = ["Score", "Estimated Latency", "Estimated Throughput", "Estimated Energy", "Resource Utilization", "Suggested Location", "Decision Time", "Remark"]
        for i, text in enumerate(fields):
            tk.Label(panel, text=text + ":", bg='#1e1e1e', fg='white', font=('Segoe UI', 11)).grid(row=i, column=0, sticky='w', pady=6)
            val_lbl = tk.Label(panel, text="-", bg='#1e1e1e', fg=color, font=('Segoe UI', 11, 'bold'))
            val_lbl.grid(row=i, column=1, sticky='w', padx=10, pady=6)
            labels[text] = val_lbl
        return labels

    def create_gbfs_panel(self, parent):
        self.gbfs_labels = self.create_algo_panel(parent, "2. GBFS EVALUATION PANEL", '#00FFFF')

    def create_pso_panel(self, parent):
        self.pso_labels = self.create_algo_panel(parent, "3. PSO EVALUATION PANEL", '#FFA500')

    def create_task_offloading_eval_panel(self, parent):
        panel = self.create_panel_frame(parent, "4. TASK OFFLOADING EVALUATION", bg_color='#252526', fg_color='#FFFF00', border_color='#FFFF00')
        
        headers = ["Metric", "GBFS", "PSO", "Better"]
        for col, text in enumerate(headers):
            tk.Label(panel, text=text, bg='#333333', fg='white', font=('Segoe UI', 10, 'bold'), pady=6, borderwidth=1, relief='solid').grid(row=0, column=col, sticky='nsew')
            
        self.comp_table_labels = {}
        metrics = ["Latency", "Throughput", "Energy", "Resource"]
        
        for row, metric in enumerate(metrics, start=1):
            tk.Label(panel, text=metric, bg='#2d2d2d', fg='white', font=('Segoe UI', 10, 'bold'), borderwidth=1, relief='solid', anchor='w', padx=5).grid(row=row, column=0, sticky='nsew')
            lbl_gbfs = tk.Label(panel, text="-", bg='#2d2d2d', fg='#00FFFF', font=('Segoe UI', 10), borderwidth=1, relief='solid')
            lbl_gbfs.grid(row=row, column=1, sticky='nsew')
            lbl_pso = tk.Label(panel, text="-", bg='#2d2d2d', fg='#FFA500', font=('Segoe UI', 10), borderwidth=1, relief='solid')
            lbl_pso.grid(row=row, column=2, sticky='nsew')
            lbl_better = tk.Label(panel, text="-", bg='#2d2d2d', fg='#00FF00', font=('Segoe UI', 10, 'bold'), borderwidth=1, relief='solid')
            lbl_better.grid(row=row, column=3, sticky='nsew')
            self.comp_table_labels[metric] = (lbl_gbfs, lbl_pso, lbl_better)
            
        for c in range(4): panel.grid_columnconfigure(c, weight=1)

        bottom_frame = tk.Frame(panel, bg='#252526')
        bottom_frame.grid(row=len(metrics)+1, column=0, columnspan=4, pady=15, sticky='ew')
        
        self.comp_bottom_labels = {}
        bottom_fields = ["Winning Algorithm", "Reason for Selection"]
        for i, f in enumerate(bottom_fields):
            tk.Label(bottom_frame, text=f+":", bg='#252526', fg='white', font=('Segoe UI', 11, 'bold')).grid(row=i, column=0, sticky='w', pady=5)
            val_lbl = tk.Label(bottom_frame, text="-", bg='#252526', fg='#4ec9b0', font=('Segoe UI', 11), wraplength=200, justify='left')
            val_lbl.grid(row=i, column=1, sticky='w', padx=10, pady=5)
            self.comp_bottom_labels[f] = val_lbl

    # --- ROW 2 PANELS ---

    def create_task_assignment_panel(self, parent):
        panel = self.create_panel_frame(parent, "5. TASK ASSIGNMENT PANEL", fg_color='#4ec9b0', border_color='#4ec9b0')
        self.assignment_labels = {}
        fields = ["Assigned Task Target", "Server Target", "Placement Reason", "Task Category", "Decision Summary"]
        for i, text in enumerate(fields):
            tk.Label(panel, text=text + ":", bg='#1e1e1e', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=i, column=0, sticky='nw', pady=8)
            val_lbl = tk.Label(panel, text="-", bg='#1e1e1e', fg='white', font=('Segoe UI', 12), wraplength=500, justify='left')
            val_lbl.grid(row=i, column=1, sticky='w', padx=15, pady=8)
            self.assignment_labels[text] = val_lbl
        panel.grid_columnconfigure(1, weight=1)

    def create_result_transmission_panel(self, parent):
        panel = self.create_panel_frame(parent, "6. RESULT TRANSMISSION PANEL", fg_color='#007acc', border_color='#007acc')
        self.transmission_labels = {}
        fields = ["Selected Processing Location", "Processing Status", "Result Transmission Status", "Network Return Status", "Final Task Status"]
        for i, text in enumerate(fields):
            tk.Label(panel, text=text + ":", bg='#1e1e1e', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=i, column=0, sticky='nw', pady=8)
            val_lbl = tk.Label(panel, text="-", bg='#1e1e1e', fg='#cccccc', font=('Segoe UI', 12), wraplength=500, justify='left')
            val_lbl.grid(row=i, column=1, sticky='w', padx=15, pady=8)
            self.transmission_labels[text] = val_lbl
        panel.grid_columnconfigure(1, weight=1)

    # --- ROW 3: CHARTS ---

    def create_monitoring_panel(self, parent):
        panel = tk.LabelFrame(parent, text="7. PERFORMANCE MONITORING PANEL", bg='#1e1e1e', fg='white', font=('Segoe UI', 14, 'bold'), padx=15, pady=15, highlightthickness=2, highlightbackground='#444444')
        panel.pack(fill='both', expand=True, pady=(0, 15), padx=10)
        self.monitor = PerformanceMonitor(panel)

    # --- ROW 4: LOGS ---

    def create_logs_panel(self, parent):
        panel = tk.Frame(parent, bg='#1e1e1e')
        panel.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        tk.Label(panel, text="8. EXECUTION LOGS", bg='#1e1e1e', fg='white', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 10))
        
        columns = ("Record No.", "Machine ID", "Task Type", "GBFS Latency", "PSO Latency", "GBFS Energy", "PSO Energy", "Winner", "Assigned Server", "Placement Reason", "Final Status")
        self.logs_table = ttk.Treeview(panel, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.logs_table.heading(col, text=col)
            width = 80 if col in ("Record No.", "Winner", "Assigned Server") else 110
            if col == "Placement Reason": width = 250
            if col == "Final Status": width = 120
            self.logs_table.column(col, width=width)
            
        scroll = ttk.Scrollbar(panel, orient="vertical", command=self.logs_table.yview)
        scroll.pack(side="right", fill="y")
        self.logs_table.configure(yscrollcommand=scroll.set)
        self.logs_table.pack(fill='both', expand=True)

    # --- LOGIC ---

    def update_flow_status(self, step, status="Done", color="#00FF00"):
        if step in self.flow_labels:
            self.flow_labels[step].config(text=status, fg=color)
            self.root.update_idletasks()

    def reset_flow_status(self):
        for step, lbl in self.flow_labels.items():
            lbl.config(text="Waiting...", fg="#777777")
        self.root.update_idletasks()

    def set_transmission_status(self, p_loc, p_stat, r_trans, n_ret, f_stat):
        self.transmission_labels["Selected Processing Location"].config(text=p_loc, fg='#00FFFF' if 'Edge' in p_loc else '#C586C0')
        self.transmission_labels["Processing Status"].config(text=p_stat, fg='#00FF00' if 'Complete' in p_stat else '#ffffff')
        self.transmission_labels["Result Transmission Status"].config(text=r_trans, fg='#00FF00' if 'Complete' in r_trans else '#ffffff')
        self.transmission_labels["Network Return Status"].config(text=n_ret, fg='#00FF00' if 'Confirmed' in n_ret else '#ffffff')
        self.transmission_labels["Final Task Status"].config(text=f_stat, fg='#4ec9b0')

    def get_form_values(self):
        v = {}
        for k, e in self.inputs.items():
            v[k] = e.get()
        v["Task Type"] = self.task_type.get()
        return v

    def on_offload_click(self):
        try:
            params = self.get_form_values()
            self.reset_flow_status()
            
            # Step 1: Generate Task
            self.update_flow_status("Task Generated", "Processing...", "#FFFF00")
            time.sleep(0.1)
            self.update_flow_status("Task Generated", "Done", "#00FF00")
            
            # Step 2: Transmit Task
            self.update_flow_status("Task Transmitted", "Transmitting...", "#FFFF00")
            time.sleep(0.2)
            self.update_flow_status("Task Transmitted", "Transmitted", "#00FF00")

            # Step 3 & 4: Apply Algorithms
            self.update_flow_status("Algorithms Applied", "Evaluating...", "#FFFF00")
            gbfs_res = compute_gbfs_score(params)
            pso_res = compute_pso_score(params)
            self.update_algo_panel_vals(self.gbfs_labels, gbfs_res)
            self.update_algo_panel_vals(self.pso_labels, pso_res)
            self.root.update()
            time.sleep(0.2)
            self.update_flow_status("Algorithms Applied", "Evaluated", "#00FF00")
            
            # Step 5: Evaluate Decision
            winner, server, placement_reason, w_data = self.run_task_offloading_eval(params, gbfs_res, pso_res)

            # Step 6: Assign Task
            self.update_flow_status("Task Assigned", "Assigning...", "#FFFF00")
            self.assignment_labels["Assigned Task Target"].config(text=params.get("Machine ID"), fg='#ffffff')
            self.assignment_labels["Server Target"].config(text=f"{server} Server", fg='#00FFFF' if server=='Edge' else '#C586C0')
            self.assignment_labels["Placement Reason"].config(text=placement_reason)
            self.assignment_labels["Task Category"].config(text=params.get("Task Type"))
            self.assignment_labels["Decision Summary"].config(text=f"{winner} assigned task to {server} Server.")
            time.sleep(0.2)
            self.update_flow_status("Task Assigned", "Assigned", "#00FF00")

            # Step 7 & 8: Process & Transmit Results
            self.update_flow_status("Results Transmitted", "Processing...", "#FFFF00")
            
            self.set_transmission_status(
                p_loc=f"Process Task at {server}",
                p_stat="Processing...",
                r_trans="Pending",
                n_ret="Pending",
                f_stat="In Progress"
            )
            self.root.update()
            time.sleep(0.3)
            
            self.set_transmission_status(
                p_loc=f"Process Task at {server}",
                p_stat="Processing Complete",
                r_trans="Transmitting via Network...",
                n_ret="Waiting...",
                f_stat="In Progress"
            )
            self.root.update()
            time.sleep(0.2)
            
            self.set_transmission_status(
                p_loc=f"Process Task at {server}",
                p_stat="Processing Complete",
                r_trans="Transmission Complete",
                n_ret="Confirmed",
                f_stat="Task Successfully Offloaded & Returned"
            )
            self.update_flow_status("Results Transmitted", "Received", "#00FF00")

            # Step 9 & 10: Monitor and Log
            self.monitor.update_graphs(gbfs_res, pso_res)
            
            self.record_counter += 1
            self.logs_table.insert('', 0, values=(
                self.record_counter, params.get("Machine ID"), params.get("Task Type"),
                f"{gbfs_res['latency']:.2f}", f"{pso_res['latency']:.2f}", 
                f"{gbfs_res['energy']:.2f}", f"{pso_res['energy']:.2f}",
                winner, server, placement_reason, "Success"
            ))
            
            # Auto scroll down to view results
            self.canvas.yview_moveto(0.3)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process: {e}")
            self.reset_flow_status()

    def update_algo_panel_vals(self, labels, res):
        labels["Score"].config(text=str(res.get('score', '-')))
        labels["Estimated Latency"].config(text=f"{res.get('latency', '-')} ms")
        labels["Estimated Throughput"].config(text=f"{res.get('throughput', '-')} tps")
        labels["Estimated Energy"].config(text=f"{res.get('energy', '-')} W")
        labels["Resource Utilization"].config(text=f"{res.get('utilization', '-')} %")
        labels["Suggested Location"].config(text=res.get('location', '-'))
        labels["Decision Time"].config(text=res.get('time', '-'))
        labels["Remark"].config(text=res.get('remark', '-'))

    def run_task_offloading_eval(self, params, gbfs, pso):
        task_type = params.get("Task Type", "Balanced")
        
        def compare(metric, g, p, lower_is_better=True):
            if lower_is_better: return "GBFS" if g < p else "PSO"
            return "GBFS" if g > p else "PSO"

        b_lat = compare("Latency", gbfs['latency'], pso['latency'], True)
        b_thr = compare("Throughput", gbfs['throughput'], pso['throughput'], False)
        b_eng = compare("Energy", gbfs['energy'], pso['energy'], True)
        b_utl = compare("Resource", gbfs['utilization'], pso['utilization'], True)

        self.update_comp_row("Latency", f"{gbfs['latency']} ms", f"{pso['latency']} ms", b_lat)
        self.update_comp_row("Throughput", f"{gbfs['throughput']} tps", f"{pso['throughput']} tps", b_thr)
        self.update_comp_row("Energy", f"{gbfs['energy']} W", f"{pso['energy']} W", b_eng)
        self.update_comp_row("Resource", f"{gbfs['utilization']} %", f"{pso['utilization']} %", b_utl)

        # Winning Logic
        if task_type == "Latency-Sensitive":
            winner = b_lat
            reason = f"{winner} achieved better latency ({gbfs['latency'] if winner=='GBFS' else pso['latency']} ms)"
            server = "Edge"
        elif task_type == "Computation-Intensive":
            winner = b_thr
            reason = f"{winner} achieved higher throughput for computation"
            server = "Cloud"
        else:
            winner = b_eng
            reason = f"{winner} proved more energy efficient"
            server = "Cloud" if pso['utilization'] > 80 else "Edge"
            
        winning_algo_data = gbfs if winner == "GBFS" else pso
        server = winning_algo_data['location']

        self.comp_bottom_labels["Winning Algorithm"].config(text=winner, fg='#00FFFF' if winner=='GBFS' else '#FFA500')
        self.comp_bottom_labels["Reason for Selection"].config(text=reason)
        
        return winner, server, reason, winning_algo_data

    def update_comp_row(self, metric, g_val, p_val, better):
        lbl_g, lbl_p, lbl_b = self.comp_table_labels[metric]
        lbl_g.config(text=g_val)
        lbl_p.config(text=p_val)
        lbl_b.config(text=better, fg='#00FFFF' if better=='GBFS' else '#FFA500')
