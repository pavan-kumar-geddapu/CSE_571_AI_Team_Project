import copy
import csv
import os
import subprocess
import random


_itrCountPositionSearchProblem = 50
_itrCountCornersProblem = 50
_itrCountFoodSearchProblem = 10
_algos = ["dfs", "bfs", "ucs", "astar", "bds"]
_layouts = {"PositionSearchProblem": ["tinyMaze", "smallMaze", "mediumMaze", "bigMaze"], \
            "CornersProblem": ["tinyCorners", "smallCorners", "mediumCorners", "bigCorners"], \
            "FoodSearchProblem": ["tinySearch", "smallSearch", "mediumSearch", "bigSearch"]}
_problems = ["PositionSearchProblem", "CornersProblem", "FoodSearchProblem"]
_maxFoodCount = 20

def generateCleanLayouts():
    """
    remove foods, pacman from layout and create empty layout with walls.
    """
    for problem, layouts in _layouts.items():
        for layout in layouts:
            # read current layout.
            file1 = open("layouts/{}.lay".format(layout), "r")
            rows = file1.read().split("\n")
            file1.close()

            # remove pacman and food location.
            cleanRows = []
            for row in rows:
                if len(row) > 0:
                    cleanRow = ""
                    for c in row:
                        if c == '%':
                            cleanRow += str(c)
                        else:
                            cleanRow += " "
                    cleanRows.append(cleanRow)

            # create clean layout.
            file2 = open("layouts/{}Clean.lay".format(layout), "w")
            s = ""
            for cleanRow in cleanRows:
                s += cleanRow
                s += "\n"
            file2.write(s)
            file2.close()


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
    generateCleanLayouts()

    for problem in _problems:
        if problem == "PositionSearchProblem":
            for layout in _layouts[problem]:
                cleanLayout = layout + "Clean"
                emptyCells = getEmptyCells(cleanLayout)
                for itr in range(1, _itrCountPositionSearchProblem + 1):
                    foodPositions = getFoodPositions(emptyCells, 1)
                    pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                    generateFinalLayout(cleanLayout, layout + str(itr), pacmanPosition, foodPositions)

        if problem == "CornersProblem":
            for layout in _layouts[problem]:
                cleanLayout = layout + "Clean"
                emptyCells = getEmptyCells(cleanLayout)
                foodPositions = getCornersProblemFoodPositions(layout)
                for itr in range(1, _itrCountCornersProblem + 1):
                    pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                    generateFinalLayout(cleanLayout, layout + str(itr), pacmanPosition, foodPositions)

        if problem == "FoodSearchProblem":
            for layout in _layouts[problem]:
                cleanLayout = layout + "Clean"
                emptyCells = getEmptyCells(cleanLayout)
                for itr in range(1, _itrCountFoodSearchProblem + 1):
                    foodNumber = min(int(len(emptyCells)/5), _maxFoodCount, len(emptyCells)-1)
                    for foodCount in range(2, foodNumber+1):
                        foodPositions = getFoodPositions(emptyCells, foodCount)
                        pacmanPosition = getPacmanPosition(emptyCells, foodPositions)
                        generateFinalLayout(cleanLayout, layout + str(itr) + "_" + str(foodCount), pacmanPosition, foodPositions)


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
    with open(fileName, "w") as f:
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
            for layout in _layouts[problem]:
                for algo in _algos:
                    for itr in range(1, _itrCountPositionSearchProblem + 1):
                        finalLayout = layout + str(itr)
                        curResult = [layout, algo, itr]
                        curResult.extend(runScript(finalLayout, algo, problem))
                        resultsPositionSearchProblem.append(curResult)
                        printProgress(problem, finalLayout, algo, itr)

        if problem == "CornersProblem":
            for layout in _layouts[problem]:
                for algo in _algos:
                    for itr in range(1, _itrCountCornersProblem + 1):
                        finalLayout = layout + str(itr)
                        curResult = [layout, algo, itr]
                        curResult.extend(runScript(finalLayout, algo, problem))
                        resultsCornersProblem.append(curResult)
                        printProgress(problem, finalLayout, algo, itr)

        if problem == "FoodSearchProblem":
            for layout in _layouts[problem]:
                cleanLayout = layout + "Clean"
                emptyCells = getEmptyCells(cleanLayout)
                for algo in _algos:
                    for itr in range(1, _itrCountFoodSearchProblem + 1):
                        foodNumber = min(int(len(emptyCells)/5), _maxFoodCount, len(emptyCells)-1)
                        for foodCount in range(2, foodNumber+1):
                            finalLayout = layout + str(itr) + "_" + str(foodCount)
                            curResult = [layout, algo, itr, foodCount]
                            curResult.extend(runScript(finalLayout, algo, problem))
                            resultsFoodSearchProblem.append(curResult)
                            printProgress(problem, finalLayout, algo, itr, foodCount)

        # write results to csv file.
        fieldsPositionSearchProblem = ["layout", "algorithm", "iteration", "cost", "expandedNodes", "score", "result"]
        writeResults("results/positionalSearchProblemResults.csv", fieldsPositionSearchProblem, resultsPositionSearchProblem)

        fieldsCornersProblem = ["layout", "algorithm", "iteration", "cost", "expandedNodes", "score", "result"]
        writeResults("results/cornersProblemResults.csv", fieldsCornersProblem, resultsCornersProblem)

        fieldsFoodSearchProblem = ["layout", "algorithm", "iteration", "foodCount", "cost", "expandedNodes", "score", "result"]
        writeResults("results/foodSearchProblemResults.csv", fieldsFoodSearchProblem, resultsFoodSearchProblem)


def removeGeneratedLayouts():
    """
    remove all generated layouts.
    """
    for problem in _problems:
        if problem == "PositionSearchProblem":
            for layout in _layouts[problem]:
                for itr in range(1, _itrCountPositionSearchProblem + 1):
                    finalLayout = layout + str(itr)
                    os.remove("layouts/{}.lay".format(finalLayout))

        if problem == "CornersProblem":
            for layout in _layouts[problem]:
                for itr in range(1, _itrCountCornersProblem + 1):
                    finalLayout = layout + str(itr)
                    os.remove("layouts/{}.lay".format(finalLayout))

        if problem == "FoodSearchProblem":
            for layout in _layouts[problem]:
                cleanLayout = layout + "Clean"
                emptyCells = getEmptyCells(cleanLayout)
                for itr in range(1, _itrCountFoodSearchProblem + 1):
                    foodNumber = min(int(len(emptyCells)/5), _maxFoodCount, len(emptyCells)-1)
                    for foodCount in range(2, foodNumber + 1):
                        finalLayout = layout + str(itr) + "_" + str(foodCount)
                        os.remove("layouts/{}.lay".format(finalLayout))


# script main method.
if __name__ == "__main__":
    """
    main method to run script.
    """

    # generate all layouts.
    generateAllLayouts()

    # run all algorithms on generated layouts.
    runAlgos()

    # remove all generated layouts.
    removeGeneratedLayouts()
