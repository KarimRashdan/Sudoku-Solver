import numpy as np

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    if not is_valid_initial(sudoku):              # Checks if the initial state of the sudoku is valid
        return np.full((9, 9), -1)
    return solver(sudoku)
    
def solver(sudoku):
    empty_cell_coordinates = empty_cell(sudoku)  
    if not empty_cell_coordinates:                # Tells algorithm to terminate if there are no remaining 0's
        return sudoku

    row, col = empty_cell_coordinates
    num_choices = mrv(sudoku, row, col)

    for num in num_choices:                  
        sudoku[row][col] = num                                     # Attempts to place number in current empty cell
        result = solver(sudoku)          
        if not np.array_equal(result, np.full((9, 9), -1)):        # Checks if Sudoku was unsolvable (returned -1 array)
            return result                                          # If it was solvable, returns the solved Sudoku
        sudoku[row][col] = 0            # If going down this branch does not yield a solution, backtrack

    return np.full((9, 9), -1)          # If no number works at this position, backtrack to previous state

def empty_cell(sudoku):
    min_choices = float('inf')        # The first time the if statement is called, it should always evaluate to true
    min_cell = None
    
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                num_choices = len(mrv(sudoku, i, j))        # Checks how many possibilities are available at said empty cell
                if num_choices < min_choices:               # Checks if the empty cell currently being explored has fewer 
                    min_choices = num_choices               # remaining values than any of the previous ones
                    min_cell = (i, j)
                
    return min_cell

def mrv(sudoku, row, col):
    all_possibilities = list(range(1, 10))
    empty_list = []
    current_subgrid = get_subgrid(sudoku, row, col)
    
    for i in range(9):
        empty_list.append(sudoku[row][i])        # Adds all values in the coordinates' row to the list
        empty_list.append(sudoku[i][col])        # Adds all values in the coordinates' column to the list
        
    empty_list.extend(current_subgrid)           # Adds all values in the coordinates' subgrid to the list
    exclude_empty = [value for value in empty_list if value != 0]  # Removes all 0's from the list
    remove_duplicates = list(set(exclude_empty))                   # Removes any duplicate values in the list
    for i in remove_duplicates:
        all_possibilities.remove(i)              # Removes all values in the list from the list containing numbers 1 through 9
        
    return all_possibilities
        
def get_subgrid(sudoku, row, col):
    start_row = row // 3 * 3                      # Returns the starting row for the following nested for loop
    start_col = col // 3 * 3                      # Returns the starting column for the following nested for loop
    subgrid = []
    for i in range(3):
        for j in range(3):
            subgrid_values = sudoku[start_row + i][start_col + j]
            subgrid.append(subgrid_values)        # Creates a list of all elements in the subgrid
    return subgrid

def is_valid_initial(sudoku):
    for i in range(9):
        if not is_valid_set(sudoku[i, :]) or not is_valid_set(sudoku[:, i]):        # Makes a set of every row and column,
            return False                                                            # Checking every set for duplicate values
        
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not is_valid_set(sudoku[i:i+3, j:j+3]):        # Makes a set of values in a subgrid,
                return False                                  # Checking for duplicate values
            
    return True

def is_valid_set(nums):
    nums = nums[nums != 0]
    return len(nums) == len(set(nums))

def test_sudoku_solver():
    sudoku = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])
    solution = sudoku_solver(sudoku)
    print("Solved Sudoku Puzzle (Test Case 1):")
    print(solution)

test_sudoku_solver()