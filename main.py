import tkinter as tk
from tkinter import ttk

# Function to calculate the minimum index of an array
def minVal(arr):
    minVal = 0
    for i in range(len(arr)):
        if int(arr[i]) < int(arr[minVal]):
            minVal = i
    return minVal

# Function to calculate the maximum index of an array
def maxVal(arr):
    maxVal = 0
    for i in range(len(arr)):
        if int(arr[i]) > int(arr[maxVal]):
            maxVal = i
    return maxVal

# Function to return the minimum value of two numbers
def minof2(a, b):
    return a if a < b else b

# Function to calculate the minimum cash flow
def minCashFlow(amount, result_text):
    mxCredit = maxVal(amount)
    mxDebit = minVal(amount)

    if amount[mxCredit] == 0 and amount[mxDebit] == 0:
        return

    min = minof2(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -= min
    amount[mxDebit] += min

    result_text.append(f"Person {mxDebit + 1} pays {min} to Person {mxCredit + 1}")
    minCashFlow(amount, result_text)

# Function to handle the calculation and display results
def calculate_and_display_results():
    global num_people, matrix, result_label

    try:
        # Read the input values from the matrix
        new_matrix = []
        for i in range(num_people):
            matrixRow = []
            for j in range(num_people):
                value = matrix[i][j].get()
                if not value.isdigit() and value != '':
                    raise ValueError("Invalid input! Please enter valid numbers.")
                matrixRow.append(int(value))
            new_matrix.append(matrixRow)

        # Calculate the net amount for each person
        amount = [0 for _ in range(num_people)]
        for i in range(num_people):
            for j in range(num_people):
                amount[i] += new_matrix[j][i] - new_matrix[i][j]

        # Clear previous results
        result_label.config(text="", fg="white")

        # Check if no transactions are needed
        if all(a == 0 for a in amount):
            result_label.config(text="No transactions are needed.", fg="green")
            return

        result_text = []
        minCashFlow(amount, result_text)

        # Display results
        result_label.config(text="\n".join(result_text), fg="white")

    except ValueError as e:
        result_label.config(text=str(e), fg="red")

# Function to set up the matrix input fields
def setup_matrix():
    global num_people, matrix, result_label

    num_people = int(people_spinbox.get())

    # Clear previous matrix frame
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    matrix = []
    for i in range(num_people):
        matrixRow = []
        for j in range(num_people):
            entry = tk.Entry(matrix_frame, width=5)
            entry.grid(row=i, column=j, padx=5, pady=5)
            if i == j:
                entry.insert(0, 0)
                entry.config(state='disabled')
            matrixRow.append(entry)
        matrix.append(matrixRow)

    calculate_button = ttk.Button(root, text="Calculate", command=calculate_and_display_results)
    calculate_button.grid(row=4, column=1, pady=10)

    result_label.config(text="")  # Clear any previous result

# Create the main window
root = tk.Tk()
root.geometry("600x400")
root.title("CashFlow Minimizer")

style = ttk.Style()
style.theme_use('clam')

title = tk.Label(root, text="CashFlow Minimizer", font=("Helvetica", 16), fg="black")
title.grid(row=0, column=0, columnspan=3, pady=10)

people_label = tk.Label(root, text="How many people?", fg="black")
people_label.grid(row=1, column=0, pady=10)

people_spinbox = ttk.Spinbox(root, from_=2, to=10, width=5)
people_spinbox.grid(row=1, column=1, pady=10)

submit_button = ttk.Button(root, text="Submit", command=setup_matrix)
submit_button.grid(row=1, column=2, pady=10)

matrix_frame = tk.Frame(root)
matrix_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

result_label = tk.Label(root, text="", fg="black", justify="left")
result_label.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
