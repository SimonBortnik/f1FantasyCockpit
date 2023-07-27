from flask import Flask
from scipy.optimize import linprog
import pandas as pd
from mip import *

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

@app.route("/old")
def hello_world():
    c = getMinimizeArr(app.driversPoints.tail(5).sum().to_list() + app.constructorsPoints.tail(5).sum().to_list())

    # Lesser than constraints
    A_ub = [getCostArray()]
    b_ub = [102.9]

    #Equality contraints
    A_eq = [getDriversDecisionArray(1) + getConstructorsDecisionArray(0), getDriversDecisionArray(0) + getConstructorsDecisionArray(1)]
    b_eq = [5, 2]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, 1), integrality=1, method='highs')

    print('Status: ' + str(res.status))
    print(res.x)
    print('Results: ^^^^^^^^^^^^^^^^^^^^')
    return f'<p>{getResultString(res.x)}</p>'
    #return f'<p>Stand by</p>'

@app.route('/')
def simplex():
    m = Model()
    x = [ m.add_var(var_type=BINARY, name='driver' + str(i)) for i in range(30) ]
    points = app.driversPoints.tail(5).sum().to_list() + app.constructorsPoints.tail(5).sum().to_list()
    cost = getCostArray()
    print(points)
    print(cost)

    m.objective = maximize(xsum(points[i] * x[i] for i in range(30)))
    m += xsum(cost[i] * x[i] for i in range(30)) <= 103.4
    m += xsum(x[i] for i in range(20)) == 5
    m += xsum(x[i + 20] for i in range(10)) == 2

    m.optimize()
    selected = [i for i in range(30) if x[i].x >= 0.99]
    print(selected)
    return f'<p>{newgetResultString(selected)}</p>'

def newgetResultString(results):
    # Get sub arrays for drivers and constructors
    driverResults = results[0:5]
    constructorResults = results[5:7]
    
    # Get names for selected drivers and constructors
    drivers = []
    constructors = []
    for i, v in enumerate(driverResults):
        drivers.append(app.driversOverview.index[v])
        print(app.driversOverview.index[v])
    for i, v in enumerate(constructorResults):
        constructors.append(app.constructorsOverview.index[v - 20])
        print(app.constructorsOverview.index[v - 20])
    
    # Construct human readable string
    resultString = 'Optimal drivers are:'
    for i, name in enumerate(drivers):
        resultString += ' ' + name
        if(i < 4):
            resultString += ','
    resultString += ' ||| '
    resultString += 'Optimal constructors are:'
    for i, name in enumerate(constructors):
        resultString += ' ' + name
        if(i < 1):
            resultString += ','
    resultString += ' ||| '
    resultString += 'Asset cost are: ' + str(getTeamCost(driverResults, constructorResults)) + ' mil. $'
    print(resultString)
    return resultString

def getTeamCost(driverPicks, constrctorPicks):
    cost = 0
    for i, v in enumerate(driverPicks):
        cost += app.driversOverview.iloc[v]['cost']
    for i, v in enumerate(constrctorPicks):
        cost += app.constructorsOverview.iloc[v - 20]['cost']
    return cost