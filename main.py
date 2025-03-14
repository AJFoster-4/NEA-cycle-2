from flask import Flask, render_template, request

app = Flask(__name__)


def findEmpty(bo):
    for r in range(9):
        for c in range(9):
            if bo[r][c]==0:
                return r,c
    return False
#returns row and column of first empty cell


def checkValid(bo, num, pos):
    #check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i]==num and pos[1]!=i:
            return False

    #check column
    for i in range(len(bo)):
        if bo[i][pos[1]]==num and pos[0]!=i:
            return False

    #check 3x3 grid
    box_x=pos[1]//3
    box_y=pos[0]//3

    for i in range(box_y*3, box_y*3+3):
        for j in range(box_x*3, box_x*3+3):
            if bo[i][j]==num and (i, j)!=pos:
                return False

    return True


def solve(bo):
    find=findEmpty(bo)
    if not find:
        return True  #no empty cells left, puzzle solved
    else:
        row, col=find

    for i in range(1, 10):
        if checkValid(bo, i, (row, col)):
            bo[row][col]=i

            if solve(bo):
                #print("boom")
                return bo

            bo[row][col]=0  #reset the cell and backtrack

    return False  #trigger backtracking



solution=None
gridDataB=None


@app.route("/", methods = ["get","post"])
def displayGrid():

    global solution, gridDataB

    if request.method == "POST":

        #retrieve form data and turn it into a list

        formData = request.form

        userGridData = [
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""]
            ]
        
        for r in range(9):
            for c in range(9):
                cellName = f"r{r}c{c}"
                cellValue = formData.get(cellName, "")
                if cellValue.isdigit():
                    userGridData[c][r]=(int(cellValue))
                else:
                    userGridData[c][r]=0
        
        #compare this new list with the solution and assign True or False depending on whether cells are correct
        for r in range(9):
            for c in range(9):
                if userGridData[r][c]==solution[r][c] and userGridData[r][c]!=0:
                    gridDataB[r][c][0]=userGridData[r][c]
                    gridDataB[r][c][1]=True
                elif userGridData[r][c]==0:
                    pass
                else:
                    gridDataB[r][c][0]=userGridData[r][c]
                    gridDataB[r][c][1]=False
        
    else:
        ##Generate a new sudoku
        ##Form this as a grid and send the solution and initial grid
        
        gridDataA=[
            [8,0,0,4,0,6,0,0,7],
            [0,0,0,0,0,0,4,0,0],
            [0,1,0,0,0,0,6,5,0],
            [5,0,9,0,3,0,7,8,0],
            [0,0,0,0,7,0,0,0,0],
            [0,4,8,0,2,0,1,0,3],
            [0,5,2,0,0,0,0,9,0],
            [0,0,1,0,0,0,0,0,0],
            [3,0,0,9,0,2,0,0,5]
        ]

        gridDataB = [
            [[8, True], [0, None], [0, None], [4, True], [0, None], [6, True], [0, None], [0, None], [7, True]],
            [[0, None], [0, None], [0, None], [0, None], [0, None], [0, None], [4, True], [0, None], [0, None]],
            [[0, None], [1, True], [0, None], [0, None], [0, None], [0, None], [6, True], [5, True], [0, None]],
            [[5, True], [0, None], [9, True], [0, None], [3, True], [0, None], [7, True], [8, True], [0, None]],
            [[0, None], [0, None], [0, None], [0, None], [7, True], [0, None], [0, None], [0, None], [0, None]],
            [[0, None], [4, True], [8, True], [0, None], [2, True], [0, None], [1, True], [0, None], [3, True]],
            [[0, None], [5, True], [2, True], [0, None], [0, None], [0, None], [0, None], [9, True], [0, None]],
            [[0, None], [0, None], [1, True], [0, None], [0, None], [0, None], [0, None], [0, None], [0, None]],
            [[3, True], [0, None], [0, None], [9, True], [0, None], [2, True], [0, None], [0, None], [5, True]]
        ]

        empty=[row[:] for row in gridDataA]
        solution=solve(empty)
        

        
        
    return render_template("solution.html", gridData = gridDataB, solution = solution)





app.run(debug = True)  



#error log- highlighting function

#added [0] to the end of the gridData calls on lines 23 and 25 in html so the numbers are actually displayed (perviously blank cells)
#globalised solution and gridDataB
#new error- everything highlighted red
#error was on lines 91 and 93, changed c and r around
#added lines 99 and 104- this meant that the grid wasn't reset to its original state after the form was submitted
#new error- when a cell is highlighted red, the number inside is replaced with the correct number (very simple fix on line 104, it was a silly mistake)