import copy
import csv
import subprocess
import random

itrCount = 10
algos = ["dfs", "bfs", "ucs", "astar", "bds"]
layouts = ["tinyMaze", "smallMaze", "mediumMaze", "bigMaze"]

# create mazes with different start, goal pairs for given layout.
def modifyStartGoalPairs(layout):

    cells = []
    emptyCells = []

    # read current layout.
    file1 = open("layouts/{}.lay".format(layout), "r")
    arr = file1.read().split("\n")
    for s in arr:
        if len(s) > 0:
            cells.append(list(s))
    n = len(cells)
    m = len(cells[0])
    for i in range(n):
        for j in range(m):
            if cells[i][j] != '%':
                emptyCells.append((i, j))
            if cells[i][j] == 'P' or cells[i][j] == '.':
                cells[i][j] = ' '

    # create given number of mazes with different start, end goal pairs.
    for itr in range(itrCount):
        tmpCells = copy.deepcopy(cells)
        startCell = None
        endCell = None
        while startCell == endCell:
            startCell = random.choice(emptyCells)
            endCell = random.choice(emptyCells)
        tmpCells[startCell[0]][startCell[1]] = 'P'
        tmpCells[endCell[0]][endCell[1]] = '.'

        file2 = open("layouts/{}{}.lay".format(layout, itr), "w")
        s = ""
        for row in tmpCells:
            s += "".join(str(i) for i in row)
            s += "\n"
        file2.write(s)
        file2.close()

# helper function to trim zeros from sys output.
def trimZeros(s):
    result = ""
    for c in s:
        if c != ' ':
            result += str(c)
    return result

# function to run different algorithms for given layout.
def runScript(layout):

    results = []

    # iterate through different algorithms.
    for algo in algos:

        # iterate through different start, goal pairs for given layout.
        for itr in range(itrCount):
            cmd = "python pacman.py -l " + layout + str(itr) + " -p SearchAgent -a fn=" + algo + " -q"
            sysOutput = subprocess.check_output(cmd, shell=True)
            sysOutputSplit = sysOutput.decode("utf-8").split("\n")

            curResult = []
            curResult.append(layout)
            curResult.append(algo)
            curResult.append(itr+1)

            # split sys output to get results.
            for row in sysOutputSplit:
                if "Path found with total cost of" in row:
                    tmp = row.split(" ")
                    curResult.append(trimZeros(tmp[6]))
                elif "Search nodes expanded:" in row:
                    tmp = row.split(":")
                    curResult.append(trimZeros(tmp[1]))
                elif "Pacman emerges victorious! Score:" in row:
                    tmp = row.split(":")
                    curResult.append(trimZeros(tmp[1]))
                elif "Record:" in row:
                    tmp = row.split(":")
                    curResult.append(trimZeros(tmp[1]))
            results.append(curResult)

        print("layout: {}, algo: {} is done".format(layout, algo))

    return results

# function to print final results.
def printResults(results):
    for result in results:
        print(result)

# write results to file.
def writeResults(results):
    fields = ["layout", "algorithm", "iteration", "cost", "expanded nodes", "score", "result"]

    with open("results.csv", "w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(results)

# script main method.
if __name__ == "__main__":

    results = []

    # run through different maze sizes.
    for layout in layouts:
        modifyStartGoalPairs(layout)
        result = runScript(layout)
        for row in result:
            results.append(row)

    # write results to file.
    printResults(results)
    writeResults(results)