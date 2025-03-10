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




def display(bo):
    for i in range(9):
        if i%3==0 and i!=0:
            print("- - - - - - - - - - - - - ")
        for j in range(9):
            if j%3==0 and j!=0:
                print(" | ", end="")
            if j==8:
                print(bo[i][j])
            else:
                print(str(bo[i][j])+" ", end="")
#displays the board; uses integer division to determine when to print horizontal and vertical lines






@app.route("/", methods = ["get","post"])
def displayGrid():

    if request.method == "POST":

        #retrieve form data and turn it into a list
        form_data = request.form
        userGridData = []
        for r in range(9):
            row = []
            for c in range(9):
                cell_name = f"r{r}c{c}"
                cell_value = form_data.get(cell_name, "")
                if cell_value.isdigit():
                    row.append(int(cell_value))
                else:
                    row.append(0)
            userGridData.append(row)


        #work out how to get all form data and turn it into a list
        #compare this new list with the solution
        #create a new list with indication of correct or not
        #iterate through this new list to decide what colour to highlight cells

        gridData = [
            [[1,False],"","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
        ]
        #check if it is right or wrong
    else:
        ##Generate a new sudoku
        ##Form this as a grid and send the solution and initial grid
        
        gridData=[
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

        empty=[row[:] for row in gridData]
        solution=solve(empty)
        

        
        
    return render_template("solution.html", gridData = gridData, solution = solution)





app.run(debug = True)  









# def insertNum(number, row, col):
#     board[row][col]=number


# def displayErrors(bo, solvedBo):
#     for r in range(9):
#         for c in range(9):
#             if bo[r][c]!=solvedBo[r][c] and bo[r][c]!=0:
#                 print("Error at row "+str(r)+" and column "+str(c)+".")


# def play(board):
#     display(board)
#     empty=[row[:] for row in board]
#     solved=solve(empty)
#     done=False
#     while done==False:
#         choice = input("Do you want to A: enter a number, B: check your inputs, or C: view the solution?")
#         if choice=="A" or choice=="a":
#             num=int(input("Enter number (1 to 9): "))
#             x=int(input("Enter x coordinate (0 to 8): "))
#             y=int(input("Enter y coordinate (0 to 8): "))
#             insertNum(num, x , y)
#             display(board)
#         elif choice=="B" or choice=="b":
#             displayErrors(board, solved)
#         elif choice=="C" or choice=="c":
#             display(solved)
#             done=True
#         else:
#             print("Invalid input")

# play(board)