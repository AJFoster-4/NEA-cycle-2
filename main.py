from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods = ["get","post"])
def displayGrid():

    if request.method == "POST":
        #work out how to get all form data and turn it into a list
        #compare this new list with the solution
        #create a new list with indication of correct or not

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

        solution = [
            ["1","","","","","","","",""],
            ["","","","3","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","7","","",""],
            ["","","","","","","","",""],
            ["","","","4","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
        ]
        gridData = [
            ["1","","","","","","","",""],
            ["","","","3","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","7","","",""],
            ["","","","","","","","",""],
            ["","","","4","","","","",""],
            ["","","","","","","","",""],
            ["","","","","","","","",""],
        ]
        
        
    return render_template("solution.html", gridData = gridData, solution = solution)






app.run(debug = True)