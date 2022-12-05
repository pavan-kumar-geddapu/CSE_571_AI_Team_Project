# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import copy

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    frontierList = Stack()  # stack to store open nodes and expand the deepest first

    exploredList = set()    # set to store explored nodes

    initialNode = (problem.getNextStartStateForBds(), [])

    frontierList.push(initialNode)    # push initial node to frontier (node contains current state and path from root)

    # to initate goal Node
    nextGoalNode = problem.getNextGoalForBds()

    # to store all goals combined path.
    finalCombinedPath = list()

    while True: # iterate till we find the goal noad or get exhaust

        if frontierList.isEmpty():  # if frontier is empty, then goal node is not found, so return null path
            return []

        frontierNode = frontierList.pop() # take out top node of the stack

        curNode = frontierNode[0]

        curPath = frontierNode[1]

        exploredList.add(curNode)   # expanded nodes are added to the explored list

        if problem.isCurrentGoalState(curNode):

            # add current goal path to final combined path.
            finalCombinedPath.extend(curPath)

            # reinstate all lists to get path to new goal.
            frontierList = Stack()
            exploredList = set()
            initialNode = (problem.getNextStartStateForBds(), [])
            frontierList.push(initialNode)
            nextGoalNode = problem.getNextGoalForBds()

            # if all goals were found return combined path.
            if problem.isGoalStateForBds():
                return finalCombinedPath

            else:
                continue

        else:

            curNodeScucessors = problem.getSuccessorsForBds(curNode)

            for childNode in curNodeScucessors:    # visit current node's successors (children nodes)

                if childNode[0] not in exploredList:    # in case the successor node is not explored then add it to frontier list

                    childPath = curPath + [childNode[1]]    # find path to child node

                    newChildNode = (childNode[0], childPath)

                    frontierList.push(newChildNode)    # push childnode to stack

    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from util import Queue

    frontierList = Queue()  # queue to store open nodes and expand based on FIFO

    exploredList = set()    # set to store explored nodes

    initialNode = (problem.getNextStartStateForBds(), [])

    frontierList.push(initialNode)    # push initial node to frontier (node contains current state and path from root)

    # to initate goal Node
    nextGoalNode = problem.getNextGoalForBds()

    # to store all goals combined path.
    finalCombinedPath = list()

    while True: # iterate until goal was found or frontier list exhausted

        if frontierList.isEmpty():  # if frontier is empty, then goal node is not found, return empty path
            return []

        frontierNode = frontierList.pop() # take out top node of the stack

        curNode = frontierNode[0]

        curPath = frontierNode[1]

        exploredList.add(curNode)   # expanded nodes are added to the explored list

        if problem.isCurrentGoalState(curNode):

            # add current goal path to final combined path.
            finalCombinedPath.extend(curPath)

            # reinstate all lists to get path to new goal.
            frontierList = Queue()
            exploredList = set()
            initialNode = (problem.getNextStartStateForBds(), [])
            frontierList.push(initialNode)
            nextGoalNode = problem.getNextGoalForBds()

            # if all goals were found return combined path.
            if problem.isGoalStateForBds():
                return finalCombinedPath

            else:
                continue

        else:

            curNodeScucessors = problem.getSuccessorsForBds(curNode)

            for childNode in curNodeScucessors:    # visit current node's successors (children nodes)

                frontierNodeList = (frontierNode[0] for frontierNode in frontierList.list)

                if childNode[0] not in exploredList and childNode[0] not in frontierNodeList:    # in case the successor node is not explored and is not in frontier list

                    childPath = curPath + [childNode[1]]    # find path to child node

                    newChildNode = (childNode[0], childPath)

                    frontierList.push(newChildNode)    # push childnode to stack

    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue

    frontierList = PriorityQueue()  # priority Queue to store open nodes and expand based on priority (cost)

    exploredList = set()    # set to store explored nodes

    initialNode = (problem.getNextStartStateForBds(), [])

    frontierList.push(initialNode, 0)    # push initial node to frontier (node contains current state and path from root)

    # to initate goal Node
    nextGoalNode = problem.getNextGoalForBds()

    # to store all goals combined path.
    finalCombinedPath = list()

    while True: # iterate till goal was found or frontier list exhausted

        if frontierList.isEmpty():  # if frontier list is empty, then goal node is not found, so return empty path
            return []

        frontierNode = frontierList.pop() # take out top node of the stack

        curNode = frontierNode[0]

        curPath = frontierNode[1]

        exploredList.add(curNode)   # expanded nodes are added to the explored list

        if problem.isCurrentGoalState(curNode):

            # add current goal path to final combined path.
            finalCombinedPath.extend(curPath)

            # reinstate all lists to get path to new goal.
            frontierList = PriorityQueue()
            exploredList = set()
            initialNode = (problem.getNextStartStateForBds(), [])
            frontierList.push(initialNode, 0)
            nextGoalNode = problem.getNextGoalForBds()

            # if all goals were found return combined path.
            if problem.isGoalStateForBds():
                return finalCombinedPath

            else:
                continue

        else:

            curNodeScucessors = problem.getSuccessorsForBds(curNode)

            for childNode in curNodeScucessors:    # visit current node's successors (children nodes)

                frontierNodeList = (frontierNode[2][0] for frontierNode in frontierList.heap)

                if childNode[0] not in exploredList and childNode[0] not in frontierNodeList: # in case the successor node is not explored and is not in frontier list

                    childPath = curPath + [childNode[1]]    # find path to child node

                    childCost = problem.getCostOfActionsForBds(childPath) # find cost to the child node

                    newChildNode = (childNode[0], childPath)

                    frontierList.push(newChildNode, childCost) # push child node to frontier list

                elif childNode[0] not in exploredList and childNode[0] in (frontierNode[2][0] for frontierNode in frontierList.heap):   # in case the successor node is not explored and is already in frontier list, then we check new path's cost and update accordingly

                    oldCost = 0

                    for frontierNode in frontierList.heap:  # find old cost of the child node
                        if frontierNode[2][0] == childNode[0]:  # check for the child node in frontier list
                            oldCost = problem.getCostOfActionsForBds(frontierNode[2][1])  # find it's cost

                    childPath = curPath + [childNode[1]]    # find child node path

                    newChildNode = (childNode[0], childPath)

                    newCost = problem.getCostOfActionsForBds(childPath)   # find new cost of the child node

                    if oldCost > newCost:   # if new cost is better then old cost then update frontier node with new cost
                        frontierList.update(newChildNode, newCost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanDistance(startPos, endPos):
    """
    The Manhattan distance between two points.
    """
    print(startPos, endPos)
    return abs(startPos[0] - endPos[0]) + abs(startPos[1] - endPos[1])
def manhattanHeuristic(curPos, goalPos):
    """
    A heuristic to get min manhattan distance from current state to
    goal state.
    """
    if not curPos or not goalPos:
        return float("inf")
    return abs(curPos[0] - goalPos[0]) + abs(curPos[1] - goalPos[1])

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue

    frontierList = PriorityQueue()  # priority Queue to store open nodes and expand based on priority (f(n)=g(n)+h(n))

    exploredList = set()    # set to store explored nodes

    startNode = problem.getNextStartStateForBds()

    initialNode = (startNode, [])

    # to initiate goal Node.
    goalNode = problem.getNextGoalForBds()

    fnValue = problem.getCostOfActionsForBds([])+manhattanHeuristic(startNode, goalNode)  # Calculate f(n) value of the start node


    frontierList.push(initialNode, fnValue)   # push initial node to frontier (node contains current state and path from root), priority is f(n) value


    # to store all goals combined path.
    finalCombinedPath = list()

    while True: # iterate till goal node is found or frontier list exhausted

        if frontierList.isEmpty():  # if frontier list is empty, then goal node is not found, return empty path
            return []

        frontierNode = frontierList.pop() # take out top node of the stack

        curNode = frontierNode[0]

        curPath = frontierNode[1]

        if curNode in exploredList: # if node is already visited then continue, to avoid expaning same node multiple times
            continue

        exploredList.add(curNode)   # expanded nodes are added to the explored list

        if problem.isCurrentGoalState(curNode):

            # add current goal path to final combined path.
            finalCombinedPath.extend(curPath)

            # reinstate all lists to get path to new goal.
            frontierList = PriorityQueue()
            exploredList = set()
            startNode = problem.getNextStartStateForBds()
            initialNode = (startNode, [])
            goalNode = problem.getNextGoalForBds()
            fnValue = problem.getCostOfActionsForBds([])+manhattanHeuristic(startNode, goalNode)
            frontierList.push(initialNode, fnValue)

            # if all goals were found return combined path.
            if problem.isGoalStateForBds():
                return finalCombinedPath

            else:
                continue

        else:

            curNodeScucessors = problem.getSuccessorsForBds(curNode)

            for childNode in curNodeScucessors:    # visit current node's successors (children nodes)

                if childNode[0] not in exploredList:    # in case the successor node is not explored, add it to frontier list

                    childPath = curPath + [childNode[1]]    # find child node path

                    childCost = problem.getCostOfActionsForBds(childPath)+manhattanHeuristic(childNode[0], goalNode) # find child node f(n) value

                    newChildNode = (childNode[0], childPath)

                    frontierList.push(newChildNode, childCost) # push child node to frontier list

                elif childNode[0] not in exploredList and childNode[0] in (frontierNode[2][0] for frontierNode in frontierList.heap):   # in case the successor node is not explored and is already in frontier list, then we check new path's cost and update accordingly

                    oldCost = 0

                    for frontierNode in frontierList.heap:  # find old cost of the child node
                        if frontierNode[2][0] == childNode[0]:  # check for the child node in frontier list
                            oldCost = problem.getCostOfActionsForBds(frontierNode[2][1]) + manhattanHeuristic(frontierNode[2][0], goalNode)  # find it's cost

                    childPath = curPath + [childNode[1]]    # find child node path

                    newCost = problem.getCostOfActionsForBds(childPath)+manhattanHeuristic(childNode[0], goalNode) # find child node f(n) value

                    if oldCost > newCost:   # if new cost is better then old cost then update frontier node with new cost
                        frontierList.update((childNode[0], childPath), newCost)

    util.raiseNotDefined()

def biDirectionalSearch(problem):
    """Search the shallowest nodes in the search tree first, from both direction (from start node and goal node)."""

    from util import Queue

    # queue to store open nodes and expand based on FIFO from start node.
    startFrontierList = Queue()

    # set to store explored nodes from start node.
    startExploredList = set()

    # list to store nodes visited from start node.
    startVisitedList = list()

    startInitialNode = (problem.getNextStartStateForBds(), [])

    # push initial node to start frontier (node contains current state and path from root).
    startFrontierList.push(startInitialNode)

    # queue to store open nodes and expand based on FIFO from start node.
    endFrontierList = Queue()

    # set to store explored nodes from start node.
    endExploredList = set()

    # list to store nodes visited from start node.
    endVisitedList = list()

    endInitialNode = (problem.getNextGoalForBds(), [])

    # push initial node to end frontier (node contains current state and path from root).
    endFrontierList.push(endInitialNode)

    # to store all goals combined path.
    finalCombinedPath = list()

    # iterate till we find the goal noad or get exhaust.
    while True:

        # if both frontiers are empty, then goal node is not found, so return null path.
        if startFrontierList.isEmpty() and endFrontierList.isEmpty():
            return []

        # if start frontier is not empty expand it.
        if not startFrontierList.isEmpty():
            
            # take out top node from the frontier list.
            frontierNode = startFrontierList.pop()

            curNode = frontierNode[0]

            curPath = frontierNode[1]

            # expanded nodes are added to the explored list.
            startExploredList.add(curNode)
            
            # if current node is in end visited list then we can combine both path to get final path.
            if curNode in endVisitedList:

                # find curNode in end frontier list.
                while not endFrontierList.isEmpty():

                    (endCurNode, endCurPath) = endFrontierList.pop()

                    # if we got the matching node append paths.
                    if endCurNode == curNode:

                        # reverse end node's path and get final path by combining both paths.
                        finalPath = curPath + reverseDirections(endCurPath[::-1])

                        # add current goal path to final combined path.
                        finalCombinedPath.extend(finalPath)

                        # reinstate all lists to get path to new goal.
                        startFrontierList = Queue()
                        startExploredList = set()
                        startVisitedList = list()
                        startInitialNode = (problem.getNextStartStateForBds(), [])
                        startFrontierList.push(startInitialNode)
                        endFrontierList = Queue()
                        endExploredList = set()
                        endVisitedList = list()
                        endInitialNode = (problem.getNextGoalForBds(), [])
                        endFrontierList.push(endInitialNode)

                        # if all goals were found return combined path.
                        if problem.isGoalStateForBds():
                            return finalCombinedPath

                        else:
                            break
            
            # else visit current node's successors (children nodes)
            else:

                curNodeScucessors = problem.getSuccessorsForBds(curNode)

                for childNode in curNodeScucessors:

                    # in case the successor node is not explored and is not in frontier list.
                    if childNode[0] not in startExploredList and childNode[0] not in startVisitedList:

                        # find path to child node.
                        childPath = curPath + [childNode[1]]

                        newChildNode = (childNode[0], childPath)

                        # push child node to frontier.
                        startFrontierList.push(newChildNode)

                        # push child node to visited list.
                        startVisitedList.append(childNode[0])

        # if end frontier is not empty expand it.
        if not endFrontierList.isEmpty():
            
            # take out top node from the frontier list.
            frontierNode = endFrontierList.pop()

            curNode = frontierNode[0]

            curPath = frontierNode[1]

            # expanded nodes are added to the explored list.
            endExploredList.add(curNode)
            
            # if current node is in start visited list then we can combine both path to get final path.
            if curNode in startVisitedList:

                # find curNode in end frontier
                while not startFrontierList.isEmpty():

                    (startCurNode, startCurPath) = startFrontierList.pop()

                    # if we got the matching node append paths.
                    if startCurNode == curNode:

                        # reverse end node's path.
                        curPath.reverse()

                        # get final path by combining both paths.
                        finalPath = startCurPath + reverseDirections(curPath)

                        # add current goal path to final combined path.
                        finalCombinedPath.extend(finalPath)

                        # reinstate all lists to get path to new goal.
                        startFrontierList = Queue()
                        startExploredList = set()
                        startVisitedList = list()
                        startInitialNode = (problem.getNextStartStateForBds(), [])
                        startFrontierList.push(startInitialNode)
                        endFrontierList = Queue()
                        endExploredList = set()
                        endVisitedList = list()
                        endInitialNode = (problem.getNextGoalForBds(), [])
                        endFrontierList.push(endInitialNode)

                        # if all goals are covered, return combined path.
                        if problem.isGoalStateForBds():
                            return finalCombinedPath
                        else:
                            break

            # else visit current node's successors (children nodes)
            else:

                curNodeScucessors = problem.getSuccessorsForBds(curNode)

                for childNode in curNodeScucessors:

                    # in case the successor node is not explored and is not in frontier list.
                    if childNode[0] not in endExploredList and childNode[0] not in endVisitedList:

                        # find path to child node.
                        childPath = curPath + [childNode[1]]

                        newChildNode = (childNode[0], childPath)

                        # push child node to frontier.
                        endFrontierList.push(newChildNode)

                        # push child node to visited list.
                        endVisitedList.append(childNode[0])


def heuristicBiDirectionalSearch(problem):
    """
    Search the node that has the lowest combined cost and heuristic first. from both direction (from start node and goal node).
    """

    from util import PriorityQueue

    # queue to store open nodes and expand based on FIFO from start node.
    startFrontierList = PriorityQueue()

    # set to store explored nodes from start node.
    startExploredList = set()

    # list to store nodes visited from start node.
    startVisitedList = list()

    startNode = problem.getNextStartStateForBds()

    startInitialNode = (startNode, [])


    # queue to store open nodes and expand based on FIFO from start node.
    endFrontierList = PriorityQueue()

    # set to store explored nodes from start node.
    endExploredList = set()

    # list to store nodes visited from start node.
    endVisitedList = list()

    goalNode = problem.getNextGoalForBds()

    endInitialNode = (goalNode, [])

    startFnValue = problem.getCostOfActionsForBds([]) + manhattanHeuristic(startNode, goalNode)

    endFnValue = problem.getCostOfActionsForBds([]) + manhattanHeuristic(goalNode, startNode)

    # push initial node to start frontier (node contains current state and path from root).
    startFrontierList.push(startInitialNode, startFnValue)

    # push initial node to end frontier (node contains current state and path from root).
    endFrontierList.push(endInitialNode, endFnValue)

    # to store all goals combined path.
    finalCombinedPath = list()

    # iterate till we find the goal noad or get exhaust.
    while True:

        # if both frontiers are empty, then goal node is not found, so return null path.
        if startFrontierList.isEmpty() and endFrontierList.isEmpty():
            return []

        # if start frontier is not empty expand it.
        if not startFrontierList.isEmpty():

            # take out top node from the frontier list.
            frontierNode = startFrontierList.pop()

            curNode = frontierNode[0]

            curPath = frontierNode[1]

            # expanded nodes are added to the explored list.
            startExploredList.add(curNode)

            # if current node is in end visited list then we can combine both path to get final path.
            if curNode in endVisitedList:

                # find curNode in end frontier list.
                while not endFrontierList.isEmpty():

                    (endCurNode, endCurPath) = endFrontierList.pop()

                    # if we got the matching node append paths.
                    if endCurNode == curNode:

                        # reverse end node's path and get final path by combining both paths.
                        finalPath = curPath + reverseDirections(endCurPath[::-1])

                        # add current goal path to final combined path.
                        finalCombinedPath.extend(finalPath)

                        # reinstate all lists to get path to new goal.
                        startFrontierList = PriorityQueue()
                        startExploredList = set()
                        startVisitedList = list()
                        startNode = problem.getNextStartStateForBds()
                        startInitialNode = (startNode, [])
                        endFrontierList = PriorityQueue()
                        endExploredList = set()
                        endVisitedList = list()
                        goalNode = problem.getNextGoalForBds()
                        endInitialNode = (goalNode, [])
                        startFnValue = problem.getCostOfActionsForBds([]) + manhattanHeuristic(startNode, goalNode)
                        endFnValue = problem.getCostOfActionsForBds([]) + manhattanHeuristic(goalNode, startNode)
                        startFrontierList.push(startInitialNode, startFnValue)
                        endFrontierList.push(endInitialNode, endFnValue)

                        # if all goals were found return combined path.
                        if problem.isGoalStateForBds():
                            return finalCombinedPath

                        else:
                            break

            # else visit current node's successors (children nodes)
            else:

                curNodeScucessors = problem.getSuccessorsForBds(curNode)

                for childNode in curNodeScucessors:

                    # in case the successor node is not explored and is not in frontier list.
                    if childNode[0] not in startExploredList:
                        # find path to child node.
                        childPath = curPath + [childNode[1]]

                        childCost = problem.getCostOfActionsForBds(childPath)+manhattanHeuristic(childNode[0], goalNode)

                        newChildNode = (childNode[0], childPath)

                        # push child node to frontier.
                        startFrontierList.push(newChildNode, childCost)

                        # push child node to visited list.
                        startVisitedList.append(childNode[0])

                    elif childNode[0] not in startExploredList and childNode[0] in (frontierNode[2][0] for frontierNode in startFrontierList.heap):

                        oldCost = 0
                        for frontierNode in startFrontierList.heap:  # find old cost of the child node
                            if frontierNode[2][0] == childNode[0]:  # check for the child node in frontier list
                                oldCost = problem.getCostOfActionsForBds(frontierNode[2][1]) + manhattanHeuristic(
                                    frontierNode[2][0], goalNode)  # find it's cost

                        childPath = curPath + [childNode[1]]  # find child node path

                        newCost = problem.getCostOfActionsForBds(childPath) + manhattanHeuristic(childNode[0], goalNode)  # find child node f(n) value

                        if oldCost > newCost:
                            startFrontierList.update((childNode[0], childPath), newCost)

        # if end frontier is not empty expand it.
        if not endFrontierList.isEmpty():

            # take out top node from the frontier list.
            frontierNode = endFrontierList.pop()

            curNode = frontierNode[0]

            curPath = frontierNode[1]

            # expanded nodes are added to the explored list.
            endExploredList.add(curNode)

            # if current node is in start visited list then we can combine both path to get final path.
            if curNode in startVisitedList:

                # find curNode in end frontier
                while not startFrontierList.isEmpty():

                    (startCurNode, startCurPath) = startFrontierList.pop()

                    # if we got the matching node append paths.
                    if startCurNode == curNode:

                        # reverse end node's path.
                        curPath.reverse()

                        # get final path by combining both paths.
                        finalPath = startCurPath + reverseDirections(curPath)

                        # add current goal path to final combined path.
                        finalCombinedPath.extend(finalPath)

                        # reinstate all lists to get path to new goal.
                        startFrontierList = PriorityQueue()
                        startExploredList = set()
                        startVisitedList = list()
                        startNode = problem.getNextStartStateForBds()
                        startInitialNode = (startNode, [])
                        endFrontierList = PriorityQueue()
                        endExploredList = set()
                        endVisitedList = list()
                        goalNode = problem.getNextGoalForBds()
                        endInitialNode = (goalNode, [])
                        startFnValue = problem.getCostOfActionsForBds([]) + manhattanHeuristic(startNode, goalNode)
                        endFnValue = problem.getCostOfActionsForBds([]) + manhattanHeuristic(goalNode, startNode)
                        startFrontierList.push(startInitialNode, startFnValue)
                        endFrontierList.push(endInitialNode, endFnValue)

                        # if all goals are covered, return combined path.
                        if problem.isGoalStateForBds():
                            return finalCombinedPath
                        else:
                            break

            # else visit current node's successors (children nodes)
            else:

                curNodeScucessors = problem.getSuccessorsForBds(curNode)

                for childNode in curNodeScucessors:

                    # in case the successor node is not explored and is not in frontier list.
                    if childNode[0] not in endExploredList:
                        # find path to child node.
                        childPath = curPath + [childNode[1]]

                        childCost = problem.getCostOfActionsForBds(childPath) + manhattanHeuristic(childNode[0], startNode)

                        newChildNode = (childNode[0], childPath)

                        # push child node to frontier.
                        endFrontierList.push(newChildNode, childCost)

                        # push child node to visited list.
                        endVisitedList.append(childNode[0])

                    elif childNode[0] not in endExploredList and childNode[0] in (frontierNode[2][0] for frontierNode in endFrontierList.heap):

                        oldCost = 0
                        for frontierNode in endFrontierList.heap:  # find old cost of the child node
                            if frontierNode[2][0] == childNode[0]:  # check for the child node in frontier list
                                oldCost = problem.getCostOfActionsForBds(frontierNode[2][1]) + manhattanHeuristic(
                                    frontierNode[2][0], goalNode)  # find it's cost

                        childPath = curPath + [childNode[1]]  # find child node path

                        newCost = problem.getCostOfActionsForBds(childPath) + manhattanHeuristic(childNode[0], startNode)  # find child node f(n) value

                        if oldCost > newCost:
                            endFrontierList.update((childNode[0], childPath), newCost)

def reverseDirections(directions):
    """Reverses the directions from goal node to current node."""

    finalDirections = []

    for direction in directions:
        
        if direction == "North":
            finalDirections.append("South")
        
        elif direction == "South":
            finalDirections.append("North")

        elif direction == "East":
            finalDirections.append("West")

        else:
            finalDirections.append("East")
    
    return finalDirections

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
bds = biDirectionalSearch
hbds = heuristicBiDirectionalSearch