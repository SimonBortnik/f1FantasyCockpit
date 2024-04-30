from flask import Flask
from flask import request
import pandas as pd
from mip import *
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app) # TODO: Check environment to only allow this in dev

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

def getCostArray():
    return app.driversOverview['cost'].to_numpy().tolist() + app.constructorsOverview['cost'].to_numpy().tolist()

@app.route('/') 
def simplex():
    costCap = float(request.args.get('costCap'))

    ignoreDriversString = request.args.get('ignoreDrivers')
    if(ignoreDriversString is not None):
        ignoreDriversByName = json.loads(ignoreDriversString)
        ignoreDrivers = list(map(nameToIndex, ignoreDriversByName))

    ignoreConstructorsString = request.args.get('ignoreConstructors')
    if(ignoreConstructorsString is not None):
        ignoreConstructorsByName = json.loads(ignoreConstructorsString)
        ignoreConstructors = list(map(teamToIndex, ignoreConstructorsByName))

    includeDriversString = request.args.get('includeDrivers')
    if(includeDriversString is not None):
        includeDriversByName = json.loads(includeDriversString)
        includeDrivers = list(map(nameToIndex, includeDriversByName))

    includeConstructorsString = request.args.get('includeConstructors')
    if(includeConstructorsString is not None):
        includeConstructorsByName = json.loads(includeConstructorsString)
        includeConstructors = list(map(teamToIndex, includeConstructorsByName))    

    races = 5

    m = Model()
    x = [ m.add_var(var_type=BINARY, name='driver' + str(i)) for i in range(30) ] # TODO: Correct naming for constructors
    points = app.driversPoints.tail(races).sum().to_list() + app.constructorsPoints.tail(races).sum().to_list()
    cost = getCostArray()

    # Objective function
    m.objective = maximize(xsum(points[i] * x[i] for i in range(30)))
    # Cost cap
    m += xsum(cost[i] * x[i] for i in range(30)) <= costCap
    # Pick exactly 5 drivers
    m += xsum(x[i] for i in range(20)) == 5
    # Pick exactly 2 constructors
    m += xsum(x[i + 20] for i in range(10)) == 2

    # Ignore picks if instructed
    if(ignoreDriversString is not None):
        for driverIndex in ignoreDrivers:
            m+= x[driverIndex] == 0
    if(ignoreConstructorsString is not None):
        for constructorsIndex in ignoreConstructors:
            m+= x[constructorsIndex] == 0
    
    # Lock in picks if instructed
    if(includeDriversString is not None):
        for driverIndex in includeDrivers:
            m+= x[driverIndex] == 1
    if(includeConstructorsString is not None):
        for constructorsIndex in includeConstructors:
            m+= x[constructorsIndex] == 1

    m.verbose = 0
    m.optimize()

    if(m.status == OptimizationStatus.OPTIMAL):
        selected = [i for i in range(30) if x[i].x >= 0.99]
        print(selected)
        return getResultObject(selected, races)
    
    return 'No solution could be identified. Acquire more paper', 404

def nameToIndex(name):
    print(f'Ignoring {name}')
    return app.driversPoints.columns.get_loc(name)

def teamToIndex(team):
    print(f'Ignoring {team}')
    return app.constructorsPoints.columns.get_loc(team) + 20

def getResultObject(results, races):
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

    # Construct response object
    return {
        'drivers': drivers,
        'constructors': constructors,
        'cost': getTeamCost(driverResults, constructorResults),
        'projectedPoints': getProjectedPoints(driverResults, constructorResults, races)
    }

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