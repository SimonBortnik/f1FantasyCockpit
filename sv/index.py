from flask import Flask
from scipy.optimize import linprog
import pandas as pd
import sys
from flask import current_app

app = Flask(__name__)

def prepareData(drivers):
    drivers = drivers.dropna(axis=1, how='all')
    drivers['total'] = drivers['r0'] + drivers['r1'] + drivers['r2'] + drivers['r3'] + drivers['r4'] + drivers['r5'] + drivers['r6'] + drivers['r7'] + drivers['r8'] + drivers['r9'] + drivers['r10']
    return drivers

drivers = pd.read_excel('./data/test.xlsx', index_col=0, header=0) # TODO: Make path OS agnostic
drivers['total'] = drivers['r1'] * 10
app.drivers = prepareData(drivers)


@app.route("/drivers")
def drivers():
    print(current_app.drivers.head(5), file=sys.stderr)
    #print(current_app.drivers.dtypes, file=sys.stderr)
    return "qweqwe"

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