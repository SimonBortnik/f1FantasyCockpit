from flask import Flask
import pandas as pd
from mip import *

app = Flask(__name__)

def prepareData(drivers, constructors):
    # Prepare calculation dataframe
    driversPoints = drivers.copy().drop(['cost'], axis=1).drop(['r5'], axis=1).dropna(axis=1, how='all').transpose() # TODO: Drop race woth no starts
    constructorsPoints = constructors.copy().drop(['cost'], axis=1).drop(['r5'], axis=1).dropna(axis=1, how='all').transpose() # TODO: Drop race woth no starts

    # Prepare overview df
    driversOverview = drivers.copy().dropna(axis=1, how='all').drop(['r5'], axis=1)
    constructorsOverview = constructors.copy().dropna(axis=1, how='all').drop(['r5'], axis=1)
    return driversOverview, driversPoints, constructorsOverview, constructorsPoints

drivers = pd.read_excel('./data/test.xlsx', index_col=0, header=0) # TODO: Make path OS agnostic
constructors = pd.read_excel('./data/test.xlsx', index_col=0, header=0, sheet_name=1) # TODO: Make path OS agnostic
app.driversOverview, app.driversPoints, app.constructorsOverview, app.constructorsPoints = prepareData(drivers, constructors)

def getCostArray():
    return app.driversOverview['cost'].to_numpy().tolist() + app.constructorsOverview['cost'].to_numpy().tolist()

@app.route('/')
def simplex():
    races = 5
    m = Model()
    x = [ m.add_var(var_type=BINARY, name='driver' + str(i)) for i in range(30) ] # TODO: Correct naming for constructors
    points = app.driversPoints.tail(races).sum().to_list() + app.constructorsPoints.tail(races).sum().to_list()
    cost = getCostArray()
    print(points)
    print(cost)

    # Objective function
    m.objective = maximize(xsum(points[i] * x[i] for i in range(30)))
    # Cost cap
    m += xsum(cost[i] * x[i] for i in range(30)) <= 117.8
    # Pick exactly 5 drivers
    m += xsum(x[i] for i in range(20)) == 5
    # Pick exactly 2 constructors
    m += xsum(x[i + 20] for i in range(10)) == 2

    # Picks that neeed to be included
    #m+= x[0] == 1 #albon
    #m+= x[3] == 1 #alonso
    #m+= x[8] == 0 #norris
    #m+= x[11] == 1 #verstappen
    #m+= x[13] == 0 #ricardo/lawson
    #m+= x[14] == 1 #piastri
    #m+= x[15] == 0 #gasly
    #m+= x[26] == 1 #mcLaren

    m.verbose = 0
    m.optimize()
    selected = [i for i in range(30) if x[i].x >= 0.99]
    print(selected)
    return f'<p>{getResultString(selected, races)}</p>'

def getResultString(results, races):
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
    resultString += ' ||| '
    resultString += f'Projected points are: {getProjectedPoints(driverResults, constructorResults, races)}'
    return resultString

def getTeamCost(driverPicks, constrctorPicks):
    cost = 0
    for i, v in enumerate(driverPicks):
        cost += app.driversOverview.iloc[v]['cost']
    for i, v in enumerate(constrctorPicks):
        cost += app.constructorsOverview.iloc[v - 20]['cost']
    return cost

def getProjectedPoints(driverPicks, constrctorPicks, races):
    pPoints = 0
    for i, v in enumerate(driverPicks):
        pPoints += app.driversPoints.tail(races).mean()[v]
    for i, v in enumerate(constrctorPicks):
        pPoints += app.constructorsPoints.tail(races).mean()[v - 20]
    return pPoints