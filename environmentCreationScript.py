import copy
import csv
import os
import subprocess
import random
import numpy as np
import pandas
import scipy.stats as stats

_itrCountPositionSearchProblem = 10
_itrCountCornersProblem = 10
_itrCountFoodSearchProblem = 1
_maxFoodCount = 11
_layoutCount = 10
_algos = ["dfs", "bfs", "ucs", "astar", "bds", "hbds"]
_layouts = ["tiny", "small", "medium", "big"]
_layoutSizes = {"tiny": (5, 10), "small": (10, 15), "medium": (15, 20), "big": (20, 25)}
_layoutWallCount = {"tiny": 20, "small": 50, "medium": 100, "big": 125}
_layoutType = {"PositionSearchProblem": "Maze", "CornersProblem": "Corners", "FoodSearchProblem": "Search"}
_problems = ["PositionSearchProblem", "CornersProblem", "FoodSearchProblem"]

dataGroups = {"PositionSearchProblem": {}, "CornersProblem": {}, "FoodSearchProblem": {}}
tStats_hbds = {}
tStats_bds = {}


def isPathAvailable(emptyCells, wallCells, height, width):
    """
    check if random generated maze has path.
    """
    dir = ((0, -1), (0, 1), (-1, 0), (1, 0))
    visitedCells = []
    queue = []
    queue.append(emptyCells[0])
    while len(queue) > 0:
        cell = queue.pop(0)
        visitedCells.append(cell)
        for _x, _y in dir:
            x, y = _x + cell[0], _y + cell[1]
            if 0 <= x < height and 0 <= y < width and (x, y) not in wallCells and (x, y) not in visitedCells and (
            x, y) not in queue:
                queue.append((x, y))

    if len(visitedCells) != len(emptyCells):
        return False
    for cell in visitedCells:
        if cell not in emptyCells:
            return False
    return True


def generateNewLayout(height, width, layoutSize, layoutIteration):
    """
    generate random layout with given height, width.
    """

    wallCells = []
    isPath = False

    # find wall, empty cells for path.
    while not isPath:
        cells = [(i, j) for i in range(height) for j in range(width)]
        cornerCells = ((0, 0), (height - 1, 0), (0, width - 1), (height - 1, width - 1))
        wallCells = []
        count = 0
        while count < _layoutWallCount[layoutSize]:
            cell = random.choice(cells)
            if cell not in cornerCells and cell not in wallCells:
                wallCells.append(cell)
                count += 1
        emptyCells = [cell for cell in cells if cell not in wallCells]
        isPath = isPathAvailable(emptyCells, wallCells, height, width)

    # get final wall, empty cells.
    wallCells = [(cell[0] + 1, cell[1] + 1) for cell in wallCells]
    height, width = height + 2, width + 2
    for i in range(height):
        wallCells.append((i, 0))
        wallCells.append((i, width - 1))
    for j in range(1, width - 1):
        wallCells.append((0, j))
        wallCells.append((height - 1, j))

    # create maze string.
    mazeString = ""
    for i in range(height):
        curRow = ""
        for j in range(width):
            if (i, j) in wallCells:
                curRow += "%"
            else:
                curRow += " "
        curRow += "\n"
        mazeString += curRow

    # write layout to file.
    with open("layouts/{}Clean{}.lay".format(layoutSize, layoutIteration), "w") as file:
        file.write(mazeString)
        file.close()

    print("clean layout generated for {}Clean{}.".format(layoutSize, layoutIteration))


def generateCleanLayouts():
    """
    generate Empty layouts for all layout sizes.
    """
    for layoutSize, layoutDimensions in _layoutSizes.items():
        for itr in range(_layoutCount):
            generateNewLayout(layoutDimensions[0], layoutDimensions[1], layoutSize, itr)


def generateFinalLayout(cleanLayout, finalLayout, pacmanPosition, foodPositions):
    """
    fill clean layout with pacman positions and food positions.
    """
    # read current layout.
    file1 = open("layouts/{}.lay".format(cleanLayout), "r")
    rows = file1.read().split("\n")
    file1.close()

    # create final layout.
    finalRows = []
    for i in range(len(rows)):
        if len(rows[i]) > 0:
            finalRow = ""
            for j in range(len(rows[i])):
                if rows[i][j] == '%':
                    finalRow += "%"
                elif (i, j) == pacmanPosition:
                    finalRow += "P"
                elif (i, j) in foodPositions:
                    finalRow += "."
                else:
                    finalRow += " "
            finalRows.append(finalRow)

    # write final layout.
    file2 = open("layouts/{}.lay".format(finalLayout), "w")
    s = ""
    for finalRow in finalRows:
        s += finalRow
        s += "\n"
    s = s[:-1]
    file2.write(s)
    file2.close()


