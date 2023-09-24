from mip import *

def parse_graph(graph):
    # Parse the input graph
    input = graph.strip().split("\n")

    # n is the number of vertices. m is the number of edges.
    n, m = map(int, input[0].split())

    # Map the remaining lines of string input into the pair of (u,v)
    edges = [tuple(map(int, entry.split())) for entry in input[1:]]

    return n, edges

def binary_model(graph, relaxation):
    """Returns the minimum number of colours using the linear relaxation of the binary model"""

    # Parse the input graph
    # n: number of vertex
    n, edges = parse_graph(graph)

    # Create an integer program for binary model
    model = Model(solver_name=mip.CBC)
    model.verbose = 0

    # Determine variable type based on relaxation param.
    binary_type = CONTINUOUS if relaxation else BINARY

    ## Decision variables
    # 1. x[v][i]: whether vertex v is assigned color i
    x = [
        [model.add_var(var_type=binary_type, lb=0, ub=1) for _ in range(n)]
        for _ in range(n)
    ]

    # 2. y[i]: whether color i is ever used
    y = [model.add_var(var_type=binary_type, lb=0, ub=1) for _ in range(n)]

    ## Objective Function: Minimize the number of colors
    model.objective = minimize(xsum(y[i] for i in range(n)))

    ## Constraints
    # 1. Relate y to x
    for i in range(n):
        for v in range(n):
            model += x[v][i] <= y[i]

    # 2. Each vertex must be assigned exactly one color
    for v in range(n):
        model += xsum(x[v][i] for i in range(n)) == 1

    # 3. Two adjacent vertices cannot have the same color.
    # To deal with relaxed binary program, every vertex of an edge could be assigned a fraction of a color at every iteration.
    # Therefore, the upper bound of this constraint will be y[i].
    for u, v in edges:
        for i in range(n):
            model += x[u][i] + x[v][i] - y[i] <= 0

    model.optimize(relax=relaxation)

    return model.objective_value

def integer_model(graph, relaxation=False):  
    """Returns the minimum number of colours using the linear relaxation of the integer model"""

    # Parse the input graph
    # n: number of vertex
    n, edges = parse_graph(graph)

    # Create an integer program for binary model
    model = Model(solver_name=mip.CBC)
    model.verbose = 0

    # Determine variable type based on relaxation param.
    binary_type = CONTINUOUS if relaxation else BINARY
    integer_type = CONTINUOUS if relaxation else INTEGER

    ## Decision variables:
    # 1. x[v] = color assigned to vertex v
    x = [model.add_var(var_type=integer_type, lb=1, ub=n) for _ in range(n)]

    # 2. y[u][v] = conditional binary variables to check if the vertices u and v have the same color
    y = [[model.add_var(var_type=binary_type) for _ in range(n)] for _ in range(n)]

    # 3. z = maximum value of color assigned
    z = model.add_var(var_type=integer_type, lb=1, ub=n)

    ## Objective function: Minimize the number of colors assigned to maximum number of edges
    model.objective = minimize(z)

    ## Constraints 
    # 1. The color assigned to vertex v must be less than the maximum available colors
    for v in range(n):
        model += x[v] <= z

    # 2. No two adjacent vertices can have the same color.
    M = n + 1         # a big enough number to model OR
    epsilon = 0.001   # a small enough number to compare with
                      # as MIP doesn't support constraints like 'x > 0', we use 'x >= epsilon' instead
    for u, v in edges:
        model += x[u] - x[v] + M * y[u][v] >= epsilon
        model += x[u] - x[v] - M * (1 - y[u][v]) <= -1 * epsilon

    model.optimize(relax=relaxation)

    return model.objective_value
