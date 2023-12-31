## Graph Coloring Problem

Objective: Solving the graph coloring problem using mixed linear programming.
Read more about Graph Coloring here: https://en.wikipedia.org/wiki/Graph_coloring

Graph colouring is the assignment of colours to vertices in a graph, such that no two adjacent vertices are assigned the same colour. The number of colours used should be minimized.
This solution code will model the graph colouring problem using integer programming with two different models.

- Model 1: Use binary variables x[v][i] which indicate if vertex v is assigned colour i.
- Model 2: Use integer variables x[v] which indicate the colour that is assigned to vertex v.

## How to run the program
pip install -r requirements.txt
python solution.py
