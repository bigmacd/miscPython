import math

puzzle = [
    [0, 0, 0,  0, 0, 0,  2, 0, 0],
    [0, 8, 0,  0, 0, 7,  0, 9, 0],
    [6, 0, 2,  0, 0, 0,  5, 0, 0],

    [0, 7, 0,  0, 6, 0,  0, 0, 0],
    [0, 0, 0,  9, 0, 1,  0, 0, 0],
    [0, 0, 0,  0, 2, 0,  0, 4, 0],

    [0, 0, 5,  0, 0, 0,  6, 0, 3],
    [0, 9, 0,  4, 0, 0,  0, 7, 0],
    [0, 0, 6,  0, 0, 0,  0, 0, 0]
]

def itFits(xAxis, yAxis, n, puzzle):
    
    # first check the row
    for v in range(0, 9):
        if puzzle[xAxis][v] == n:
            return False

    # now check the column
    for v in range(0, 9):
        if puzzle[v][yAxis] == n:
            return False

    # now check the smaller grid
    # get the index of the upper left hand of the smaller grid
    smallX = (math.floor(xAxis/3)) * 3
    smallY = (math.floor(yAxis/3)) * 3
    for choice1 in range(0, 3):
        for choice2 in range(0, 3):
            if puzzle[smallX + choice1][smallY + choice2] == n:
                return False

    return True


def solvePuzzle(puzzle):

    for xAxis in range(9):    # for each row
        for yAxis in range(9):    # for each column
            if puzzle[xAxis][yAxis] == 0:  # if it is unsolved
                for n in range(1, 10):  # find a solution
                    if itFits(xAxis, yAxis, n, puzzle):  # a solution was found
                        puzzle[xAxis][yAxis] = n   # save it
                        solvePuzzle(puzzle)  # keep solving

                        # if we have exhausted all possibilities,
                        # try, try again.  This resets the cell
                        # and makes that possible
                        puzzle[xAxis][yAxis] = 0
                return
    for row in puzzle:
        print(row)

if __name__ == '__main__':
    solvePuzzle(puzzle)