def getEmptyCells(layout):
    """
    get empty cells in current layout.
    """
    # read current layout.
    rows = []
    file1 = open("layouts/{}.lay".format(layout), "r")
    rows = file1.read().split("\n")

    # find empty cells.
    emptyCells = []
    for i in range(len(rows)):
        curRow = list(rows[i])
        for j in range(len(curRow)):
            if curRow[j] == ' ':
                emptyCells.append((i, j))

    return emptyCells


def getFoodPositions(emptyCells, foodNumber):
    """
    generate random food positions for given count.
    """
    if foodNumber > len(emptyCells):
        print("food Number is greater than empty cells.")
        return []

    count = 0
    foodPositions = []
    while foodNumber > count:
        food = random.choice(emptyCells)
        if food not in foodPositions:
            foodPositions.append(copy.deepcopy(food))
            count += 1

    return foodPositions


def getPacmanPosition(emptyCells, foodPositions):
    """
    generate random pacman position.
    """
    pacmanPositon = random.choice(emptyCells)
    while pacmanPositon in foodPositions:
        pacmanPositon = random.choice(emptyCells)
    return pacmanPositon


def getDimensions(layout):
    """
    get height and width of given layout.
    """
    # read current layout.
    file1 = open("layouts/{}.lay".format(layout), "r")
    rows = file1.read().split("\n")
    file1.close()
    height = 0
    for row in rows:
        if len(row) > 0:
            height += 1

    return (height, len(rows[0]))


def getCornersProblemFoodPositions(layout):
    """
    get all four corner's positions for corner problem.
    """
    dimensions = getDimensions(layout)
    top, right = dimensions[0] - 2, dimensions[1] - 2
    return ((1, 1), (1, right), (top, 1), (top, right))


def generateAllLayouts():
    """
    generate all different layouts for the script.
    """

    for problem in _problems:
        if problem == "PositionSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    for itr in range(_itrCountPositionSearchProblem):
                        foodPositions = getFoodPositions(emptyCells, 1)
                        pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                        generateFinalLayout(cleanLayout,
                                            layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr),
                                            pacmanPosition, foodPositions)

        if problem == "CornersProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    foodPositions = getCornersProblemFoodPositions(cleanLayout)
                    for itr in range(_itrCountCornersProblem):
                        pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                        generateFinalLayout(cleanLayout,
                                            layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr),
                                            pacmanPosition, foodPositions)

        if problem == "FoodSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    for itr in range(_itrCountFoodSearchProblem):
                        foodNumber = min(len(emptyCells) - 1, _maxFoodCount)
                        for foodCount in range(2, foodNumber + 1):
                            foodPositions = getFoodPositions(emptyCells, foodCount)
                            pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                            generateFinalLayout(cleanLayout,
                                                layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(
                                                    itr) + "FoodCount" + str(foodCount), pacmanPosition, foodPositions)

    print("filled clean mazes with food.")


def runScript(layout, algorithm, problem):
    """
    run given command.
    """
    cmd = "python pacman.py -l " + layout + " -p SearchAgent -a fn=" + algorithm + ",prob=" + problem + " -q"
    sysOutput = subprocess.check_output(cmd, shell=True)

    # parse output of current command.
    sysOutputSplit = sysOutput.decode("utf-8").split("\n")

    results = []
    for row in sysOutputSplit:
        if "Path found with total cost of" in row:
            tmp = row.split(" ")
            results.append(tmp[6].strip())
        elif "Search nodes expanded:" in row:
            tmp = row.split(":")
            results.append(tmp[1].strip())
        elif "Pacman emerges victorious! Score:" in row:
            tmp = row.split(":")
            results.append(tmp[1].strip())
        elif "Record:" in row:
            tmp = row.split(":")
            results.append(tmp[1].strip())

    return results


