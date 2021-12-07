from copy import deepcopy


# board = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]


def board_validity_test(board):
    '''
    Returns True if there are no conflicts within the given board, False otherwise.
    '''
    # checking for duplicate numbers
    # horizontal
    for i in range(9):
        for n in range(1, 10):
            if board[i].count(n) > 1:
                return False

    # vertical
    for i in range(9):
        for n in range(1, 10):
            if [board[j][i] for j in range(9)].count(n) > 1:
                return False

    # box
    for box_x in range(0, 9, 3):
        for box_y in range(0, 9, 3):
            for num in range(1, 10):
                num_count = 0
                for row in range(box_y, box_y + 3):
                    for col in range(box_x, box_x + 3):
                        if board[row][col] == num:
                            num_count += 1
                            if num_count > 1:
                                return False
    return True


def find_null(board) -> tuple:
    '''
    Returns the (x,y) coords of first 0 in given board;
    Returns None if there are no 0's.
    '''

    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                return (x, y)
    return None


def is_ok(board, num, pos: tuple):
    '''
    Returns True if it is a valid move to put num at pos on the given board, False otherwise.
    '''

    x, y = pos

    # is empty?
    if board[y][x] != 0:
        return False

    # horizontal
    if num in board[y]:
        return False

    # vertical
    for row in range(9):
        if board[row][x] == num:
            return False

    # box
    box_x, box_y = x//3 * 3, y//3 * 3
    for row in range(box_y, box_y + 3):
        for col in range(box_x, box_x + 3):
            if board[row][col] == num:
                return False
    return True


def get_prev_pos(x, y):
    '''
    Returns the coords of position before given position (x, y).

    #1 The previous position is 1 to the left (x - 1) from the given position (x, y)\n
    #2 If '1 to the left' is not a valid position (bad index), the previous position is the last square of the previous row.

    If prev. position selected based on #1 and #2 is not valid (occupied or bad index), rule #1 is again applied.

    Returns None if there is no valid previous position.
    '''

    prev_x, prev_y = x-1, y  # #1 rule
    if prev_x < 0:  # #2 rule
        prev_y -= 1
        prev_x = prev_x % 9
    while not is_valid_pos(prev_x, prev_y):
        prev_x = prev_x - 1  # '1 to the left' - #1 rule
        if prev_x < 0:  # bad index - #2 rule
            prev_y -= 1
            prev_x %= 9
        if prev_y < 0:  # no valid previous position
            return None
    return prev_x, prev_y


def is_valid_pos(x, y):
    '''
    Returns True if given position is not occupied (in global board) and has no negative indexes
    '''

    global board
    if x < 0 or y < 0:  # negative indexes
        return False
    if board[y][x] != 0:   # occupied in global board
        return False
    return True


def print_board(board):
    '''
    Prints the given board (2D array 9, 9) nicely
    '''

    board_to_print = deepcopy(board)
    out = []
    for i in range(9):
        for j in range(9):
            board_to_print[i][j] = str(board_to_print[i][j])

    for row in board_to_print:
        out.append([' '.join(row[i:i+3]) for i in range(0, 9, 3)])
    out = [' │ '.join(row) for row in out]

    i = 1
    for row in out:
        print(row.replace('0', '.'))
        if i % 3 == 0 and i != 9:
            print('──────┼───────┼──────')
        i += 1


def main():
    solutions = []  # list to store all found solutions

    if find_null(board) is None:  # if there is no empty space on the board, it is solved
        print('This board is solved.')
        return board

    while True:
        solution = deepcopy(board)

        # run loop when there are still empty spaces on the board
        while find_null(solution) is not None:
            x, y = find_null(solution)  # coords of the first empty space

            need_new_zero = False
            # run loop when the (x, y) square is still empty
            while not need_new_zero:
                for n in range(solution[y][x] + 1, 10):
                    # clear the (x, y) square, if a wrong number was assigned to it before - needed for the next line's is_ok() function
                    solution[y][x] = 0
                    if is_ok(solution, n, (x, y)):  # test if n is a valid number for (x, y) square
                        solution[y][x] = n
                        # if the board is still unfinished we need to find the next 0 and repeat the process
                        if find_null(solution) is not None or solution not in solutions:
                            need_new_zero = True
                            break
                # if no number from 1 - 9 is suitable, the previously assigned number(s) are not correct - backtrack
                else:
                    solution[y][x] = 0
                    try:  # backtrack to the previous square
                        x, y = get_prev_pos(x, y)
                    except TypeError:  # we exhausted all options
                        # print what happened & return the found solutions
                        if len(solutions) > 0:
                            print('All solutions found')
                            return solutions
                        else:
                            print('Board has no solutions')
                            return None
        solutions.append(solution)  # append found solution to solutions list
        print_board(solution)  # show the solved board

        # find next solution on request of the user
        input('Press enter for another solution...\n')


if __name__ == '__main__':
    # get a puzzle at https://qqwing.com/generate.html
    board = input(
        'Enter a sudoku puzzle to solve\n(example: 6.871.....4...21.......4.....6...7.........982.9......7..4...59...8..4...2416....)\n>')
    if len(board) != 81:
        print('Invalid puzzle, using example input')
        board = '6.871.....4...21.......4.....6...7.........982.9......7..4...59...8..4...2416....'
    board = [int(i) for i in list(board.replace('.', '0'))]
    board = [board[i:i+9] for i in range(0, len(board), 9)]

    if board_validity_test(board):  # test if the board is a valid sudoku
        print_board(board)
        print('The above board is a valid sudoku.')
        print('Finding solutions...\n')
        main()
    else:
        print_board(board)
        print('The above board is not a valid sudoku!')
