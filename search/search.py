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


def tinyMazeSearch(problem: SearchProblem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


class Node:
    def __init__(self, state, path, pathCost=-1):
        self.state = state
        self.path = path
        self.pathCost = pathCost
        self.depth = len(path)
        if pathCost == -1:
            self.pathCost = self.depth


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def bestFirstSearch(problem: SearchProblem, f=nullHeuristic):
    """Search the node that has the lowest value first."""
    # Will be called with the proper evaluation function
    # to utilize each of the different search algorithms.

    startNode = Node(problem.getStartState(), [], 0)
    frontier = util.PriorityQueue()
    frontier.push(startNode, f(startNode, problem))
    explored = dict()

    while not frontier.isEmpty():
        node = frontier.pop()

        if node.state in explored: continue

        if problem.isGoalState(node.state):
            return node.path

        explored[node.state] = node

        # reverse successors so that DFS expands the least nodes for Q1.
        # does not meaningfully affect the other search algorithms
        for successor, action, cost in problem.getSuccessors(node.state)[::-1]:
            path = node.path + [action]
            child = Node(successor, path, node.pathCost + cost)
            if child.state not in explored:
                frontier.push((child), f(child, problem))
            elif child.pathCost < explored[child.state].pathCost:
                frontier.update(child, f(child, problem))
                explored.pop(child.state)
                # explored[child.state] = child

    return None
    # return node.path

def nodeDepth(node: Node, problem):
    return node.depth

def nodeNegativeDepth(node: Node, problem):
    return -nodeDepth(node, problem)

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    return bestFirstSearch(problem, nodeNegativeDepth)

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    return bestFirstSearch(problem, nodeDepth)

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    def f(node: Node, problem: SearchProblem):
        try:
            return node.pathCost + heuristic(node.state, problem)
        except TypeError:
            return node.pathCost + 0

    return bestFirstSearch(problem, f)

def uniformCostSearch(problem: SearchProblem):
    "Search the node of least total cost first. "

    return aStarSearch(problem, nullHeuristic)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch