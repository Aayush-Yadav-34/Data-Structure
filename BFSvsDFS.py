import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
import time
import tracemalloc
from collections import deque
import queue
from graphviz import Digraph
from PIL import Image, ImageTk
import io

class GraphTraversalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS vs Iterative DFS Graph Traversal Visualizer")
        self.root.geometry("1400x900")
        
        # Initialize graph and traversal data
        self.graph = nx.DiGraph()
        self.bfs_path = []
        self.dfs_path = []
        self.bfs_stats = {}
        self.dfs_stats = {}
        
        # Animation control
        self.animation_speed = 1.0
        self.animation_queue = queue.Queue()
        self.animation_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for graph input and controls (increase width)
        left_frame = ttk.LabelFrame(main_frame, text="Graph Input & Controls", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.config(width=450)  # Increased width
        left_frame.pack_propagate(False)
        
        # Graph input section
        graph_frame = ttk.LabelFrame(left_frame, text="Graph Definition", padding=5)
        graph_frame.pack(fill=tk.X, pady=(0, 10))

        # Node input
        node_input_frame = ttk.Frame(graph_frame)
        node_input_frame.pack(fill=tk.X, pady=2)
        ttk.Label(node_input_frame, text="Node:").pack(side=tk.LEFT)
        self.node_entry = ttk.Entry(node_input_frame, width=15)
        self.node_entry.pack(side=tk.LEFT, padx=2)
        self.node_entry.pack(fill=tk.X, pady=2)
        self.node_entry.insert(0, "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z")
        ttk.Button(node_input_frame, text="Add Node", command=self.add_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(node_input_frame, text="Remove Node", command=self.remove_node).pack(side=tk.LEFT, padx=2)

        # Edge input
        edge_input_frame = ttk.Frame(graph_frame)
        edge_input_frame.pack(fill=tk.X, pady=2)
        ttk.Label(edge_input_frame, text="Edge (A-B):").pack(side=tk.LEFT)
        self.edge_entry = ttk.Entry(edge_input_frame, width=15)
        self.edge_entry.pack(side=tk.LEFT, padx=2)
        self.edge_entry.pack(fill=tk.X, pady=2)
        self.edge_entry.insert(0, "A-B,B-C,C-D,D-E,E-F,E-P,F-G,P-G,G-H,G-X,H-I,H-Z,B-O,B-R,K-L,A-K,L-R,K-J,J-Q,J-S,J-Y,Q-T,Y-T,Y-W,W-A,T-M,T-U,U-N,N-V")
        ttk.Button(edge_input_frame, text="Add Edge", command=self.add_edge).pack(side=tk.LEFT, padx=2)
        ttk.Button(edge_input_frame, text="Remove Edge", command=self.remove_edge).pack(side=tk.LEFT, padx=2)

        # Button to clear the graph
        ttk.Button(graph_frame, text="Clear Graph", command=self.clear_graph).pack(pady=5)

        # Traversal controls
        control_frame = ttk.LabelFrame(left_frame, text="Traversal Controls", padding=5)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="Start Node:").pack(anchor=tk.W)
        self.start_node_var = tk.StringVar()
        self.start_node_combo = ttk.Combobox(control_frame, textvariable=self.start_node_var, 
                                           state="readonly", width=15)
        self.start_node_combo.pack(fill=tk.X, pady=2)
        
        ttk.Label(control_frame, text="Goal Node (optional):").pack(anchor=tk.W, pady=(10, 0))
        self.goal_node_var = tk.StringVar()
        self.goal_node_combo = ttk.Combobox(control_frame, textvariable=self.goal_node_var, 
                                          state="readonly", width=15)
        self.goal_node_combo.pack(fill=tk.X, pady=2)
        
        # Animation speed control
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(speed_frame, text="Animation Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.1, to=3.0, variable=self.speed_var, 
                               orient=tk.HORIZONTAL, length=150)
        speed_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Run BFS", command=self.run_bfs).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Run DFS", command=self.run_dfs).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Compare Both", command=self.compare_algorithms).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=2)
        
        # Results display
        results_frame = ttk.LabelFrame(left_frame, text="Results", padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabbed results
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # BFS Results tab
        self.bfs_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.bfs_frame, text="BFS Results")
        
        self.bfs_text = scrolledtext.ScrolledText(self.bfs_frame, height=15, width=40)
        self.bfs_text.pack(fill=tk.BOTH, expand=True)
        
        # DFS Results tab
        self.dfs_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.dfs_frame, text="DFS Results")
        
        self.dfs_text = scrolledtext.ScrolledText(self.dfs_frame, height=15, width=40)
        self.dfs_text.pack(fill=tk.BOTH, expand=True)
        
        # Comparison Results tab
        self.comparison_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.comparison_frame, text="Comparison")
        self.comparison_text = scrolledtext.ScrolledText(self.comparison_frame, height=15, width=40)
        self.comparison_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for graph visualization (decrease width)
        right_frame = ttk.LabelFrame(main_frame, text="Graph Visualization", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        right_frame.config(width=700)  # Decreased width
        right_frame.pack_propagate(False)

        # Graphviz image label (for direct display)
        self.graph_img_label = tk.Label(right_frame)
        self.graph_img_label.pack(fill=tk.BOTH, expand=True)
        
    def visualize_graph(self, bfs_visited=None, dfs_visited=None, bfs_current=None, dfs_current=None):
        """Visualize the graph using Graphviz and display in the main interface"""
        dot = Digraph(format='png')
        for node in self.graph.nodes():
            color = 'lightblue'
            if bfs_current and node == bfs_current:
                color = 'red'
            elif bfs_visited and node in bfs_visited:
                color = 'lightgreen'
            elif dfs_current and node == dfs_current:
                color = 'red'
            elif dfs_visited and node in dfs_visited:
                color = 'lightcoral'
            dot.node(node, style='filled', fillcolor=color)
        for u, v in self.graph.edges():
            dot.edge(u, v, arrowhead='none')
        img_bytes = dot.pipe(format='png')
        image = Image.open(io.BytesIO(img_bytes))
        image = image.resize((700, 600), Image.LANCZOS)
        self.graph_img = ImageTk.PhotoImage(image)
        self.graph_img_label.configure(image=self.graph_img)
        self.graph_img_label.image = self.graph_img
    
    def breadth_first_search(self, start, goal=None):
        """Perform BFS and return path with statistics"""
        if start not in self.graph.nodes():
            return [], {"error": "Start node not in graph"}
        
        # Start memory tracking
        tracemalloc.start()
        start_time = time.time()
        
        visited = set()
        queue = deque([start])
        path = []
        parent = {start: None}
        nodes_visited = 0
        
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                path.append(current)
                nodes_visited += 1
                
                # Check if goal is reached
                if goal and current == goal:
                    break
                
                # Add neighbors to queue
                for neighbor in self.graph.neighbors(current):
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                        parent[neighbor] = current
        
        end_time = time.time()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Calculate path to goal if specified
        goal_path = []
        if goal and goal in visited:
            node = goal
            while node is not None:
                goal_path.append(node)
                node = parent[node]
            goal_path.reverse()
        
        stats = {
            "algorithm": "BFS",
            "traversal_path": path,
            "goal_path": goal_path,
            "nodes_visited": nodes_visited,
            "execution_time": (end_time - start_time) * 1000,  # in milliseconds
            "memory_used": peak_mem / 1024,  # in KB
            "path_length": len(goal_path) if goal_path else 0
        }
        
        return path, stats
    
    def iterative_depth_first_search(self, start, goal=None):
        """Perform Iterative DFS and return path with statistics"""
        if start not in self.graph.nodes():
            return [], {"error": "Start node not in graph"}
        
        # Start memory tracking
        tracemalloc.start()
        start_time = time.time()
        
        visited = set()
        stack = [start]
        path = []
        parent = {start: None}
        nodes_visited = 0
        
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                path.append(current)
                nodes_visited += 1
                
                # Check if goal is reached
                if goal and current == goal:
                    break
                
                # Add neighbors to stack (in reverse order for consistent behavior)
                neighbors = list(self.graph.neighbors(current))
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        if neighbor not in parent:
                            parent[neighbor] = current
        
        end_time = time.time()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Calculate path to goal if specified
        goal_path = []
        if goal and goal in visited:
            node = goal
            while node is not None:
                goal_path.append(node)
                node = parent[node]
            goal_path.reverse()
        
        stats = {
            "algorithm": "Iterative DFS",
            "traversal_path": path,
            "goal_path": goal_path,
            "nodes_visited": nodes_visited,
            "execution_time": (end_time - start_time) * 1000,  # in milliseconds
            "memory_used": peak_mem / 1024,  # in KB
            "path_length": len(goal_path) if goal_path else 0
        }
        
        return path, stats
    
    def animate_traversal(self, path, algorithm_type):
        """Animate the traversal process"""
        visited = set()
        
        for i, node in enumerate(path):
            visited.add(node)
            
            if algorithm_type == "BFS":
                self.visualize_graph(bfs_visited=visited, bfs_current=node)
            else:
                self.visualize_graph(dfs_visited=visited, dfs_current=node)
            
            self.root.update()
            time.sleep(1.0 / self.speed_var.get())
    
    def run_bfs(self):
        """Run BFS algorithm"""
        if not self.graph.nodes():
            messagebox.showerror("Error", "Please create a graph first")
            return
        
        start = self.start_node_var.get()
        goal = self.goal_node_var.get() if self.goal_node_var.get() else None
        
        if not start:
            messagebox.showerror("Error", "Please select a start node")
            return
        
        # Run BFS
        self.bfs_path, self.bfs_stats = self.breadth_first_search(start, goal)
        
        # Display results
        self.display_results(self.bfs_stats, self.bfs_text)
        
        # Animate traversal
        self.animate_traversal(self.bfs_path, "BFS")
        
        # Switch to BFS results tab
        self.results_notebook.select(self.bfs_frame)
    
    def run_dfs(self):
        """Run DFS algorithm"""
        if not self.graph.nodes():
            messagebox.showerror("Error", "Please create a graph first")
            return
        
        start = self.start_node_var.get()
        goal = self.goal_node_var.get() if self.goal_node_var.get() else None
        
        if not start:
            messagebox.showerror("Error", "Please select a start node")
            return
        
        # Run DFS
        self.dfs_path, self.dfs_stats = self.iterative_depth_first_search(start, goal)
        
        # Display results
        self.display_results(self.dfs_stats, self.dfs_text)
        
        # Animate traversal
        self.animate_traversal(self.dfs_path, "DFS")
        
        # Switch to DFS results tab
        self.results_notebook.select(self.dfs_frame)
    
    def compare_algorithms(self):
        """Run both algorithms and show both results and the graph visualization"""
        if not self.graph.nodes():
            messagebox.showerror("Error", "Please create a graph first")
            return
        
        start = self.start_node_var.get()
        goal = self.goal_node_var.get() if self.goal_node_var.get() else None
        
        if not start:
            messagebox.showerror("Error", "Please select a start node")
            return
        
        # Run both algorithms
        self.bfs_path, self.bfs_stats = self.breadth_first_search(start, goal)
        self.dfs_path, self.dfs_stats = self.iterative_depth_first_search(start, goal)
        
        # Display individual results
        self.display_results(self.bfs_stats, self.bfs_text)
        self.display_results(self.dfs_stats, self.dfs_text)
        
        # Show final visualization with both traversals
        self.visualize_graph(bfs_visited=set(self.bfs_path), dfs_visited=set(self.dfs_path))
        
        # Display comparison
        self.display_comparison()
        
        # Switch to comparison tab
        self.results_notebook.select(self.comparison_frame)
    
    def display_results(self, stats, text_widget):
        """Display algorithm results in the specified text widget"""
        text_widget.delete('1.0', tk.END)
        
        if "error" in stats:
            text_widget.insert(tk.END, f"Error: {stats['error']}\n")
            return
        
        output = f"Algorithm: {stats['algorithm']}\n"
        output += f"{'='*40}\n\n"
        
        output += f"Traversal Path:\n"
        output += f"{' -> '.join(stats['traversal_path'])}\n\n"
        
        if stats['goal_path']:
            output += f"Path to Goal:\n"
            output += f"{' -> '.join(stats['goal_path'])}\n\n"
        
        output += f"Performance Metrics:\n"
        output += f"- Nodes Visited: {stats['nodes_visited']}\n"
        output += f"- Execution Time: {stats['execution_time']:.2f} ms\n"
        output += f"- Memory Used: {stats['memory_used']:.2f} KB\n"
        if stats['path_length'] > 0:
            output += f"- Path Length: {stats['path_length']}\n"
        
        text_widget.insert(tk.END, output)
    
    def display_comparison(self):
        """Display comparison between BFS and DFS in the comparison tab"""
        self.comparison_text.delete('1.0', tk.END)
        
        if not self.bfs_stats or not self.dfs_stats:
            self.comparison_text.insert(tk.END, "Please run both algorithms first.")
            return
        
        output = "ALGORITHM COMPARISON\n"
        output += "=" * 50 + "\n\n"
        
        # Traversal comparison
        output += "TRAVERSAL PATHS:\n"
        output += f"BFS: {' -> '.join(self.bfs_stats['traversal_path'])}\n"
        output += f"DFS: {' -> '.join(self.dfs_stats['traversal_path'])}\n\n"
        
        # Goal path comparison
        if self.bfs_stats['goal_path'] and self.dfs_stats['goal_path']:
            output += "PATHS TO GOAL:\n"
            output += f"BFS: {' -> '.join(self.bfs_stats['goal_path'])}\n"
            output += f"DFS: {' -> '.join(self.dfs_stats['goal_path'])}\n\n"
        
        # Performance comparison
        output += "PERFORMANCE COMPARISON:\n"
        output += f"{'Metric':<20} {'BFS':<15} {'DFS':<15} {'Winner':<10}\n"
        output += "-" * 60 + "\n"
        
        # Nodes visited
        bfs_nodes = self.bfs_stats['nodes_visited']
        dfs_nodes = self.dfs_stats['nodes_visited']
        nodes_winner = "BFS" if bfs_nodes <= dfs_nodes else "DFS"
        output += f"{'Nodes Visited':<20} {bfs_nodes:<15} {dfs_nodes:<15} {nodes_winner:<10}\n"
        
        # Execution time
        bfs_time = self.bfs_stats['execution_time']
        dfs_time = self.dfs_stats['execution_time']
        time_winner = "BFS" if bfs_time <= dfs_time else "DFS"
        output += f"{'Execution Time (ms)':<20} {bfs_time:<15.2f} {dfs_time:<15.2f} {time_winner:<10}\n"
        
        # Memory usage
        bfs_mem = self.bfs_stats['memory_used']
        dfs_mem = self.dfs_stats['memory_used']
        mem_winner = "BFS" if bfs_mem <= dfs_mem else "DFS"
        output += f"{'Memory Used (KB)':<20} {bfs_mem:<15.2f} {dfs_mem:<15.2f} {mem_winner:<10}\n"
        
        # Path length (if goal specified)
        if self.bfs_stats['path_length'] > 0 and self.dfs_stats['path_length'] > 0:
            bfs_path_len = self.bfs_stats['path_length']
            dfs_path_len = self.dfs_stats['path_length']
            path_winner = "BFS" if bfs_path_len <= dfs_path_len else "DFS"
            output += f"{'Path Length':<20} {bfs_path_len:<15} {dfs_path_len:<15} {path_winner:<10}\n"
        
        self.comparison_text.insert(tk.END, output)
    
    def clear_results(self):
        """Clear all results and visualizations"""
        self.bfs_text.delete('1.0', tk.END)
        self.dfs_text.delete('1.0', tk.END)
        self.comparison_text.delete('1.0', tk.END)
        
        self.bfs_path = []
        self.dfs_path = []
        self.bfs_stats = {}
        self.dfs_stats = {}
        
        # Reset visualization
        self.visualize_graph()
    
    def add_node(self):
        nodes = [n.strip() for n in self.node_entry.get().split(',') if n.strip()]
        if not nodes:
            messagebox.showerror("Error", "Please enter at least one node name")
            return
        errors = []
        for node in nodes:
            if node in self.graph.nodes:
                errors.append(f"Node '{node}' already exists")
            else:
                self.graph.add_node(node)
        self.update_node_edge_controls()
        self.visualize_graph()
        self.node_entry.delete(0, tk.END)
        if errors:
            messagebox.showerror("Error", "\n".join(errors))

    def remove_node(self):
        nodes = [n.strip() for n in self.node_entry.get().split(',') if n.strip()]
        if not nodes:
            messagebox.showerror("Error", "Please enter at least one node name")
            return
        errors = []
        for node in nodes:
            if node not in self.graph.nodes:
                errors.append(f"Node '{node}' does not exist")
            else:
                self.graph.remove_node(node)
        self.update_node_edge_controls()
        self.visualize_graph()
        self.node_entry.delete(0, tk.END)
        if errors:
            messagebox.showerror("Error", "\n".join(errors))

    def add_edge(self):
        edge_texts = [e.strip() for e in self.edge_entry.get().split(',') if e.strip()]
        if not edge_texts:
            messagebox.showerror("Error", "Please enter at least one edge as 'A-B'")
            return
        errors = []
        for edge_text in edge_texts:
            if '-' not in edge_text:
                errors.append(f"Invalid edge format: '{edge_text}'")
                continue
            u, v = [x.strip() for x in edge_text.split('-', 1)]
            if u not in self.graph.nodes or v not in self.graph.nodes:
                errors.append(f"Both nodes must exist for edge '{u}-{v}'")
                continue
            if self.graph.has_edge(u, v):
                errors.append(f"Edge '{u}-{v}' already exists")
                continue
            self.graph.add_edge(u, v)
        self.visualize_graph()
        self.edge_entry.delete(0, tk.END)
        if errors:
            messagebox.showerror("Error", "\n".join(errors))

    def remove_edge(self):
        edge_texts = [e.strip() for e in self.edge_entry.get().split(',') if e.strip()]
        if not edge_texts:
            messagebox.showerror("Error", "Please enter at least one edge as 'A-B'")
            return
        errors = []
        for edge_text in edge_texts:
            if '-' not in edge_text:
                errors.append(f"Invalid edge format: '{edge_text}'")
                continue
            u, v = [x.strip() for x in edge_text.split('-', 1)]
            if not self.graph.has_edge(u, v):
                errors.append(f"Edge '{u}-{v}' does not exist")
                continue
            self.graph.remove_edge(u, v)
        self.visualize_graph()
        self.edge_entry.delete(0, tk.END)
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
    
    def clear_graph(self):
        self.graph.clear()
        self.update_node_edge_controls()
        self.visualize_graph()

    def update_node_edge_controls(self):
        nodes = list(self.graph.nodes)
        self.start_node_combo['values'] = nodes
        self.goal_node_combo['values'] = [''] + nodes
        if nodes:
            self.start_node_var.set(nodes[0])
            self.goal_node_var.set('')
        else:
            self.start_node_var.set('')
            self.goal_node_var.set('')

def main():
    root = tk.Tk()
    app = GraphTraversalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
