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
from util import Stack, Queue, PriorityQueue, Counter, PriorityQueueWithFunction

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
    return [s, s, w, s, w, w, s, w]

def genericSearch(problem, fringe):

    visited = set()
    totalPath = list()
    fringe.push((problem.getStartState(), list(), 0))
    while not fringe.isEmpty():
        currentState = fringe.pop()
        if problem.isGoalState(currentState[0]) == True:
            return currentState[1]
        if currentState[0] not in visited:
            for childNode, action, childCost in problem.getSuccessors(currentState[0]):
                    totalPath = currentState[1].copy()
                    totalPath.append(action)
                    totalCost = currentState[2] + childCost
                    fringe.push((childNode, totalPath, totalCost))
        visited.add(currentState[0])

    return None

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
    start_state = problem.getStartState()
    fringe = util.Stack()
    parent = {}  # Use a dictionary to store the parent of each state
    visited = set()  # Set of visited states (states that have already been visited)

    # Insert the starting state into the fringe
    # Node format: (state, action, cost)
    start_node = (start_state, None, 0)
    fringe.push(start_node)

    while not fringe.isEmpty():
        node = fringe.pop()
        state, action, cost = node

        if problem.isGoalState(state):
            actions = []
            while node[1] is not None:
                actions.insert(0, node[1])  # Insert action at the beginning
                node = parent[node[0]]
            return actions

        if state not in visited:
            visited.add(state)

            for successor in problem.getSuccessors(state):
                successor_state, successor_action, successor_cost = successor

                if successor_state not in visited:
                    fringe.push((successor_state, successor_action, successor_cost))
                    parent[successor_state] = node

    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Initialize a queue for BFS
    fringe = util.Queue()
    # Initialize a set to keep track of visited states
    visited = set()
    # Start with the initial state and an empty list of actions
    fringe.push((problem.getStartState(), []))

    while not fringe.isEmpty():
        state, actions = fringe.pop()
        
        if problem.isGoalState(state):
            return actions  # Return the list of actions when the goal is reached
        
        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for successor_state, action, successor_cost in successors:
                if successor_state not in visited:
                    new_actions = actions + [action]  # Append the current action to the list
                    fringe.push((successor_state, new_actions))
    
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push((problem.getStartState(),[],0),0)
    while not fringe.isEmpty():
        state,actions,cost = fringe.pop()

        if problem.isGoalState(state):
            return actions
        
        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for successor_state,action,successor_cost in successors:
                new_actions = actions + [action]
                new_cost = cost + successor_cost
                fringe.push((successor_state, new_actions, new_cost),new_cost)
    return []
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push((problem.getStartState(),[],0),0)
    while not fringe.isEmpty():
        state,actions,cost = fringe.pop()

        if problem.isGoalState(state):
            return actions
        
        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for successor_state,action,successor_cost in successors:
                new_action = actions + [action]
                new_cost = cost + successor_cost
                heuristic_value = heuristic(successor_state,problem)
                new_priority = new_cost + heuristic_value
                fringe.push((successor_state,new_action,new_cost),new_priority)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
