import copy
import csv
import os
import subprocess
import random


_itrCountPositionSearchProblem = 1
_itrCountCornersProblem = 1
_itrCountFoodSearchProblem = 1
_maxFoodCount = 2
_layoutCount = 1
_algos = ["dfs", "bfs", "ucs", "astar", "bds"]
_layouts = ["tiny", "small", "medium", "big"]
_layoutSizes = {"tiny": (5, 10), "small": (10, 15), "medium": (15, 20), "big": (20, 25)}
_layoutWallCount = {"tiny": 20, "small": 50, "medium": 100, "big": 125}
_layoutType = {"PositionSearchProblem": "Maze", "CornersProblem": "Corners", "FoodSearchProblem": "Search"}
_problems = ["PositionSearchProblem", "CornersProblem", "FoodSearchProblem"]


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
            x, y = _x+cell[0], _y+cell[1]
            if 0 <= x < height and 0 <= y < width and (x, y) not in wallCells and (x, y) not in visitedCells and (x, y) not in queue:
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
        cornerCells = ((0,0), (height-1, 0), (0, width-1), (height-1, width-1))
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
    wallCells = [(cell[0]+1, cell[1]+1) for cell in wallCells]
    height, width = height + 2, width + 2
    for i in range(height):
        wallCells.append((i, 0))
        wallCells.append((i, width-1))
    for j in range(1, width-1):
        wallCells.append((0, j))
        wallCells.append((height-1, j))

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
    top, right = dimensions[0]-2, dimensions[1]-2
    return ((1,1), (1, right), (top, 1), (top, right))

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
                        generateFinalLayout(cleanLayout, layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr), pacmanPosition, foodPositions)

        if problem == "CornersProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    foodPositions = getCornersProblemFoodPositions(cleanLayout)
                    for itr in range(_itrCountCornersProblem):
                        pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                        generateFinalLayout(cleanLayout, layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr), pacmanPosition, foodPositions)

        if problem == "FoodSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    for itr in range(_itrCountFoodSearchProblem):
                        foodNumber = min(int(len(emptyCells)/5), _maxFoodCount, len(emptyCells)-1)
                        for foodCount in range(2, foodNumber+1):
                            foodPositions = getFoodPositions(emptyCells, foodCount)
                            pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                            generateFinalLayout(cleanLayout, layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr) + "FoodCount" + str(foodCount), pacmanPosition, foodPositions)

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
    with open(fileName, "w",newline = "") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(data)


def printProgress(problem, layout, algo, iteration, foodCount = 0):
    """
    helper function to print progress.
    """
    if foodCount == 0:
        print("done {} {} {} {}".format(problem, layout, algo, iteration))
    else:
        print("done {} {} {} {} {}".format(problem, layout, algo, iteration, foodCount))


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
                            printProgress(problem, finalLayout, algo, itr)

        if problem == "CornersProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    for algo in _algos:
                        for itr in range(_itrCountCornersProblem):
                            finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr)
                            curResult = [layout, layoutCount, algo, itr]
                            curResult.extend(runScript(finalLayout, algo, problem))
                            resultsCornersProblem.append(curResult)
                            printProgress(problem, finalLayout, algo, itr)

        if problem == "FoodSearchProblem":
            for layout in _layouts:
                for layoutCount in range(_layoutCount):
                    cleanLayout = layout + "Clean" + str(layoutCount)
                    emptyCells = getEmptyCells(cleanLayout)
                    for algo in _algos:
                        for itr in range(_itrCountFoodSearchProblem):
                            foodNumber = min(int(len(emptyCells)/5), _maxFoodCount, len(emptyCells)-1)
                            for foodCount in range(2, foodNumber+1):
                                finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr) + "FoodCount" + str(foodCount)
                                curResult = [layout, layoutCount, algo, itr, foodCount]
                                curResult.extend(runScript(finalLayout, algo, problem))
                                resultsFoodSearchProblem.append(curResult)
                                printProgress(problem, finalLayout, algo, itr, foodCount)

        # write results to csv file.
        fieldsPositionSearchProblem = ["layout", "layoutCount", "algorithm", "iteration", "cost", "expandedNodes", "score", "result"]
        writeResults("results/positionalSearchProblemResults.csv", fieldsPositionSearchProblem, resultsPositionSearchProblem)

        fieldsCornersProblem = ["layout", "layoutCount", "algorithm", "iteration", "cost", "expandedNodes", "score", "result"]
        writeResults("results/cornersProblemResults.csv", fieldsCornersProblem, resultsCornersProblem)

        fieldsFoodSearchProblem = ["layout", "layoutCount", "algorithm", "iteration", "foodCount", "cost", "expandedNodes", "score", "result"]
        writeResults("results/foodSearchProblemResults.csv", fieldsFoodSearchProblem, resultsFoodSearchProblem)


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
                        foodNumber = min(int(len(emptyCells)/5), _maxFoodCount, len(emptyCells)-1)
                        for foodCount in range(2, foodNumber + 1):
                            finalLayout = layout + _layoutType[problem] + str(layoutCount) + "Itr" + str(itr) + "FoodCount" + str(foodCount)
                            os.remove("layouts/{}.lay".format(finalLayout))

    print("all generated layouts removed.")


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