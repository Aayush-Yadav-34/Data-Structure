# Data-Structure
# BFS vs Iterative DFS Graph Traversal Visualizer

This is a Python Tkinter GUI application to visualize and compare Breadth-First Search (BFS) and Iterative Depth-First Search (DFS) traversals on a user-defined directed graph. The tool allows you to add/remove nodes and edges, run both algorithms, and see their traversal paths, performance metrics, and a side-by-side comparison.

## Features

- **Add/Remove Nodes and Edges:** Easily build your own graph.
- **Visual Graph Display:** See your graph and traversal progress visually (no arrowheads).
- **Run BFS and DFS:** Execute either algorithm and view the traversal path and stats.
- **Compare Algorithms:** See a side-by-side comparison of BFS and DFS on your graph.
- **Performance Metrics:** View nodes visited, execution time, memory used, and path length.
- **Example Input Provided:** The node and edge entry fields are pre-filled with an example graph for quick testing and traversal.

## How to Use

1. **Install Requirements:**
   - Python 3.x
   - `networkx`, `matplotlib`, `graphviz`, `Pillow`
   - Graphviz system package (for rendering)

2. **Run the Application:**
   ```
   python BFSvsDFS.py
   ```

3. **Build Your Graph:**
   - Use the "Node" and "Edge" fields to add/remove nodes and edges.
   - Example input is already provided in the entry fields for quick testing.

4. **Set Traversal Parameters:**
   - Select a start node (and optionally a goal node).

5. **Run Traversals:**
   - Click "Run BFS", "Run DFS", or "Compare Both" to see results and visualizations.

6. **Clear/Reset:**
   - Use "Clear Graph" or "Clear Results" as needed.

## Example Input

- **Nodes:**  
  `A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z`
- **Edges:**  
  `A-B,B-C,C-D,D-E,E-F,E-P,F-G,P-G,G-H,G-X,H-I,H-Z,B-O,B-R,K-L,A-K,L-R,K-J,J-Q,J-S,J-Y,Q-T,Y-T,Y-W,W-A,T-M,T-U,U-N,N-V`

These are pre-filled in the GUI for you to try out traversal and comparison immediately.

---

**Note:**  
Make sure Graphviz is installed and available in your system PATH for the visualization to work.

---
