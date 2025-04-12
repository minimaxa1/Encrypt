import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import random
import threading
import time
from typing import List, Dict
import json
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class TerminalOutput(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=("Consolas", 12), text_color="#00FF00", fg_color="#0D1117", border_width=1, wrap="word")
        self.tag_config("success", foreground="#00FF00")
        self.tag_config("warning", foreground="#FFA500")
        self.tag_config("error", foreground="#FF0000")
        self.tag_config("info", foreground="#00BFFF")
        self.tag_config("system", foreground="#FFFFFF")

    def add_message(self, message, tag="info"):
        self.configure(state="normal")
        timestamp = time.strftime("[%H:%M:%S] ", time.localtime())
        self.insert(tk.END, timestamp, "system")
        self.insert(tk.END, message + "\n", tag)
        self.see(tk.END)
        self.configure(state="disabled")

class NetworkGraph(ctk.CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#0D1117", highlightthickness=0)
        self.nodes = []
        self.connections = []
        self.active_nodes = set()
        self.infected_nodes = set()

    def initialize_network(self, num_nodes=25):
        self.delete("all")
        self.nodes = []
        self.connections = []
        self.active_nodes = set()
        self.infected_nodes = set()

        # Create nodes
        width = self.winfo_width() or 600
        height = self.winfo_height() or 300

        for _ in range(num_nodes):
            x = random.randint(20, width-20)
            y = random.randint(20, height-20)
            node_type = random.choice(["server", "router", "firewall", "database", "endpoint"])
            node_id = len(self.nodes)
            self.nodes.append({"id": node_id, "x": x, "y": y, "type": node_type})

        # Create connections (edges)
        for i in range(len(self.nodes)):
            # Connect to 2-4 other nodes
            num_connections = random.randint(2, 4)
            potential_targets = list(range(len(self.nodes)))
            potential_targets.remove(i)  # Can't connect to self

            # If we already have connections, avoid those nodes
            existing_connections = [c[1] for c in self.connections if c[0] == i] + [c[0] for c in self.connections if c[1] == i]
            for existing in existing_connections:
                if existing in potential_targets:
                    potential_targets.remove(existing)

            # Create new connections
            for _ in range(min(num_connections, len(potential_targets))):
                if not potential_targets:
                    break
                target = random.choice(potential_targets)
                potential_targets.remove(target)

                # Avoid duplicate connections
                if (i, target) not in self.connections and (target, i) not in self.connections:
                    self.connections.append((i, target))

        self.redraw()

    def redraw(self):
        self.delete("all")

        # Draw connections
        for source, target in self.connections:
            source_node = self.nodes[source]
            target_node = self.nodes[target]

            # Determine connection color
            if source in self.infected_nodes and target in self.infected_nodes:
                line_color = "#00FF00"  # Green for infected
                line_width = 2
            elif source in self.active_nodes and target in self.active_nodes:
                line_color = "#FFD700"  # Gold for active
                line_width = 2
            else:
                line_color = "#555555"  # Grey for inactive
                line_width = 1

            self.create_line(source_node["x"], source_node["y"],
                           target_node["x"], target_node["y"],
                           fill=line_color, width=line_width)

        # Draw nodes
        for i, node in enumerate(self.nodes):
            # Determine node color
            if i in self.infected_nodes:
                fill_color = "#00FF00"  # Green for infected
                outline_color = "#00AA00"
            elif i in self.active_nodes:
                fill_color = "#FFD700"  # Gold for active
                outline_color = "#B8860B"
            else:
                fill_color = "#1E90FF"  # Blue for normal
                outline_color = "#4169E1"

            # Draw node with appropriate icon or shape based on type
            if node["type"] == "server":
                self.create_rectangle(node["x"]-8, node["y"]-8, node["x"]+8, node["y"]+8,
                                    fill=fill_color, outline=outline_color, width=2)
            elif node["type"] == "router":
                self.create_oval(node["x"]-7, node["y"]-7, node["x"]+7, node["y"]+7,
                               fill=fill_color, outline=outline_color, width=2)
            elif node["type"] == "firewall":
                self.create_polygon(node["x"], node["y"]-8, node["x"]+8, node["y"]+4, node["x"]-8, node["y"]+4,
                                  fill=fill_color, outline=outline_color, width=2)
            elif node["type"] == "database":
                self.create_oval(node["x"]-6, node["y"]-8, node["x"]+6, node["y"]+8,
                               fill=fill_color, outline=outline_color, width=2)
            else:  # endpoint
                self.create_rectangle(node["x"]-5, node["y"]-5, node["x"]+5, node["y"]+5,
                                    fill=fill_color, outline=outline_color, width=2)

            # Add small label with node type
            self.create_text(node["x"], node["y"]+15, text=node["type"][0].upper(), fill="#AAAAAA", font=("Arial", 7))

    def activate_node(self, node_id):
        if 0 <= node_id < len(self.nodes):
            self.active_nodes.add(node_id)
            self.redraw()

    def infect_node(self, node_id):
        if 0 <= node_id < len(self.nodes):
            self.infected_nodes.add(node_id)
            self.redraw()

    def get_connected_nodes(self, node_id):
        connected = []
        for source, target in self.connections:
            if source == node_id:
                connected.append(target)
            elif target == node_id:
                connected.append(source)
        return connected

class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#1A1E24", corner_radius=0)

        # Create status indicators
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.status_labels = {}
        statuses = [
            ("connection", "Connection", "#00FF00"),
            ("encryption", "Encryption", "#00FF00"),
            ("detection", "Detection Risk", "#00FF00"),
            ("progress", "Progress", "#00FF00")
        ]

        for i, (key, text, color) in enumerate(statuses):
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

            label = ctk.CTkLabel(frame, text=text, font=("Arial", 12))
            label.pack(side="left", padx=5)

            status = ctk.CTkLabel(frame, text="Optimal", text_color=color, font=("Arial", 12, "bold"))
            status.pack(side="right", padx=5)

            self.status_labels[key] = status

    def update_status(self, key, text, color):
        if key in self.status_labels:
            self.status_labels[key].configure(text=text, text_color=color)

class ProgressModule(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, **kwargs)

        # Configure frame
        self.configure(fg_color="#1A1E24", corner_radius=10)

        # Add title
        self.title_label = ctk.CTkLabel(self, text=title, font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(10, 5), padx=10, anchor="w")

        # Add progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)

        # Add status text
        self.status_text = ctk.CTkLabel(self, text="Waiting...", text_color="#AAAAAA")
        self.status_text.pack(pady=(0, 10), padx=10, anchor="w")

    def update_progress(self, value, status_text=None, status_color=None):
        self.progress_bar.set(value)
        if status_text:
            self.status_text.configure(text=status_text)
        if status_color:
            self.status_text.configure(text_color=status_color)

class MimicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("MIMIC - Advanced Network Infiltration System")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Create main grid layout
        self.grid_columnconfigure(0, weight=0)  # Control panel - fixed width
        self.grid_columnconfigure(1, weight=1)  # Main area - expandable
        self.grid_rowconfigure(0, weight=1)     # Content area - expandable
        self.grid_rowconfigure(1, weight=0)     # Status bar - fixed height

        # Create control panel (left sidebar)
        self.control_panel = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#0D1117")
        self.control_panel.grid(row=0, column=0, sticky="nsew")
        self.control_panel.grid_propagate(False)  # Prevent resizing

        # App title/logo
        self.logo_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.logo_frame.pack(fill="x", padx=20, pady=20)

        self.logo_label = ctk.CTkLabel(self.logo_frame, text="MIMIC", font=("Arial", 24, "bold"))
        self.logo_label.pack(side="left")

        self.subtitle_label = ctk.CTkLabel(self.control_panel,
                                         text="Advanced Network Infiltration System",
                                         font=("Arial", 12),
                                         text_color="#AAAAAA")
        self.subtitle_label.pack(fill="x", padx=20, pady=(0, 20))

        # Control buttons
        self.btn_scan = ctk.CTkButton(self.control_panel, text="Scan Network", command=self.start_scan)
        self.btn_scan.pack(fill="x", padx=20, pady=10)

        self.btn_infiltrate = ctk.CTkButton(self.control_panel, text="Deploy Mimic",
                                          state="disabled", command=self.start_infiltration)
        self.btn_infiltrate.pack(fill="x", padx=20, pady=10)

        self.btn_analyze = ctk.CTkButton(self.control_panel, text="Analyze Environment",
                                       state="disabled", command=self.analyze_environment)
        self.btn_analyze.pack(fill="x", padx=20, pady=10)

        self.btn_exfiltrate = ctk.CTkButton(self.control_panel, text="Gather Intelligence",
                                          state="disabled", command=self.gather_intelligence) # Corrected button definition
        self.btn_exfiltrate.pack(fill="x", padx=20, pady=10)

        # Target system selector
        self.target_label = ctk.CTkLabel(self.control_panel, text="Target System:", anchor="w")
        self.target_label.pack(fill="x", padx=20, pady=(20, 5))

        self.target_var = tk.StringVar(value="GOV-SECLAB-MAINFRAME")
        self.target_selector = ctk.CTkComboBox(self.control_panel,
                                             values=["GOV-SECLAB-MAINFRAME", "NSA-DATANODE-07", "DARPA-RESEARCH-NET", "FED-INTELLIGENCE-GRID"],
                                             variable=self.target_var)
        self.target_selector.pack(fill="x", padx=20, pady=5)

        # Information frame at bottom of sidebar
        self.info_frame = ctk.CTkFrame(self.control_panel, fg_color="#161B22")
        self.info_frame.pack(fill="x", padx=10, pady=10, side="bottom")

        self.connection_status = ctk.CTkLabel(self.info_frame, text="Secure Connection: ACTIVE",
                                            text_color="#00FF00", font=("Arial", 12))
        self.connection_status.pack(pady=5)

        self.encryption_status = ctk.CTkLabel(self.info_frame, text="Encryption: AES-256",
                                            text_color="#00BFFF", font=("Arial", 12))
        self.encryption_status.pack(pady=5)

        # Create main content area
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="#0A0E14")
        self.content_area.grid(row=0, column=1, sticky="nsew")

        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=3)  # Network visualization
        self.content_area.grid_rowconfigure(1, weight=2)  # Terminal output
        self.content_area.grid_rowconfigure(2, weight=1)  # Progress modules

        # Create network visualization
        self.network_frame = ctk.CTkFrame(self.content_area, fg_color="#0D1117", corner_radius=10)
        self.network_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.network_header = ctk.CTkLabel(self.network_frame, text="Network Topology",
                                         font=("Arial", 14, "bold"))
        self.network_header.pack(padx=10, pady=10, anchor="w")

        self.network_graph = NetworkGraph(self.network_frame)
        self.network_graph.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create terminal output
        self.terminal_frame = ctk.CTkFrame(self.content_area, fg_color="#0D1117", corner_radius=10)
        self.terminal_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.terminal_header = ctk.CTkLabel(self.terminal_frame, text="Operation Log",
                                          font=("Arial", 14, "bold"))
        self.terminal_header.pack(padx=10, pady=10, anchor="w")

        self.terminal = TerminalOutput(self.terminal_frame, height=10)
        self.terminal.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create progress modules
        self.progress_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.progress_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.progress_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.progress_frame.grid_rowconfigure(0, weight=1)

        self.infiltration_module = ProgressModule(self.progress_frame, "System Infiltration")
        self.infiltration_module.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.mimicry_module = ProgressModule(self.progress_frame, "Protocol Mimicry")
        self.mimicry_module.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.data_module = ProgressModule(self.progress_frame, "Intelligence Collection")
        self.data_module.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        # Create status bar
        self.status_bar = StatusBar(self, height=30)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Initialize data
        self.running = False
        self.current_phase = None
        self.collected_data = []
        self.current_node = None
        self.target_nodes = []

        # Add welcome message
        self.terminal.add_message("MIMIC Infiltration System v3.7.4 initialized", "success")
        self.terminal.add_message("Connect to a target system to begin infiltration sequence", "info")

        # Bind to events
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize network graph once window is fully loaded
        self.after(100, self.network_graph.initialize_network)

    def start_scan(self):
        if self.running:
            return

        self.running = True
        self.btn_scan.configure(state="disabled")

        # Reset progress
        self.infiltration_module.update_progress(0, "Preparing scan...", "#AAAAAA")
        self.mimicry_module.update_progress(0, "Waiting...", "#AAAAAA")
        self.data_module.update_progress(0, "Waiting...", "#AAAAAA")

        self.current_phase = "scan"

        # Update status
        self.status_bar.update_status("connection", "Establishing", "#FFA500")
        self.status_bar.update_status("detection", "Minimal", "#00FF00")
        self.status_bar.update_status("progress", "Scanning", "#00BFFF")

        self.terminal.add_message(f"Initiating network scan on target: {self.target_var.get()}", "info")

        # Start scanning animation in separate thread
        threading.Thread(target=self.run_scanning_simulation, daemon=True).start()

    def run_scanning_simulation(self):
        # Simulate network scanning
        target_name = self.target_var.get()
        scan_progress = 0

        # Reset network
        self.after(0, self.network_graph.initialize_network)
        time.sleep(1)

        # Find entry point
        total_nodes = len(self.network_graph.nodes)
        entry_point = random.randint(0, total_nodes - 1)
        self.current_node = entry_point

        self.after(0, lambda: self.terminal.add_message(f"Searching for vulnerabilities in {target_name} network...", "info"))

        while scan_progress < 1.0 and self.running:
            scan_progress += random.uniform(0.05, 0.1)
            scan_progress = min(scan_progress, 1.0)

            # Simulate scanning activity
            self.after(0, lambda p=scan_progress: self.infiltration_module.update_progress(p,
                                                                                        "Mapping network topology..." if p < 0.5 else
                                                                                        "Identifying vulnerable nodes...",
                                                                                        "#00BFFF"))

            # Activate random nodes to simulate scanning
            if scan_progress < 0.9:
                node_to_activate = random.randint(0, total_nodes - 1)
                self.after(0, lambda n=node_to_activate: self.network_graph.activate_node(n))

                # Add scan messages
                if random.random() < 0.3:
                    node_type = self.network_graph.nodes[node_to_activate]["type"]
                    self.after(0, lambda t=node_type: self.terminal.add_message(
                        f"Discovered {t.upper()} node with {random.choice(['standard', 'outdated', 'enhanced'])} security",
                        "info"))

            time.sleep(0.5)

        # Scan complete
        if self.running:
            # Select target nodes (high-value systems)
            potential_targets = [i for i in range(total_nodes)
                               if self.network_graph.nodes[i]["type"] in ["server", "database"]]

            self.target_nodes = random.sample(potential_targets, min(3, len(potential_targets)))

            # Highlight entry point
            self.after(0, lambda: self.network_graph.activate_node(entry_point))
            self.after(0, lambda: self.terminal.add_message(
                f"Scan complete. Entry point identified: {self.network_graph.nodes[entry_point]['type'].upper()}",
                "success"))

            # Highlight target nodes
            for target in self.target_nodes:
                self.after(0, lambda t=target: self.network_graph.activate_node(t))
                node_type = self.network_graph.nodes[target]["type"].upper()
                self.after(0, lambda t=node_type: self.terminal.add_message(
                    f"High-value target identified: {t}", "info"))

            # Update UI
            self.after(0, lambda: self.btn_infiltrate.configure(state="normal"))
            self.after(0, lambda: self.infiltration_module.update_progress(1.0, "Scan complete", "#00FF00"))
            self.after(0, lambda: self.status_bar.update_status("progress", "Scan Complete", "#00FF00"))
            self.after(0, lambda: self.status_bar.update_status("connection", "Established", "#00FF00"))

            self.running = False

    def start_infiltration(self):
        if self.running:
            return

        self.running = True
        self.btn_infiltrate.configure(state="disabled")

        # Reset progress
        self.mimicry_module.update_progress(0, "Initializing mimicry protocols...", "#AAAAAA")
        self.data_module.update_progress(0, "Waiting...", "#AAAAAA")

        self.current_phase = "infiltrate"

        # Update status
        self.status_bar.update_status("detection", "Low", "#FFA500")
        self.status_bar.update_status("progress", "Infiltrating", "#FFA500")

        self.terminal.add_message("Deploying Mimic infiltration module...", "info")
        self.terminal.add_message("Establishing secure communication channels...", "info")

        # Start infiltration in separate thread
        threading.Thread(target=self.run_infiltration_simulation, daemon=True).start()

    def run_infiltration_simulation(self):
        # Simulate infiltration process
        infiltration_progress = 0
        mimicry_progress = 0

        # Start with entry point
        self.after(0, lambda: self.network_graph.infect_node(self.current_node))
        self.after(0, lambda: self.terminal.add_message(
            f"Initial access established at node {self.current_node}", "success"))

        infected_nodes = {self.current_node}
        attempt_count = 0

        while (len(infected_nodes) < len(self.target_nodes) + 3) and self.running and attempt_count < 20:
            attempt_count += 1

            # Update infiltration progress
            infiltration_progress = min(1.0, len(infected_nodes) / (len(self.target_nodes) + 3))
            self.after(0, lambda p=infiltration_progress: self.infiltration_module.update_progress(p,
                                                                                                "Establishing persistence...",
                                                                                                "#00BFFF"))

            # Update mimicry progress
            mimicry_progress += random.uniform(0.1, 0.2)
            mimicry_progress = min(mimicry_progress, 1.0)
            self.after(0, lambda p=mimicry_progress: self.mimicry_module.update_progress(p,
                                                                                       "Adapting to system protocols...",
                                                                                       "#00BFFF"))

            # Try to spread to connected nodes
            for node_id in list(infected_nodes):
                connected = self.network_graph.get_connected_nodes(node_id)
                for target in connected:
                    if target not in infected_nodes and random.random() < 0.4:
                        # Successfully infected a new node
                        infected_nodes.add(target)
                        self.after(0, lambda t=target: self.network_graph.infect_node(t))

                        # Generate message based on node type
                        node_type = self.network_graph.nodes[target]["type"]
                        if node_type == "firewall":
                            self.after(0, lambda: self.terminal.add_message(
                                "Bypassing firewall security by mimicking authorized traffic patterns", "warning"))
                        elif node_type == "router":
                            self.after(0, lambda: self.terminal.add_message(
                                "Routing table accessed, creating hidden communication channels", "info"))
                        elif node_type == "server":
                            self.after(0, lambda: self.terminal.add_message(
                                "Server infiltrated - established persistence via modified service module", "success"))
                        elif node_type == "database":
                            self.after(0, lambda: self.terminal.add_message(
                                "Database server accessed - concealing queries within legitimate traffic", "success"))
                        else:
                            self.after(0, lambda: self.terminal.add_message(
                                f"Successfully infiltrated {node_type} node", "info"))

                        # Simulate some detection risk
                        if random.random() < 0.2:
                            self.after(0, lambda: self.terminal.add_message(
                                f"Security scan detected - shifting traffic patterns to avoid detection", "warning"))
                            self.after(0, lambda: self.status_bar.update_status("detection", "Moderate", "#FFA500"))
                            time.sleep(0.5)
                            self.after(0, lambda: self.status_bar.update_status("detection", "Low", "#00FF00"))

            time.sleep(0.8)

        # Infiltration complete
        if self.running:
            self.after(0, lambda: self.terminal.add_message(
                "Mimic infiltration complete - established presence in target network", "success"))
            self.after(0, lambda: self.terminal.add_message(
                "System defenses successfully bypassed. No signs of detection.", "success"))

            # Update UI
            self.after(0, lambda: self.btn_analyze.configure(state="normal"))
            self.after(0, lambda: self.infiltration_module.update_progress(1.0, "Infiltration complete", "#00FF00"))
            self.after(0, lambda: self.mimicry_module.update_progress(1.0, "Protocol mimicry active", "#00FF00"))
            self.after(0, lambda: self.status_bar.update_status("progress", "Infiltrated", "#00FF00"))

            self.running = False

    def analyze_environment(self):
        if self.running:
            return

        self.running = True
        self.btn_analyze.configure(state="disabled")

        self.current_phase = "analyze"

        # Update status
        self.terminal.add_message("Beginning environment analysis...", "info")
        self.terminal.add_message("Scanning for classified information and system vulnerabilities...", "info")

        # Start analysis in separate thread
        threading.Thread(target=self.run_analysis_simulation, daemon=True).start()

    def run_analysis_simulation(self):
        # Simulate system analysis
        time.sleep(1)

        # Generate fake discovery data
        discoveries = [
            {"type": "personnel", "message": "Discovered classified personnel records for operation 'SHADOWFALL'", "tag": "warning"},
            {"type": "operation", "message": "Located protocol details for experimental memory reconfiguration technology", "tag": "warning"},
            {"type": "subject", "message": "Found list of subjects previously processed through memory reconfiguration", "tag": "warning"},
            {"type": "security", "message": "Identified critical vulnerability in security subsystem", "tag": "success"},
            {"type": "network", "message": "Mapped connections to 3 additional classified research facilities", "tag": "info"},
            {"type": "system", "message": "Discovered automated backup schedule - optimal exfiltration window identified", "tag": "success"}
        ]

        # Display discoveries
        for i, discovery in enumerate(discoveries):
            if not self.running:
                break

            # Add to collected data
            self.collected_data.append(discovery)

            # Update terminal
            self.after(0, lambda msg=discovery["message"], tag=discovery["tag"]:
                     self.terminal.add_message(msg, tag))

            # Update progress
            progress = (i + 1) / len(discoveries)
            self.after(0, lambda p=progress: self.data_module.update_progress(p,
                                                                            "Analyzing environment...",
                                                                            "#00BFFF"))

            time.sleep(random.uniform(1.0, 2.0))

        # Analysis complete
        if self.running:
            self.after(0, lambda: self.terminal.add_message(
                "Environment analysis complete. Ready", "success")) # Fixed the unterminated string and added "success" tag
            self.after(0, lambda: self.btn_exfiltrate.configure(state="normal")) # Enable Gather Intelligence button
            self.after(0, lambda: self.data_module.update_progress(1.0, "Analysis Complete", "#00FF00"))
            self.after(0, lambda: self.status_bar.update_status("progress", "Analysis Complete", "#00FF00"))

            self.running = False

    def gather_intelligence(self):
        if self.running:
            return

        self.running = True
        self.btn_exfiltrate.configure(state="disabled") # Disable button during operation

        self.current_phase = "exfiltrate"

        self.terminal.add_message("Initiating intelligence gathering operation...", "info")
        self.terminal.add_message("Preparing to exfiltrate collected data...", "info")
        self.data_module.update_progress(0, "Preparing data exfiltration...", "#AAAAAA") # Update progress module

        # Start exfiltration simulation in a thread
        threading.Thread(target=self.run_exfiltration_simulation, daemon=True).start()


    def run_exfiltration_simulation(self):
        exfiltration_progress = 0
        total_data_points = len(self.collected_data)

        if total_data_points == 0:
            self.after(0, lambda: self.terminal.add_message("No intelligence data collected to exfiltrate.", "warning"))
            self.after(0, lambda: self.data_module.update_progress(1.0, "No data to exfiltrate", "#FFA500"))
            self.after(0, lambda: self.status_bar.update_status("progress", "Exfiltration N/A", "#FFA500"))
            self.after(0, lambda: self.btn_exfiltrate.configure(state="normal")) # Re-enable button
            self.running = False
            return


        for i, data_item in enumerate(self.collected_data):
            if not self.running:
                break

            exfiltration_progress = (i + 1) / total_data_points
            self.after(0, lambda p=exfiltration_progress: self.data_module.update_progress(p,
                                                                                    "Exfiltrating data...",
                                                                                    "#00BFFF"))
            self.after(0, lambda item=data_item: self.terminal.add_message(f"Exfiltrated data: {item['type']}", "success"))
            time.sleep(random.uniform(0.3, 0.7)) # Simulate data exfiltration time


        if self.running:
            self.after(0, lambda: self.terminal.add_message("Intelligence gathering and exfiltration complete.", "success"))
            self.after(0, lambda: self.terminal.add_message("Operation MIMIC successfully concluded.", "success"))
            self.after(0, lambda: self.data_module.update_progress(1.0, "Exfiltration Complete", "#00FF00"))
            self.after(0, lambda: self.status_bar.update_status("progress", "Exfiltration Complete", "#00FF00"))
            self.after(0, lambda: self.btn_exfiltrate.configure(state="disabled")) # Keep button disabled after completion
            self.running = False


    def on_closing(self):
        self.running = False  # Stop any running threads
        self.destroy()

if __name__ == "__main__":
    app = MimicApp()
    app.mainloop()