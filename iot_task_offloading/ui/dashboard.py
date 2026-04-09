import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# Imports
from algorithms.gbfs import compute_gbfs_score
from algorithms.pso import compute_pso_score
from simulation.server_simulator import ServerSimulator
from monitoring.performance_graphs import PerformanceMonitor

# Modern Theme Colors
BG_COLOR = "#0b1121"
SIDEBAR_BG = "#0f172a"
CARD_BG = "#1e293b"
CARD_BORDER = "#334155"
TEXT_MAIN = "#f8fafc"
TEXT_MUTED = "#94a3b8"
CYAN = "#00e5ff"       # GBFS / Edge
MAGENTA = "#ec4899"    # PSO
YELLOW = "#fbbf24"
GREEN = "#10b981"
DARK_GREEN = "#064e3b"

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Offloading Simulation System")
        self.root.geometry("1800x1000")
        self.root.configure(bg=BG_COLOR)
        
        self.simulator = ServerSimulator()
        self.setup_styles()
        self.record_counter = 0

        # Main Layout: Sidebar (Left) + Content (Right)
        self.sidebar_frame = tk.Frame(self.root, bg=SIDEBAR_BG, width=280)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        self.content_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.target_widgets = {}

        self.build_sidebar()
        self.build_content_area()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                        background=CARD_BG, 
                        foreground=TEXT_MAIN, 
                        fieldbackground=CARD_BG, 
                        bordercolor=CARD_BORDER,
                        rowheight=28,
                        font=('Segoe UI', 10))
        style.map("Treeview", background=[('selected', '#3b82f6')])
        style.configure("Treeview.Heading", background=SIDEBAR_BG, foreground=TEXT_MAIN, bordercolor=CARD_BORDER, font=('Segoe UI', 11, 'bold'))
        
        # Rounded/Flat combobox style
        style.configure("TCombobox", fieldbackground=SIDEBAR_BG, background=SIDEBAR_BG, foreground=TEXT_MAIN, bordercolor=CARD_BORDER, darkcolor=CARD_BORDER, lightcolor=CARD_BORDER)
        self.root.option_add('*TCombobox*Listbox.background', SIDEBAR_BG)
        self.root.option_add('*TCombobox*Listbox.foreground', TEXT_MAIN)
        self.root.option_add('*TCombobox*Listbox.selectBackground', CARD_BG)
        self.root.option_add('*TCombobox*Listbox.selectForeground', CYAN)

    def build_sidebar(self):
        # Logo/Title area
        logo_frame = tk.Frame(self.sidebar_frame, bg=SIDEBAR_BG)
        logo_frame.pack(fill="x", pady=40, padx=10)
        
        tk.Label(logo_frame, text="Task Offloading\nSimulation System", 
                 font=('Segoe UI', 15, 'bold'), fg=CYAN, bg=SIDEBAR_BG, justify='center').pack()

        nav_items = [
            ("System Overview", "overview_panel"),
            ("Operational Metrics", "metrics_panel"),
            ("GBFS Evaluation", "gbfs_panel"),
            ("PSO Evaluation", "pso_panel"),
            ("Task Offloading Evaluation", "offloading_panel"),
            ("Task Assignment", "assignment_panel"),
            ("Result Transmission", "transmission_panel"),
            ("Performance Monitoring", "monitoring_panel"),
            ("Execution Logs", "logs_panel")
        ]
        
        self.nav_buttons = {}
        for text, p_id in nav_items:
            bg = SIDEBAR_BG
            fg = TEXT_MUTED
            btn = tk.Button(self.sidebar_frame, text=f"  {text}", bg=bg, fg=fg, 
                            font=('Segoe UI', 11, 'bold'), anchor="w", bd=0, 
                            activebackground=CARD_BG, activeforeground=TEXT_MAIN, 
                            relief="flat", padx=20, pady=10, 
                            command=lambda name=p_id: self.scroll_to_panel(name))
            btn.pack(fill="x", pady=2)
            self.nav_buttons[p_id] = btn

    def animate_scroll(self, current_fraction, target_fraction, steps, current_step=0):
        if current_step <= steps:
            progress = current_step / steps
            ease = 1 - pow(1 - progress, 3) # Cubic ease-out
            new_fraction = current_fraction + (target_fraction - current_fraction) * ease
            self.canvas.yview_moveto(new_fraction)
            self.root.after(16, self.animate_scroll, current_fraction, target_fraction, steps, current_step + 1)
        else:
            self.canvas.yview_moveto(target_fraction)

    def scroll_to_panel(self, panel_id):
        for name, btn in self.nav_buttons.items():
            if name == panel_id:
                btn.config(bg="#1e293b", fg=CYAN)
            else:
                btn.config(bg=SIDEBAR_BG, fg=TEXT_MUTED)
                
        if getattr(self, 'target_widgets', None) and panel_id in self.target_widgets:
            widget = self.target_widgets[panel_id]
            self.root.update_idletasks()
            y = widget.winfo_rooty() - self.main_container.winfo_rooty()
            y -= 20 # small margin
            target_fraction = y / self.main_container.winfo_height()
            current_fraction = self.canvas.yview()[0]
            self.animate_scroll(current_fraction, target_fraction, steps=25)

    def build_content_area(self):
        # Scrollable Canvas
        self.canvas = tk.Canvas(self.content_frame, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.main_container = tk.Frame(self.canvas, bg=BG_COLOR, padx=20, pady=20)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.main_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        for i in range(4):
            self.main_container.grid_columnconfigure(i, weight=1, minsize=350)

        self.create_row1()
        self.create_row2()
        self.create_row3()
        self.create_row4()
        self.create_row5()
        self.create_row6()

    def create_card_frame(self, parent, title, title_color=CYAN):
        border_frame = tk.Frame(parent, bg=CARD_BORDER, padx=1, pady=1)
        card = tk.Frame(border_frame, bg=CARD_BG, padx=20, pady=20)
        card.pack(fill='both', expand=True)
        
        header_frame = tk.Frame(card, bg=CARD_BG)
        header_frame.pack(fill='x', pady=(0, 15))
        tk.Label(header_frame, text=title, bg=CARD_BG, fg=title_color, font=('Segoe UI', 14, 'bold')).pack(side='left')
        
        return border_frame, card

    def create_row1(self):
        row = tk.Frame(self.main_container, bg=BG_COLOR)
        row.pack(fill="x", pady=10)
        row.grid_columnconfigure(0, weight=1)

        c0 = tk.Frame(row, bg=BG_COLOR); c0.grid(row=0, column=0, sticky='nsew', padx=10)
        self.create_process_flow_card(c0)

    def create_row2(self):
        row = tk.Frame(self.main_container, bg=BG_COLOR)
        row.pack(fill="x", pady=10)
        row.grid_columnconfigure(0, weight=6)
        row.grid_columnconfigure(1, weight=4)

        c0 = tk.Frame(row, bg=BG_COLOR); c0.grid(row=0, column=0, sticky='nsew', padx=10)
        c1 = tk.Frame(row, bg=BG_COLOR); c1.grid(row=0, column=1, sticky='nsew', padx=10)

        self.create_machine_metrics_card(c0)
        self.create_decision_card(c1)

    def create_row3(self):
        row = tk.Frame(self.main_container, bg=BG_COLOR)
        row.pack(fill="x", pady=10)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)
        row.grid_columnconfigure(2, weight=1)

        c0 = tk.Frame(row, bg=BG_COLOR); c0.grid(row=0, column=0, sticky='nsew', padx=10)
        c1 = tk.Frame(row, bg=BG_COLOR); c1.grid(row=0, column=1, sticky='nsew', padx=10)
        c2 = tk.Frame(row, bg=BG_COLOR); c2.grid(row=0, column=2, sticky='nsew', padx=10)

        self.create_gbfs_card(c0)
        self.create_pso_card(c1)
        self.create_offloading_eval_card(c2)

    def create_row4(self):
        row = tk.Frame(self.main_container, bg=BG_COLOR)
        row.pack(fill="x", pady=10)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        c0 = tk.Frame(row, bg=BG_COLOR); c0.grid(row=0, column=0, sticky='nsew', padx=10)
        c1 = tk.Frame(row, bg=BG_COLOR); c1.grid(row=0, column=1, sticky='nsew', padx=10)

        self.create_assignment_card(c0)
        self.create_transmission_card(c1)

    def create_row5(self):
        row = tk.Frame(self.main_container, bg=BG_COLOR)
        row.pack(fill="both", expand=True, pady=10)
        c0 = tk.Frame(row, bg=BG_COLOR); c0.pack(fill="both", expand=True, padx=10)
        self.create_monitoring_card(c0)

    def create_row6(self):
        row = tk.Frame(self.main_container, bg=BG_COLOR)
        row.pack(fill="both", expand=True, pady=10)
        c0 = tk.Frame(row, bg=BG_COLOR); c0.pack(fill="both", expand=True, padx=10)
        self.create_logs_card(c0)

    # --- ROW 1: SYSTEM FLOW ---
    def create_process_flow_card(self, parent):
        border, card = self.create_card_frame(parent, "SYSTEM FLOW", TEXT_MAIN)
        border.pack(fill='both', expand=True)
        self.target_widgets["overview_panel"] = border

        self.flow_labels = {}
        steps = ["Data Input & Generation", "Algorithms Applied", "Decision Evaluated", "Task Processed", "Execution Completed"]
        
        flow_container = tk.Frame(card, bg=CARD_BG)
        flow_container.pack(fill='x', expand=True, pady=10)
        
        for i, step in enumerate(steps):
            frame = tk.Frame(flow_container, bg=CARD_BG)
            frame.pack(side='left', expand=True)
            
            # Dot indicator
            dot = tk.Label(frame, text="●", bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 18))
            dot.pack(side='left', padx=(0,10))
            lbl = tk.Label(frame, text=step, bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 12, 'bold'))
            lbl.pack(side='left')
            self.flow_labels[step] = (dot, lbl)
            
            if i < len(steps) - 1:
                arrow = tk.Label(flow_container, text="      ❯      ", bg=CARD_BG, fg=CARD_BORDER, font=('Segoe UI', 14))
                arrow.pack(side='left')

    # --- ROW 2: METRICS & DECISION ---
    def create_machine_metrics_card(self, parent):
        border, card = self.create_card_frame(parent, "OPERATIONAL METRICS", CYAN)
        border.pack(fill='both', expand=True)
        self.target_widgets["metrics_panel"] = border
        
        grid_frame = tk.Frame(card, bg=CARD_BG)
        grid_frame.pack(fill='x', expand=True)

        tk.Label(grid_frame, text="Specific Machine", bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=8)
        self.machine_var = tk.StringVar()
        self.machine_cb = ttk.Combobox(grid_frame, textvariable=self.machine_var, values=[
            "Select Machine", "CNC Milling Machine", "Arc Welding Machine", "Plasma Cutting Machine", "Conveyor Systems", "Electro-Deposition Coating System"
        ], font=('Segoe UI', 12), state="readonly", width=35)
        self.machine_cb.grid(row=0, column=1, sticky='ew', padx=15, pady=8)
        
        tk.Label(grid_frame, text="Machine Category", bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=8)
        self.category_var = tk.StringVar()
        
        # Style category exactly like combobox without arrow
        cat_frame = tk.Frame(grid_frame, bg=SIDEBAR_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        cat_frame.grid(row=1, column=1, sticky='ew', padx=15, pady=8)
        tk.Entry(cat_frame, textvariable=self.category_var, bg=SIDEBAR_BG, fg=TEXT_MAIN, readonlybackground=SIDEBAR_BG, borderwidth=0, font=('Segoe UI', 12), state="readonly").pack(fill='x', padx=5, pady=2)
        
        # Dynamic inputs frame
        self.dynamic_metrics_frame = tk.Frame(grid_frame, bg=CARD_BG)
        self.dynamic_metrics_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(15, 5))
        self.dynamic_metrics_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        self.dynamic_inputs = {}
        
        self.auto_task_type_var = tk.StringVar(value="Computation-Intensive")
        self.machine_cb.bind('<<ComboboxSelected>>', self.on_machine_selected)
        self.machine_cb.current(0)
        self.on_machine_selected()

        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.pack(fill='x', pady=(20, 0))
        btn = tk.Button(btn_frame, text="GENERATE & OFFLOAD TASK", bg=CYAN, fg="#000000", font=('Segoe UI', 12, 'bold'), borderwidth=0, cursor="hand2", pady=12, command=self.on_offload_click)
        btn.pack(fill='x')

    def create_decision_card(self, parent):
        border, card = self.create_card_frame(parent, "PROCESSING DECISION", YELLOW)
        border.pack(fill='both', expand=True)

        self.decision_status_lbl = tk.Label(card, text="WAITING FOR TASK", font=('Segoe UI', 24, 'bold'), fg=TEXT_MUTED, bg=CARD_BG)
        self.decision_status_lbl.pack(pady=15)

        info_frame = tk.Frame(card, bg=CARD_BG)
        info_frame.pack(fill='x', expand=True)
        
        self.dec_labels = {}
        for row, text in enumerate(["Auto-Assigned Task Type", "Final Location", "Reason"]):
            tk.Label(info_frame, text=text, bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 11, 'bold')).grid(row=row, column=0, sticky='nw', pady=8)
            val = tk.Label(info_frame, text="-", bg=CARD_BG, fg=TEXT_MAIN, font=('Segoe UI', 12, 'bold'), wraplength=250, justify='left')
            val.grid(row=row, column=1, sticky='nw', padx=15, pady=8)
            self.dec_labels[text] = val
            info_frame.grid_rowconfigure(row, weight=1)

    # --- ROW 2: EVALUATION PANELS ---
    def build_algo_grid(self, parent, title, color):
        border, card = self.create_card_frame(parent, title, color)
        border.pack(fill='both', expand=True)
        labels = {}
        grid = tk.Frame(card, bg=CARD_BG)
        grid.pack(fill='both', expand=True)
        
        fields = ["Score", "Latency", "Response Time", "Throughput", "Resource Util", "Target Location", "Decision Time", "Remark"]
        for i, f in enumerate(fields):
            tk.Label(grid, text=f, bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 11, 'bold')).grid(row=i, column=0, sticky='w', pady=4)
            val = tk.Label(grid, text="-", bg=CARD_BG, fg=color, font=('Segoe UI', 12, 'bold'))
            val.grid(row=i, column=1, sticky='e', padx=10, pady=4)
            grid.grid_rowconfigure(i, weight=1)
            labels[f] = val
        
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        return border, labels

    def create_gbfs_card(self, parent):
        border, self.gbfs_labels = self.build_algo_grid(parent, "GBFS EVALUATION", CYAN)
        self.target_widgets["gbfs_panel"] = border
        
    def create_pso_card(self, parent):
        border, self.pso_labels = self.build_algo_grid(parent, "PSO EVALUATION", MAGENTA)
        self.target_widgets["pso_panel"] = border

    def create_offloading_eval_card(self, parent):
        border, card = self.create_card_frame(parent, "COMPARISON EVALUATION", YELLOW)
        border.pack(fill='both', expand=True)
        self.target_widgets["offloading_panel"] = border
        
        table = tk.Frame(card, bg=CARD_BORDER)
        table.pack(fill='x', pady=5)
        
        headers = ["Metric", "GBFS", "PSO", "Winner"]
        for c, h in enumerate(headers):
            tk.Label(table, text=h, bg=SIDEBAR_BG, fg=TEXT_MUTED, font=('Segoe UI', 10, 'bold')).grid(row=0, column=c, sticky='nsew', padx=1, pady=1)
        
        self.comp_labels = {}
        metrics = ["Latency", "Throughput", "Energy", "Resource"]
        
        for r, m in enumerate(metrics, start=1):
            tk.Label(table, text=m, bg=CARD_BG, fg=TEXT_MAIN, font=('Segoe UI', 11, 'bold')).grid(row=r, column=0, sticky='nsew', padx=1, pady=1)
            g = tk.Label(table, text="-", bg=CARD_BG, fg=CYAN, font=('Segoe UI', 11, 'bold'))
            g.grid(row=r, column=1, sticky='nsew', padx=1, pady=1)
            p = tk.Label(table, text="-", bg=CARD_BG, fg=MAGENTA, font=('Segoe UI', 11, 'bold'))
            p.grid(row=r, column=2, sticky='nsew', padx=1, pady=1)
            w = tk.Label(table, text="-", bg=CARD_BG, fg=GREEN, font=('Segoe UI', 11, 'bold'))
            w.grid(row=r, column=3, sticky='nsew', padx=1, pady=1)
            self.comp_labels[m] = (g, p, w)
        
        for i in range(4): table.grid_columnconfigure(i, weight=1)
        
        bot = tk.Frame(card, bg=CARD_BG)
        bot.pack(fill='x', pady=(20,0))
        tk.Label(bot, text="Winning Algorithm:", bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 12, 'bold')).pack(side='left')
        self.win_lbl = tk.Label(bot, text="-", bg=CARD_BG, fg=GREEN, font=('Segoe UI', 14, 'bold'))
        self.win_lbl.pack(side='left', padx=10)

    # --- ROW 3: ASSIGNMENT & TRANSMISSION ---
    def create_assignment_card(self, parent):
        border, card = self.create_card_frame(parent, "TASK ASSIGNMENT", CYAN)
        border.pack(fill='both', expand=True)
        self.target_widgets["assignment_panel"] = border
        self.assign_labels = {}
        
        fields = ["Task Type", "Assigned Server", "Placement Reason", "Summary"]
        grid = tk.Frame(card, bg=CARD_BG)
        grid.pack(fill='both', expand=True)
        for i, f in enumerate(fields):
            tk.Label(grid, text=f, bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 11, 'bold')).grid(row=i, column=0, sticky='nw', pady=6)
            val = tk.Label(grid, text="-", bg=CARD_BG, fg=TEXT_MAIN, font=('Segoe UI', 12, 'bold'), wraplength=450, justify='left')
            val.grid(row=i, column=1, sticky='nw', padx=15, pady=6)
            self.assign_labels[f] = val
        grid.grid_columnconfigure(1, weight=1)

    def create_transmission_card(self, parent):
        border, card = self.create_card_frame(parent, "RESULT TRANSMISSION", GREEN)
        border.pack(fill='both', expand=True)
        self.target_widgets["transmission_panel"] = border
        self.trans_labels = {}
        
        fields = ["Processing Status", "Transmission Status", "Network Return Status", "Final Task Status"]
        grid = tk.Frame(card, bg=CARD_BG)
        grid.pack(fill='both', expand=True)
        for i, f in enumerate(fields):
            tk.Label(grid, text=f, bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 11, 'bold')).grid(row=i, column=0, sticky='nw', pady=6)
            val = tk.Label(grid, text="-", bg=CARD_BG, fg=TEXT_MAIN, font=('Segoe UI', 12, 'bold'))
            val.grid(row=i, column=1, sticky='nw', padx=15, pady=6)
            self.trans_labels[f] = val
        grid.grid_columnconfigure(1, weight=1)

    # --- ROW 4: MONITORING ---
    def create_monitoring_card(self, parent):
        border, card = self.create_card_frame(parent, "PERFORMANCE MONITORING", title_color=TEXT_MAIN)
        border.pack(fill='both', expand=True)
        self.target_widgets["monitoring_panel"] = border
        # Limit height to prevent matplotlib canvas memory allocation error
        card.pack_propagate(False)
        card.config(height=350)
        self.monitor = PerformanceMonitor(card)

    # --- ROW 6: LOGS ---
    def create_logs_card(self, parent):
        border, card = self.create_card_frame(parent, "EXECUTION LOGS", TEXT_MAIN)
        border.pack(fill='both', expand=True)
        self.target_widgets["logs_panel"] = border
        
        headers = ["No.", "Machine Category", "Specific Machine", "Input Metrics", "Task Type", "GBFS Lat", "PSO Lat", "GBFS Eng", "PSO Eng", "Winner", "Server", "Status"]
        self.log_weights = [1, 2, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1]
        
        header_frame = tk.Frame(card, bg=SIDEBAR_BG, pady=8)
        header_frame.pack(fill='x')
        for i, h in enumerate(headers):
            lbl = tk.Label(header_frame, text=h, bg=SIDEBAR_BG, fg=TEXT_MUTED, font=('Segoe UI', 9, 'bold'), anchor='w')
            lbl.grid(row=0, column=i, sticky='ew', padx=5)
            header_frame.grid_columnconfigure(i, weight=self.log_weights[i])
            
        # Scrollable area
        canvas_bg = CARD_BG
        self.logs_canvas = tk.Canvas(card, bg=canvas_bg, highlightthickness=0, height=350)
        logs_scroll = ttk.Scrollbar(card, orient="vertical", command=self.logs_canvas.yview)
        self.logs_inner_frame = tk.Frame(self.logs_canvas, bg=canvas_bg)
        
        self.logs_canvas.create_window((0, 0), window=self.logs_inner_frame, anchor="nw")
        self.logs_canvas.configure(yscrollcommand=logs_scroll.set)
        
        logs_scroll.pack(side="right", fill="y")
        self.logs_canvas.pack(side="left", fill="both", expand=True)
        
        def on_logs_configure(event):
            self.logs_canvas.itemconfig(self.logs_canvas.find_withtag("all")[0], width=event.width)
            self.logs_canvas.configure(scrollregion=self.logs_canvas.bbox("all"))

        self.logs_canvas.bind("<Configure>", on_logs_configure)
        self.logs_inner_frame.bind("<Configure>", lambda e: self.logs_canvas.configure(scrollregion=self.logs_canvas.bbox("all")))
        
        self.log_row_count = 0

    def add_log_record(self, data):
        r = self.log_row_count
        self.log_row_count += 1
        bg_color = CARD_BG if r % 2 == 0 else "#253347"
        
        row_frame = tk.Frame(self.logs_inner_frame, bg=bg_color, pady=8)
        row_frame.pack(fill='x', pady=2)
        
        for i, w in enumerate(self.log_weights): row_frame.grid_columnconfigure(i, weight=w)
        
        def make_lbl(idx, text, fg=TEXT_MAIN, font_weight='normal'):
            tk.Label(row_frame, text=text, bg=bg_color, fg=fg, font=('Segoe UI', 9, font_weight), anchor='w', wraplength=180, justify='left').grid(row=0, column=idx, sticky='ew', padx=5)
            
        make_lbl(0, str(data[0]), TEXT_MUTED)
        make_lbl(1, data[1], TEXT_MAIN)
        make_lbl(2, data[2], TEXT_MAIN)
        make_lbl(3, data[3], TEXT_MUTED)
        make_lbl(4, data[4], TEXT_MAIN)
        make_lbl(5, data[5], TEXT_MAIN)
        make_lbl(6, data[6], TEXT_MAIN)
        make_lbl(7, data[7], TEXT_MAIN)
        make_lbl(8, data[8], TEXT_MAIN)
        
        winner = data[9]
        w_color = CYAN if winner == "GBFS" else "#f97316" # Orange for PSO
        make_lbl(9, winner, w_color, 'bold')
        
        server = data[10]
        s_color = {"Local": "#3b82f6", "Edge": CYAN, "Cloud": "#a855f7"}.get(server, TEXT_MAIN)
        make_lbl(10, server, s_color, 'bold')
        
        status = data[11]
        st_frame = tk.Frame(row_frame, bg=bg_color)
        st_frame.grid(row=0, column=11, sticky='w', padx=5)
        st_color = GREEN if status == "SUCCESS" else ("#ef4444" if status == "FAILED" else YELLOW)
        tk.Label(st_frame, text=f" {status} ", bg=st_color, fg="#000000", font=('Segoe UI', 8, 'bold')).pack(side='left')
        
        self.logs_canvas.update_idletasks()
        self.logs_canvas.yview_moveto(1.0)

    # --- LOGIC & FLOW ---
    def on_machine_selected(self, event=None):
        machine = self.machine_var.get()
        if machine == "Select Machine" or not machine:
            self.category_var.set("")
            self.auto_task_type_var.set("")
            for w in self.dynamic_metrics_frame.winfo_children(): w.destroy()
            self.dynamic_inputs.clear()
            return
            
        categories = {
            "CNC Milling Machine": "Frame Fabrication / Metal Fabrication",
            "Arc Welding Machine": "Welding Machines",
            "Plasma Cutting Machine": "Cutting Machines",
            "Conveyor Systems": "Assembly Line Equipment",
            "Electro-Deposition Coating System": "Painting Machines"
        }
        metrics = {
            "CNC Milling Machine": ["Temperature", "Vibration", "Spindle Speed", "Motor Load"],
            "Arc Welding Machine": ["Welding Current", "Machine Temperature", "Power Consumption"],
            "Plasma Cutting Machine": ["Cutting Speed", "Machine Temperature", "Energy Consumption"],
            "Conveyor Systems": ["Queue Length", "Processing Time", "Idle Time"],
            "Electro-Deposition Coating System": ["Temperature", "Humidity", "Cycle Time"]
        }
        task_types = {
            "CNC Milling Machine": "Computation-Intensive",
            "Arc Welding Machine": "Latency-Sensitive",
            "Plasma Cutting Machine": "Computation-Intensive",
            "Conveyor Systems": "Latency-Sensitive",
            "Electro-Deposition Coating System": "Balanced"
        }
        
        self.category_var.set(categories.get(machine, ""))
        self.auto_task_type_var.set(task_types.get(machine, "Balanced"))
        
        for w in self.dynamic_metrics_frame.winfo_children(): w.destroy()
        self.dynamic_inputs.clear()
        
        for i, m in enumerate(metrics.get(machine, [])):
            tk.Label(self.dynamic_metrics_frame, text=f"{m}:", bg=CARD_BG, fg=TEXT_MUTED, font=('Segoe UI', 11, 'bold')).grid(row=i, column=0, sticky='w', pady=6)
            
            entry_border = tk.Frame(self.dynamic_metrics_frame, bg=SIDEBAR_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
            entry_border.grid(row=i, column=1, sticky='ew', padx=15, pady=6)
            
            e = tk.Entry(entry_border, bg=SIDEBAR_BG, fg=TEXT_MAIN, bd=0, insertbackground='white', font=('Segoe UI', 12))
            e.insert(0, "0")
            e.pack(fill='x', padx=5, pady=3)
            self.dynamic_inputs[m] = e

    def set_flow_step(self, active_index):
        steps = list(self.flow_labels.keys())
        for i, step in enumerate(steps):
            dot, lbl = self.flow_labels[step]
            if i < active_index:
                dot.config(fg=GREEN)
                lbl.config(fg=TEXT_MAIN)
            elif i == active_index:
                dot.config(fg=YELLOW)
                lbl.config(fg=CYAN)
            else:
                dot.config(fg=CARD_BORDER)
                lbl.config(fg=TEXT_MUTED)
        self.root.update_idletasks()

    def get_form_values(self):
        v = {}
        v["Machine ID"] = f"MCH-{random.randint(100, 999)}"
        v["CPU Load (%)"] = str(random.randint(50, 95))
        v["Net Latency (ms)"] = str(random.randint(10, 50))
        v["Power Usage (W)"] = str(random.randint(10, 30))
        v["Task Queue"] = str(random.randint(1, 10))
        v["Input Metrics"] = " | ".join([f"{k}: {e.get()}" for k, e in self.dynamic_inputs.items()])
        for k, e in self.dynamic_inputs.items(): v[k] = e.get()
        v["Task Type"] = self.auto_task_type_var.get()
        v["Specific Machine"] = self.machine_var.get()
        v["Machine Category"] = self.category_var.get()
        return v

    def on_offload_click(self):
        machine = self.machine_var.get()
        if machine == "Select Machine" or not machine:
            messagebox.showwarning("Warning", "Please select a machine before generating a task.")
            return
            
        try:
            params = self.get_form_values()
            self.set_flow_step(0)
            
            self.dec_labels["Auto-Assigned Task Type"].config(text=params["Task Type"])
            self.decision_status_lbl.config(text="EVALUATING...", fg=YELLOW)
            
            time.sleep(0.3)
            self.set_flow_step(1)
            
            gbfs_res = compute_gbfs_score(params)
            pso_res = compute_pso_score(params)
            self.update_algo_panel_vals(self.gbfs_labels, gbfs_res)
            self.update_algo_panel_vals(self.pso_labels, pso_res)
            self.root.update()
            
            time.sleep(0.3)
            self.set_flow_step(2)
            winner, server, placement_reason, w_data = self.run_task_offloading_eval(params, gbfs_res, pso_res)
            
            # Update decision card
            self.decision_status_lbl.config(text=f"OFFLOAD TO {server.upper()}", fg=CYAN if server=='Edge' else MAGENTA)
            self.dec_labels["Final Location"].config(text=f"{server} Server", fg=CYAN if server=='Edge' else MAGENTA)
            self.dec_labels["Reason"].config(text=placement_reason)
            
            # Update assignment
            self.assign_labels["Task Type"].config(text=params["Task Type"])
            self.assign_labels["Assigned Server"].config(text=f"{server} Server", fg=CYAN if server=='Edge' else MAGENTA)
            self.assign_labels["Placement Reason"].config(text=placement_reason)
            self.assign_labels["Summary"].config(text=f"{winner} assigned task to {server} Server.")
            
            time.sleep(0.3)
            self.set_flow_step(3)
            self.trans_labels["Processing Status"].config(text="Processing Complete", fg=GREEN)
            self.trans_labels["Transmission Status"].config(text="Network Transmitting...", fg=YELLOW)
            self.root.update()
            
            time.sleep(0.3)
            self.set_flow_step(4)
            self.trans_labels["Transmission Status"].config(text="Transmission Complete", fg=GREEN)
            self.trans_labels["Network Return Status"].config(text="Confirmed", fg=GREEN)
            self.trans_labels["Final Task Status"].config(text="Task Successfully Offloaded & Returned", fg=CYAN)
            
            # Monitor & Log
            self.monitor.update_graphs(gbfs_res, pso_res)
            self.record_counter += 1
            
            log_data = (
                self.record_counter, params["Machine Category"], params["Specific Machine"], params["Input Metrics"], params["Task Type"],
                f"{gbfs_res['latency']:.2f}", f"{pso_res['latency']:.2f}", f"{gbfs_res['energy']:.2f}", f"{pso_res['energy']:.2f}", winner, server, "SUCCESS"
            )
            self.add_log_record(log_data)
            self.canvas.yview_moveto(0.3)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process: {e}")
            self.set_flow_step(-1)
            self.decision_status_lbl.config(text="ERROR", fg="#ef4444")

    def update_algo_panel_vals(self, labels, res):
        labels["Score"].config(text=str(res.get('score', '-')))
        labels["Latency"].config(text=f"{res.get('latency', '-')} ms")
        labels["Response Time"].config(text=f"{res.get('time', '-')} ms") # Mocking response time using decision time
        labels["Throughput"].config(text=f"{res.get('throughput', '-')} tps")
        labels["Resource Util"].config(text=f"{res.get('utilization', '-')} %")
        labels["Target Location"].config(text=res.get('location', '-'))
        labels["Decision Time"].config(text=res.get('time', '-'))
        labels["Remark"].config(text=res.get('remark', '-'))

    def run_task_offloading_eval(self, params, gbfs, pso):
        task_type = params.get("Task Type", "Balanced")
        def compare(g, p, lower_is_better=True):
            if lower_is_better: return "GBFS" if g < p else "PSO"
            return "GBFS" if g > p else "PSO"

        b_lat = compare(gbfs['latency'], pso['latency'], True)
        b_thr = compare(gbfs['throughput'], pso['throughput'], False)
        b_eng = compare(gbfs['energy'], pso['energy'], True)
        b_utl = compare(gbfs['utilization'], pso['utilization'], True)

        self.comp_labels["Latency"][0].config(text=f"{gbfs['latency']} ms")
        self.comp_labels["Latency"][1].config(text=f"{pso['latency']} ms")
        self.comp_labels["Latency"][2].config(text=b_lat, fg=CYAN if b_lat=='GBFS' else MAGENTA)
        
        self.comp_labels["Throughput"][0].config(text=f"{gbfs['throughput']} tps")
        self.comp_labels["Throughput"][1].config(text=f"{pso['throughput']} tps")
        self.comp_labels["Throughput"][2].config(text=b_thr, fg=CYAN if b_thr=='GBFS' else MAGENTA)
        
        self.comp_labels["Energy"][0].config(text=f"{gbfs['energy']} W")
        self.comp_labels["Energy"][1].config(text=f"{pso['energy']} W")
        self.comp_labels["Energy"][2].config(text=b_eng, fg=CYAN if b_eng=='GBFS' else MAGENTA)
        
        self.comp_labels["Resource"][0].config(text=f"{gbfs['utilization']} %")
        self.comp_labels["Resource"][1].config(text=f"{pso['utilization']} %")
        self.comp_labels["Resource"][2].config(text=b_utl, fg=CYAN if b_utl=='GBFS' else MAGENTA)

        if task_type == "Latency-Sensitive":
            winner = b_lat
            reason = f"{winner} chosen for superior latency handling."
            server = "Edge"
        elif task_type == "Computation-Intensive":
            winner = b_thr
            reason = f"{winner} chosen for higher throughput capability."
            server = "Cloud"
        else:
            winner = b_eng
            reason = f"{winner} chosen for better energy efficiency."
            server = "Cloud" if pso['utilization'] > 80 else "Edge"
            
        winning_algo_data = gbfs if winner == "GBFS" else pso
        server = winning_algo_data['location']

        self.win_lbl.config(text=winner, fg=CYAN if winner=='GBFS' else MAGENTA)
        return winner, server, reason, winning_algo_data

