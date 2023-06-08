from uib_inf100_graphics import *
import random as r

################
### Initialisering av modellen
################

class Cell:
    def __init__(self, clicked, flagged, value, pos):
        self.clicked = clicked
        self.flagged = flagged
        self.value = value
        self.pos = pos

    def __str__(self):
        return f"{self.clicked}|{self.flagged}|{self.value}|{self.pos}"

def app_started(app):
    app.boardSize = [20, 20]
    app.mineNum = 50
    app.debug_mode = False
    init(app)

def init(app):
    # Gjør klart for et nytt spill
    app.state = "pregame"
    app.board = new_default_board(app.boardSize)
    app.boardSpace = [10, 30, app.width - 10, app.height - 10]
    app.gridPos = [-1, -1]
    app.x = 0
    app.y = 0

def new_default_board(size):
    board = []
    for y in range(size[1]):
        for x in range(size[0]):
            board.append(Cell(False, False, 0, [x, y]))
        
    return board
### Hjelpefunksjoner for å initalisere modellen


################
### Kontrollere
################

def key_pressed(app, event):
    if event.key == "d":
        app.debug_mode = not app.debug_mode
    if event.key == "Space":
        if app.state == "gameover":
            init(app)
            print("restarting")
        else:
            mark_cell(app)
    
def mouse_moved(app, event):
    app.x = event.x
    app.y = event.y
    
    x1 = app.boardSpace[0]
    y1 = app.boardSpace[1]
    x2 = app.boardSpace[2]
    y2 = app.boardSpace[3]

    if app.x in range(x1, x2 + 1):
        if app.y in range(y1, y2 + 1):
            app.gridPos = get_grid_pos(app, x1, y1, x2, y2)

def mouse_pressed(app, event):
    print("click")
    x1 = app.boardSpace[0]
    y1 = app.boardSpace[1]
    x2 = app.boardSpace[2]
    y2 = app.boardSpace[3]

    if app.x in range(x1, x2 + 1):
        if app.y in range(y1, y2 + 1):
            app.gridPos = get_grid_pos(app, x1, y1, x2, y2)
            cell = app.board[(app.gridPos[1] * app.boardSize[1]) + app.gridPos[0]]
            if app.state == "pregame" and not cell.flagged:
                cell.clicked = True
                generate_board(app)
                app.state = "game"
            elif app.state == "game" and not cell.flagged:
                if cell.value == 0:
                    click_around(app, cell)
                else:
                    if cell.value == -1:
                        app.state = "gameover"
                    cell.clicked = True
### Hjelpefunksjoner for kontrollere

def get_grid_pos(app, x1, y1, x2, y2):
    rows = app.boardSize[1]
    cols = app.boardSize[0]
    mousePos = [app.x, app.y]

    cell_width = (x2 - x1) / cols
    cell_height = (y2 - y1) / rows
    tempX = x1
    tempY = y1

    pos = [-1, -1]
    while tempX < mousePos[0]:
        tempX += cell_width
        pos[0] += 1
    while tempY < mousePos[1]:
        tempY += cell_height
        pos[1] += 1
    return pos

def generate_board(app):
    cell = app.board[(app.gridPos[1] * app.boardSize[1]) + app.gridPos[0]]
    minesPos = generate_mines(app, cell)
    for minePos in minesPos:
        app.board[minePos].value = -1

    for cell in app.board:
        if cell.value != -1:
            count_mines(app, cell)
    
    cell = app.board[(app.gridPos[1] * app.boardSize[1]) + app.gridPos[0]]
    click_around(app, cell)

def generate_mines(app, cell):
    minesPos = []
    for yMod in range(-1, 2):
        for xMod in range(-1, 2):
            minesPos.append(((cell.pos[1] + yMod) * app.boardSize[1]) + (cell.pos[0] + xMod))
    for i in range(app.mineNum):
        pos = r.randrange(0, len(app.board) - 2)
        while pos in minesPos:
            pos = r.randrange(0, len(app.board) - 2)
        minesPos.append(pos)
    for i in range(9):
        minesPos.pop(0)
    minesPos.sort()
    return minesPos
    
def count_mines(app, cell):
    for yMod in range(-1, 2):
        if cell.pos[1] + yMod >= 0 and cell.pos[1] + yMod <= app.boardSize[1] - 1:
            for xMod in range(-1, 2):
                if cell.pos[0] + xMod >= 0 and cell.pos[0] + xMod <= app.boardSize[0] - 1:
                    if app.board[((cell.pos[1] + yMod) * app.boardSize[1]) + (cell.pos[0] + xMod)].value == -1:
                        cell.value += 1

