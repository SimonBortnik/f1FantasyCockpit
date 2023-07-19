from flask import Flask
from scipy.optimize import linprog

app = Flask(__name__)

test = "qweqweqwe" 

@app.route("/")
def hello_world():
    c = [-3, -1, -3]

    A = [[2, 1, 1], [1, 2, 3], [2, 2, 1]]
    b = [2, 5, 6]

    x0_bounds = (0, None)
    x1_bounds = (0, None)
    x2_bounds = (0, None)

    res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds, x2_bounds])

    res.fun

    res.x

    res.message
    return f'<p>{res.x}</p>'