def writeResults(fileName, fields, data):
    """
    helper function to write data to csv file.
    """
    with open(fileName, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(data)


def printProgress(problem, layout, algo):
    """
    helper function to print progress.
    """
    print("done {} {} {}".format(problem, layout, algo))


def runAlgos():
    """
    run corresponding algorithms for each layout.
    """
    # list to store results.
    resultsPositionSearchProblem = []
    resultsCornersProblem = []
    resultsFoodSearchProblem = []

    for problem in _problems:
        if problem == "PositionSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    for algo in _algos:
                        for itr in range(_itrCountPositionSearchProblem):
                            finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr)
                            curResult = [layout, layoutCount, algo, itr]
                            curResult.extend(runScript(finalLayout, algo, problem))
                            resultsPositionSearchProblem.append(curResult)
                            printProgress(problem, finalLayout, algo)

        if problem == "CornersProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    for algo in _algos:
                        for itr in range(_itrCountCornersProblem):
                            finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr)
                            curResult = [layout, layoutCount, algo, itr]
                            curResult.extend(runScript(finalLayout, algo, problem))
                            resultsCornersProblem.append(curResult)
                            printProgress(problem, finalLayout, algo)

        if problem == "FoodSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    for algo in _algos:
                        for itr in range(_itrCountFoodSearchProblem):
                            foodNumber = min(len(emptyCells) - 1, _maxFoodCount)
                            for foodCount in range(2, foodNumber + 1):
                                finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(
                                    itr) + "FoodCount" + str(foodCount)
                                curResult = [layout, layoutCount, algo, itr, foodCount]
                                curResult.extend(runScript(finalLayout, algo, problem))
                                resultsFoodSearchProblem.append(curResult)
                                printProgress(problem, finalLayout, algo)

        # write results to csv file.
        fieldsPositionSearchProblem = ["layout", "layoutCount", "algorithm", "iteration", "cost", "expandedNodes",
                                       "score", "result"]
        writeResults("results/PositionSearchProblemResults.csv", fieldsPositionSearchProblem,
                     resultsPositionSearchProblem)

        fieldsCornersProblem = ["layout", "layoutCount", "algorithm", "iteration", "cost", "expandedNodes", "score",
                                "result"]
        writeResults("results/CornersProblemResults.csv", fieldsCornersProblem, resultsCornersProblem)

        fieldsFoodSearchProblem = ["layout", "layoutCount", "algorithm", "iteration", "foodCount", "cost",
                                   "expandedNodes", "score", "result"]
        writeResults("results/FoodSearchProblemResults.csv", fieldsFoodSearchProblem, resultsFoodSearchProblem)


def removeGeneratedLayouts():
    """
    remove all generated layouts.
    """
    for problem in _problems:
        if problem == "PositionSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    for itr in range(_itrCountPositionSearchProblem):
                        finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr)
                        os.remove("layouts/{}.lay".format(finalLayout))

        if problem == "CornersProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    for itr in range(_itrCountCornersProblem):
                        finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr)
                        os.remove("layouts/{}.lay".format(finalLayout))

        if problem == "FoodSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    for itr in range(_itrCountFoodSearchProblem):
                        foodNumber = min(len(emptyCells) - 1, _maxFoodCount)
                        for foodCount in range(2, foodNumber + 1):
                            finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(
                                itr) + "FoodCount" + str(foodCount)
                            os.remove("layouts/{}.lay".format(finalLayout))

    print("all generated layouts removed.")


def runTTtest():
    # calculate mean and std.dev for the data by grouping them by size and algorithm, perform t-test for different algorithms of the same layout
    for problem in _problems:
        df = pandas.read_csv("results/" + problem + "Results.csv", usecols=["layout", "algorithm", "expandedNodes"])
        arr = df.to_numpy()
        for row in arr:
            if (row[0], row[1]) not in dataGroups[problem]:
                dataGroups[problem][(row[0], row[1])] = [row[2]]
            else:
                dataGroups[problem][(row[0], row[1])].append(row[2])

        # Indpendent T-Test heuristic MM with all other algorithms
        tpvalues = {}
        for layout in _layouts:
            data2 = np.array(dataGroups[problem][(layout, "hbds")])
            for algo in _algos:
                if algo != "hbds":
                    data1 = np.array(dataGroups[problem][(layout, algo)])
                    statistic = stats.ttest_rel(a=data1, b=data2)
                    tpvalues[(layout, algo)] = (statistic[0], statistic[1])
        tStats_hbds[problem] = tpvalues
        csvResults = []
        for key, value in tStats_hbds[problem].items():
            temp = [key[0], key[1], value[0], value[1]]
            csvResults.append(temp)
        fields = ["layoutSize", "algorithm", "t-value", "p-value"]
        writeResults("results/" + problem + "hbdsTTestValues.csv", fields, csvResults)

        # Indpendent T-Test MM(0) with all other algorithms
        tpvalues_bds = {}
        for layout in _layouts:
            data2 = np.array(dataGroups[problem][(layout, "bds")])
            for algo in _algos:
                if algo != "bds":
                    data1 = np.array(dataGroups[problem][(layout, algo)])
                    statistic = stats.ttest_rel(a=data1, b=data2)
                    tpvalues_bds[(layout, algo)] = (statistic[0], statistic[1])
        tStats_bds[problem] = tpvalues_bds
        csvResults_bds = []
        for key, value in tStats_bds[problem].items():
            temp = [key[0], key[1], value[0], value[1]]
            csvResults_bds.append(temp)
        fields = ["layoutSize", "algorithm", "t-value", "p-value"]
        writeResults("results/" + problem + "bdsTTestValues.csv", fields, csvResults_bds)
    print("TStats Writing Done")


# script main method.
if __name__ == "__main__":
    """
    main method to run script.
    """

    # generate clean layouts with no food or pacman.
    # clean layout generation may take some time as we are
    # randomly generating layouts and checking whether path exists or not.
    generateCleanLayouts()

    # generate all layouts.
    generateAllLayouts()

    # run all algorithms on generated layouts.
    runAlgos()

    # remove all generated layouts.
    removeGeneratedLayouts()

    # run paired t-test for different pairs of algorithms
    runTTtest()