def count_flags(app, cell):
    flags = 0
    for yMod in range(-1, 2):
        if cell.pos[1] + yMod >= 0 and cell.pos[1] + yMod <= app.boardSize[1] - 1:
            for xMod in range(-1, 2):
                if cell.pos[0] + xMod >= 0 and cell.pos[0] + xMod <= app.boardSize[0] - 1:
                    if app.board[((cell.pos[1] + yMod) * app.boardSize[1]) + (cell.pos[0] + xMod)].flagged:
                        flags += 1
    return flags

def click_around(app, cell):
    for yMod in range(-1, 2):
        if cell.pos[1] + yMod >= 0 and cell.pos[1] + yMod <= app.boardSize[1] - 1:
            for xMod in range(-1, 2):
                if cell.pos[0] + xMod >= 0 and cell.pos[0] + xMod <= app.boardSize[0] - 1:
                    newCell = app.board[((cell.pos[1] + yMod) * app.boardSize[1]) + cell.pos[0] + xMod]
                    if not newCell.flagged:
                        if newCell.value == 0 and not newCell.clicked:
                            newCell.clicked = True
                            click_around(app, newCell)
                        else:
                            if newCell.value == -1:
                                app.state = "gameover"
                            newCell.clicked = True

def mark_cell(app):
    cell = app.board[(app.gridPos[1] * app.boardSize[1]) + app.gridPos[0]]
    if not cell.flagged:
        if not cell.clicked:
            cell.flagged = True
        else:
            if count_flags(app, cell) == cell.value:
                click_around(app, cell)
    else:
        cell.flagged = False

################
### Visning
################

def redraw_all(app, canvas):
    # debug-info

    # brette
    draw_board(canvas, app.boardSpace[0], app.boardSpace[1], app.boardSpace[2], app.boardSpace[3], app.gridPos,
               app.boardSize, board=app.board, debug_mode=app.debug_mode)
    # game over
    if (app.state == "gameover"):
        canvas.create_text(app.width/2, app.height/2 - 10,
                           text="Game Over", font="Arial 26", fill="black")
        canvas.create_text(app.width/2, app.height/2 + 15,
                           text="Press space to restart", font="Arial 12", fill="black")

### Hjelpefunksjoner for visningen

def get_color(value):
    # < 0: eple, 0: tom rute, > 0: slange
    colors = ["white", "blue", "green", "red", "darkblue", "darkred", "darkcyan", "black", "darkgray"]
    return colors[value]

def draw_board(canvas, x1, y1, x2, y2, gridPos, gridSize, board, debug_mode):
    cell_width = (x2 - x1) / gridSize[0]
    cell_height = (y2 - y1) / gridSize[1]


    for row in range(gridSize[0]):
        for col in range(gridSize[1]):
            cell = board[(row * gridSize[1]) + col]
            clicked = cell.clicked
            value = cell.value
            pos = cell.pos
            # Tegne rektangelet
            cell_x1 = x1 + col * cell_width
            cell_y1 = y1 + row * cell_height
            cell_x2 = cell_x1 + cell_width
            cell_y2 = cell_y1 + cell_height
            
            color = get_color(value)
            if not clicked:
                if cell.flagged:
                    canvas.create_rectangle(cell_x1, cell_y1, cell_x2, cell_y2, fill="red")
                else:
                    canvas.create_rectangle(cell_x1, cell_y1, cell_x2, cell_y2, fill="lightgray")
            else:
                canvas.create_rectangle(cell_x1, cell_y1, cell_x2, cell_y2, fill="white")
                if value > 0:
                    canvas.create_text(cell_x1 + (cell_width / 2), cell_y1 + (cell_height / 2),
                                       text=f"{value}", fill=color, font="Arial 12 bold")
                elif value == -1:
                    canvas.create_rectangle(cell_x1, cell_y1, cell_x2, cell_y2, fill="black")
            if debug_mode:
                canvas.create_text(cell_x1 + (cell_width / 2), cell_y1 + 9 + (cell_height / 2),
                                              text=f"{pos[0],pos[1]}", font="Arial 5")
                canvas.create_text(cell_x1 + (cell_width / 2), cell_y1 - 9 + (cell_height / 2),
                                              text=f"{(row * gridSize[1]) + col}", font="Arial 5")
                if not clicked:
                    canvas.create_text(cell_x1 + (cell_width / 2), cell_y1 + (cell_height / 2),
                                       text=f"{value}", fill=color, font="Arial 12 bold")
    if debug_mode:
        canvas.create_text(50, 15, text=f"{gridPos}", fill="blue", font="Arial 12 bold")


################
### Kjør programmet
################

if __name__ == '__main__':
    run_app(width=520, height=540, title="Minesweeper")