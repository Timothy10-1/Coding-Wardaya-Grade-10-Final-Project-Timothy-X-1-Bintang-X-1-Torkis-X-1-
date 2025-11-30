import random
import curses

def init_board():
    board = [[0] * 4 for _ in range(4)]
    addnewtiles(board)
    addnewtiles(board)
    return board

def addnewtiles(board):
    empty = [(ra, ch) for ra in range(4) for ch in range(4) if board[ra][ch] == 0]
    if not empty:
        return
    ra, ch = random.choice(empty)
    board[ra][ch] = 4 if random.random() < 0.1 else 2

def compress(roww):
    new = [x for x in roww if x != 0]
    new += [0] * (4 - len(new))
    return new

def merge(roww):
    score = 0
    for i in range(3):
        if roww[i] != 0 and roww[i] == roww[i+1]:
            roww[i] *= 2
            score += roww[i]
            roww[i+1] = 0
    return roww, score

def move_left(board):
    score = 0
    new_board = []
    for roww in board:
        ch = compress(roww)
        m, s = merge(ch)
        ch = compress(m)
        new_board.append(ch)
        score += s
    return new_board, score

def rotate_board(board):
    return [list(ra) for ra in zip(*board[::-1])]

def move_right(board):
    board = [roww[::-1] for roww in board]
    board, score =  move_left(board)
    board = [roww[::-1] for roww in board]
    return board, score

def move_up(board):
    board = rotate_board(board)
    board, score = move_left(board)
    board = rotate_board(rotate_board(rotate_board(board)))
    return board, score

def move_down(board):
    board = rotate_board(board)
    board, score = move_right(board)
    board = rotate_board(rotate_board(rotate_board(board)))
    return board, score

def moves_available(board):
    if any(0 in roww for roww in board):
        return True
    for ra in range(4):
        for ch in range(4):
            if ch < 3 and board[ra][ch] == board[ra][ch+1]:
                return True
            if ra < 3 and board[ra][ch] == board[ra+1][ch]:
                return True
    return False

def draw_board(stdscr, board, score):
    stdscr.clear()
    stdscr.addstr("THE 2048 GAME (Pls use arrow keys to play, press Q (no caps lock) to quit the game)\n")
    stdscr.addstr(f"Score: {score}\n\n")

    for roww in board:
        for value in roww:
            cell = f"{value}".center(6) if  value != 0 else " ".center(6)
            stdscr.addstr(cell)
        stdscr.addstr("\n")
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    board = init_board()
    score = 0

    while True:
        draw_board(stdscr, board, score)
        key = stdscr.getch()

        if key == ord('q'):
            break

        moved = False

        if key == curses.KEY_LEFT:
            new_board, s = move_left(board)
            moved = new_board != board
        elif key == curses.KEY_RIGHT:
            new_board, s = move_right(board)
            moved = new_board, s = move_right(board)
        elif key == curses.KEY_UP:
            new_board, s = move_up(board)
            moved = new_board, s = move_up(board)
        elif key == curses.KEY_DOWN:
            new_board, s = move_down(board)
            moved = new_board, s = move_down(board)
        else:
            continue

        if moved:
            board = new_board
            score += s
            addnewtiles(board)

        if not moves_available(board):
            draw_board(stdscr, board, score)
            stdscr.addstr("\nGAME OVER! NICE TRY! Press Q (no caps lock) to quit this game.\n")
            while stdscr.getch() != ord('q'):
                pass
            break

if __name__ == "__main__":
    curses.wrapper(main)