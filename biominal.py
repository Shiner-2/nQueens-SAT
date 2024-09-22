from pysat.solvers import Glucose3
import tkinter as tk
import time

# At least one
# 1 | 2 | 3 | 4 (at least one must be true)
def at_least_one(clauses, variables):
    clauses.append(variables)

# At most one
# 1 & 2 (no pair of variables can be true) so add -1 | -2 to clauses
def at_most_one(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i+1, len(variables)):
            clauses.append([-variables[i], -variables[j]])

# Exactly one
def exactly_one(clauses, variables):
    at_least_one(clauses, variables)
    at_most_one(clauses, variables)

# Solver
def solver(n):
    # Generate variables
    variables = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(i * n + j + 1)
        variables.append(row)
    # print(variables)
    
    # Generate clauses
    clauses = []
    
    # Exactly one queen in each row
    for i in range(n):
        exactly_one(clauses, variables[i])
    
    # Exactly one queen in each column
    for i in range(n):
        column = []
        for j in range(n):
            column.append(variables[j][i])
        exactly_one(clauses, column)
    
    # At most one queen in each diagonal
    for i in range(n):
        for j in range(n): # Choose a point on board
            for k in range(1, n): # Choose a distance from point
                if i + k < n and j + k < n: # left to right diagonal
                    at_most_one(clauses, [variables[i][j], variables[i + k][j + k]])
                if i + k < n and j - k >= 0: # right to left diagonal
                    at_most_one(clauses, [variables[i][j], variables[i + k][j - k]])
                    
    # print(clauses)
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)
        
    if solver.solve() == True:
        model = solver.get_model()
        return model
    else:
        return None

# draw board on console base on solution
def draw_board_on_console(n, solution):
    for i in range(n):
        for j in range(n):
            if solution[i * n + j] > 0:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
       
# draw board on GUI base on solution 
def draw_board_on_gui(n, solution):
    window = tk.Tk()
    window.title("N-Queens Solution")
    canvas = tk.Canvas(window, width=n*50, height=n*50)
    canvas.pack()

    for i in range(n):
        for j in range(n):
            x1, y1 = j * 50, i * 50
            x2, y2 = x1 + 50, y1 + 50
            color = "white" if (i + j) % 2 == 0 else "black"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            if solution[i * n + j] > 0:
                canvas.create_text(x1 + 25, y1 + 25, text="Q", font=("Arial", 24), fill="red")

    window.mainloop()

# start the timer
start_time = time.time()

n = 8
solution = solver(n)

# end the timer
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.4f} seconds")

# print(solution)
if solution is not None:
    draw_board_on_console(n, solution)
    draw_board_on_gui(n, solution)
else:
    print("No solution found.")