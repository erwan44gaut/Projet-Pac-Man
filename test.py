import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
import math

def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()
   return T
shortestDist = 0

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);
        
LARGEUR = TBL.shape[0]
HAUTEUR = TBL.shape[1]

#region generateMap

def generateWeightMap():
    map = []
    for y in range(HAUTEUR):
        map.append([])
        for x in range(LARGEUR):
            map[y].append(1 if TBL[x][y] == 0 else math.inf)
    return map

def generateVisitedMap():
    map = []
    for y in range(HAUTEUR):
        map.append([])
        for x in range(LARGEUR):
            map[y].append(False)
    return map

def generateGumMap(): # placements des pacgums
    GUM = np.zeros(TBL.shape, dtype=np.int32)
    GUM[4][3] = 1
    GUM[1][1] = 1
    # Met un 1 quand il y a un bonbon
    #    for x in range(LARGEUR):
    #       for y in range(HAUTEUR):
    #          if ( TBL[x][y] == 0):
    #             GUM[x][y] = 1
    return GUM

def generateDistMap():
    map = []
    for y in range(HAUTEUR):
        map.append([])
        for x in range(LARGEUR):
            map[y].append(math.inf)
    return map

#endregion

def checkmMinValue(distMap, weightMap, x, y):
    # Valeur en bas par défaut
    min = weightMap[y+1][x]
    # Check à gauche
    if weightMap[y][x - 1] < min: min = weightMap[y][x - 1]
    # Check en haut
    if weightMap[y-1][x] < min: min = weightMap[y-1][x]
    # Check à droite
    if weightMap[y][x + 1] < min: min = weightMap[y][x + 1]
    
    return min

def wasVisited(visitedMap, x, y):
    return visitedMap[y][x]

def possibleDirections(weightMap, visitedMap, case):
    directions = []
    x = case["x"]
    y = case["y"]
    dist = case["dist"]
    # Check en bas
    if y < HAUTEUR-1 and weightMap[y+1][x] != math.inf and not wasVisited(visitedMap, x, y):
        directions.append({
                "x": x,
                "y": y + 1,
                "dist": dist + weightMap[y + 1][x],
            })
    # Check à gauche
    if x > 0 and weightMap[y][x - 1] != math.inf and not wasVisited(visitedMap, x, y):
        directions.append({
                "x": x - 1,
                "y": y,
                "dist": dist + weightMap[y][x - 1],
            })
    # Check en haut
    if y > 0 and weightMap[y-1][x] != math.inf and not wasVisited(visitedMap, x, y):
        directions.append({
                "x": x,
                "y": y - 1,
                "dist": dist + weightMap[y - 1][x],
            })
    # Check à droite
    if x < LARGEUR-1 and weightMap[y][x + 1] != math.inf and not wasVisited(visitedMap, x, y):
        directions.append({
                "x": x + 1,
                "y": y,
                "dist": dist + weightMap[y][x + 1],
            })
    return directions

def checkPaths(initialX, initialY, case, paths, shortestDist, gumMap, weightMap, visitedMap, distMap):
    x = case["x"]
    y = case["y"]
    dist = case["dist"]

    if gumMap[x][y] == 1:
        if dist < distMap[initialY][initialX]:
            distMap[initialY][initialX] = dist
            shortestDist = dist

    elif dist < shortestDist:
        paths += possibleDirections(weightMap, visitedMap, case)

    visitedMap[y][x] = True
    paths.remove(case)
    if len(paths) == 0: return

    for path in paths:
        checkPaths(initialX, initialY, paths[0], paths, shortestDist, gumMap, weightMap, visitedMap, distMap)


def caseDistFromGum(weightMap, visitedMap, gumMap, distMap, x, y):
    shortestDist = math.inf
    visitedMap = generateVisitedMap()
    case = {"x": x, "y": y, "dist": 0}
    paths = [case] + possibleDirections(weightMap, visitedMap, case)
    checkPaths(x, y, case, paths, shortestDist, gumMap, weightMap, visitedMap, distMap)


def main():
    weightMap = generateWeightMap()
    visitedMap = generateVisitedMap()
    gumMap = generateGumMap()
    distMap = generateDistMap()

    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            if (weightMap[y][x] != math.inf):
                caseDistFromGum(weightMap, visitedMap, gumMap, distMap, x, y)
    
    for y in range(HAUTEUR):
        print(distMap[y])

main()