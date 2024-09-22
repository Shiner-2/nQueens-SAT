from pysat.solvers import Glucose3
import tkinter as tk
import time
import math

# At least one
# 1 | 2 | 3 | 4 (at least one must be true)
def at_least_one(clauses, variables):
    clauses.append(variables)

# At most one
# commander encoding
def at_most_one(clauses, variables, new_variables):
    if len(variables) <= 1: return None
    var = []
    lst = new_variables[len(new_variables)-1]
    k = math.ceil(math.sqrt(len(variables)))
    for i in range(lst+1,lst+k+1):
        var.append(i)
    new_variables += var
    at_most_one_biominal_encoding(clauses, var)
    
    group = []
    commander_pointer = 0
    for i in range(0, len(variables)):
        group.append(variables[i])
        if len(group) == k or i == len(variables) - 1:
            at_most_one_biominal_encoding(clauses, group)
            for j in range(0, len(group)):
                clauses.append([var[commander_pointer], -group[j]])
            group.append(-var[commander_pointer])
            clauses.append(group)
            group = []
            commander_pointer += 1
    
    
def at_most_one_biominal_encoding(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i+1, len(variables)):
            clauses.append([-variables[i], -variables[j]])

# Exactly one
def exactly_one(clauses, variables, new_variables):
    at_least_one(clauses, variables)
    at_most_one(clauses, variables, new_variables)

# Solver
def solver(n):
    # Generate variables
    variables = []
    new_variables = []
    new_variables.append(n*n)
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
        exactly_one(clauses, variables[i], new_variables)
    
    # Exactly one queen in each column
    for i in range(n):
        column = []
        for j in range(n):
            column.append(variables[j][i])
        exactly_one(clauses, column, new_variables)
    
    # At most one queen in each diagonal
    for i in range(n):
        dig = []
        col = i
        row = 0
        while col < n and row < n and row >= 0 and col >= 0 :
            dig.append(variables[row][col])
            col += 1
            row += 1
        # print(dig)
        at_most_one(clauses,dig,new_variables)
    
    for i in range(n):
        dig = []
        col = i
        row = 0
        while col < n and row < n and row >= 0 and col >= 0 :
            dig.append(variables[row][col])
            col -= 1
            row += 1
        # print(dig)
        at_most_one(clauses,dig,new_variables)
    
    for i in range(1,n):
        dig = []
        col = i
        row = n-1
        while col < n and row < n and row >= 0 and col >= 0 :
            dig.append(variables[row][col])
            col += 1
            row -= 1
        # print(dig)
        at_most_one(clauses,dig,new_variables)

    for i in range(n-1):
        dig = []
        col = i
        row = n-1
        while col < n and row < n and row >= 0 and col >= 0 :
            dig.append(variables[row][col])
            col -= 1
            row -= 1
        # print(dig)
        at_most_one(clauses,dig,new_variables)
                         
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

n = 10
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