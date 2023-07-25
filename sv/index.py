from flask import Flask
from scipy.optimize import linprog
import pandas as pd
import sys
from flask import current_app

app = Flask(__name__)

def prepareData(drivers, constructors):
    # Prepare calculation dataframe
    driversPoints = drivers.copy().drop(['cost'], axis=1).dropna(axis=1, how='all').transpose() # TODO: Drop race woth no starts
    constructorsPoints = constructors.copy().drop(['cost'], axis=1).dropna(axis=1, how='all').transpose() # TODO: Drop race woth no starts

    # Prepare overview df
    driversOverview = drivers.copy().dropna(axis=1, how='all')
    constructorsOverview = constructors.copy().dropna(axis=1, how='all')
    return driversOverview, driversPoints, constructorsOverview, constructorsPoints

drivers = pd.read_excel('./data/test.xlsx', index_col=0, header=0) # TODO: Make path OS agnostic
constructors = pd.read_excel('./data/test.xlsx', index_col=0, header=0, sheet_name=1) # TODO: Make path OS agnostic
app.driversOverview, app.driversPoints, app.constructorsOverview, app.constructorsPoints = prepareData(drivers, constructors)

# Takes series of total points scored and returns them multiplied by -1 as array
def getMinimizeArr(totals):
    totals = pd.Series(totals)
    return totals.apply(lambda x : x * -1).array

def getCostArray():
    return app.driversOverview['cost'].to_numpy().tolist() + app.constructorsOverview['cost'].to_numpy().tolist()

def getBoundsArray():
    bounds = []
    for x in range(0, 30):
        bounds.append((0, 1))
    return bounds

def getDriversDecisionArray(decision):
    drivers = []
    for x in range(0, 20):
        drivers.append(decision)
    return drivers

def getConstructorsDecisionArray(decision): 
    constructors = []
    for x in range(0, 10):
        constructors.append(decision)
    return constructors

def getDecisionArray():
    return getDriversDecisionArray(1) + getConstructorsDecisionArray(1)

def getResultString(results):
    namesArray = []

    # Handle drivers
    driversResults = results[0:20]
    print(driversResults)
    print('driversResults:^^^^^^^^^^^^')
    for x, res in enumerate(driversResults):
        print(int(driversResults[x]))
        # For some reason which is beyond me the integer decision variable is returned as a float, hence we cast
        if int(driversResults[x]) == 1:
            namesArray.append(app.driversOverview.index[x])
    returnString = 'Optimal driver picks are:'
    for i in range(0, len(namesArray)):
        returnString +=  ' ' + namesArray[i]
        if i < 5:
            returnString += ','

    # Handle constructors
    namesArray = []
    returnString += ' ||| '
    constructorsResults = results[20:29]
    for x in range(len(constructorsResults)):
        if(constructorsResults[x] == 1):
            namesArray.append(app.constructorsOverview.index[x])
    returnString += 'Optimal constructor picks are:'
    for i in range(0, len(namesArray)):
        returnString +=  ' ' + namesArray[i]
        if i < 2:
            returnString += ','
    
    return returnString

def CostString():
    return ''


@app.route("/drivers")
def drivers():
    return "qweqwe"

@app.route("/")
def hello_world():
    c = getMinimizeArr(app.driversPoints.tail(5).sum().to_list() + app.constructorsPoints.tail(5).sum().to_list())

    # Lesser than constraints
    A_ub = [getCostArray()]
    b_ub = [103.4]

    #Equality contraints
    A_eq = [getDriversDecisionArray(1) + getConstructorsDecisionArray(0), getDriversDecisionArray(0) + getConstructorsDecisionArray(1)]
    b_eq = [5, 2]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, 1), integrality=1)

    print(res.x)
    print('Results: ^^^^^^^^^^^^^^^^^^^^')
    return f'<p>{getResultString(res.x)}</p>'
    #return f'<p>Stand by</p>'