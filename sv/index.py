from flask import Flask
from scipy.optimize import linprog
import pandas as pd
import sys
from flask import current_app

app = Flask(__name__)

def prepareData(drivers):
    drivers.loc[:,'total'] = 0
    
    # Prepare calculation dataframe
    driversPoints = drivers.copy().drop(['cost'], axis=1).dropna(axis=1, how='all').transpose()
    
    # Prepare overview df
    driversOverview = drivers.copy().dropna(axis=1, how='all')

    print(driversOverview.head(3), file=sys.stderr)
    print(driversPoints.head(3), file=sys.stderr)
    return driversOverview, driversPoints

# Takes series of total points scored and returns them multiplied by -1 as array
def getMinimizeArr(totals):
    return totals.apply(lambda x : x * -1).array
drivers = pd.read_excel('./data/test.xlsx', index_col=0, header=0) # TODO: Make path OS agnostic
app.driversOverview, app.driversPoints = prepareData(drivers)


@app.route("/drivers")
def drivers():
    print(app.driversPoints.mean(), file=sys.stderr)
    return "qweqwe"

@app.route("/")
def hello_world():
    c = getMinimizeArr(app.driversPoints.sum())
    print(c, file=sys.stderr)
    print(app.driversOverview['cost'].values, file=sys.stderr)

    A = [[2, 1, 1], [1, 2, 3], [2, 2, 1]]
    b = [2, 5, 6]

    x0_bounds = (0, None)
    x1_bounds = (0, None)
    x2_bounds = (0, None)

    #res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds, x2_bounds])

    #res.fun

    #res.x

    #res.message
    return f'<p></p>'