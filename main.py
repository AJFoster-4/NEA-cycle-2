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
gridData=None


@app.route("/", methods=["get","post"])
def displayGrid():

    global solution, gridData

    if request.method=="POST":

        action=request.form.get("action")

        if action=="showSolution":

            for r in range(9):
                for c in range(9):
                    gridData[r][c][0]=solution[r][c]
                    gridData[r][c][1]=True

        else:
        
            #retrieve form data and turn it into a list (userGridData)

            formData=request.form

            userGridData=[
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
                        userGridData[r][c]=int(cellValue)
                    else:
                        userGridData[r][c]=0
            
            #compare this new list with the solution and assign True or False depending on whether cells are correct
            for r in range(9):
                for c in range(9):
                    if userGridData[r][c]==solution[r][c] and userGridData[r][c]!=0:
                        gridData[r][c][0]=userGridData[r][c]
                        gridData[r][c][1]=True
                    elif userGridData[r][c]==0:
                        pass
                    else:
                        gridData[r][c][0]=userGridData[r][c]
                        gridData[r][c][1]=False
        
    else:
        
        gridDataRaw=[
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

        gridData=[
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]]
        ]

        #converts grid data from 2D to 3D, where the first index is the number and the second index is a boolean indicating whether the cell is filled
        for r in range(9):
            for c in range(9):
                if gridDataRaw[r][c]!=0:
                    gridData[r][c][0]=gridDataRaw[r][c]
                    gridData[r][c][1]=True
                else:
                    gridData[r][c][0]=gridDataRaw[r][c]
                    gridData[r][c][1]=None


        empty=[row[:] for row in gridDataRaw]
        solution=solve(empty)
        
    return render_template("solution.html", gridData=gridData)





app.run(debug = True)