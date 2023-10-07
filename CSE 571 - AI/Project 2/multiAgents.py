# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect moves moves and successor states
        movesMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in movesMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return movesMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()


        for food in newFood:
            distances = min([manhattanDistance(newPos,food)])
            score = score + (1/distances)
        
        for ghostState in newGhostStates:
            ghostPosition = ghostState.getPosition()
            distfromGhost = manhattanDistance(newPos,ghostPosition)
        
            if distfromGhost < 2:
                    if ghostState.scaredTimer > 0:
                        score = score + 20000       #Getting the pacman to eat the Ghost if powered up
                    
                    score = -1000       #trying to get away from the ghost is it is too close
            elif distfromGhost < 4:     #ghost nearby , time to stay safe
                score = -50
            else:
                score = score + (1/distfromGhost)
        
        RemFood = len(newFood)          # to find the remaining food
        score = score - RemFood
    
        return score
        return max(max(newScaredTimes),min(distances))
        return successorGameState.getScore()+max(newScaredTimes)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of moves actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        moves = gameState.getLegalActions(0)    #Getting the alloweed moves for the pacman 
        successors = [gameState.generateSuccessor(0, action) for action in moves]
        Maxfunc = -float('inf')
        goalIndex = 0
        for x in range(len(successors)):
            actionValue = self.value(successors[x], 1, 0)
            if actionValue > Maxfunc:
                Maxfunc = actionValue
                goalIndex = x
        
        return moves[goalIndex]
        
    def Maxfunc(self,gameState,agentIndex,depth):        #Finding the MAX
        moves = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex,action) for action in moves]
        x = -float('inf')
        for successor in successors:
            x = max(x, self.value(successor,1,depth))
        return x
        
    def Minfunc(self, gameState, agentIndex, depth):        #Finding the MIN
        moves = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex,action) for action in moves]
        x = float('inf')
        for successor in successors:
            if agentIndex + 1 == gameState.getNumAgents():
                x = min(x, self.value(successor,0,depth + 1))
            else:
                x = min(x, self.value(successor,agentIndex + 1,depth))
        return x
        
    def value(self,gameState,agentIndex,depth):
        print("Turn right now : ",agentIndex)
        #If the state is terminal --> return state utility
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #If it is Pacman's turn --> return MAX
        if agentIndex == 0:
            return self.Maxfunc(gameState,agentIndex,depth)
        #If it is not Pacman's turn --> return MIN
        if agentIndex > 0:
            return self.Minfunc(gameState,agentIndex,depth)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self,gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def max_value(gameState,agentIndex,depth,alpha,beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            x = float("-inf")
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                x = max(x, min_value(successor,1,depth,alpha,beta))
                if x > beta:
                    return x    #It is pruning timee
                alpha = max(alpha,x)    #Update alpha with the max value
            return x

        def min_value(gameState,agentIndex,depth,alpha,beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            x = float("inf")
            nextAgentIndex = agentIndex + 1 if agentIndex + 1 < gameState.getNumAgents() else 0
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                if nextAgentIndex == 0:
                    x = min(x, max_value(successor,nextAgentIndex,depth + 1,alpha,beta))
                else:
                    x = min(x, min_value(successor,nextAgentIndex,depth,alpha,beta))
                if x < alpha:
                    return x #Prune the damn tree
                beta = min(beta, x) #Update beta with the min value
            return x

        alpha = float("-inf")
        beta = float("inf")
        best_action = None
        Maxfunc = float("-inf")
        moves = gameState.getLegalActions(0)
        for action in moves:
            successor = gameState.generateSuccessor(0, action)
            actionValue = min_value(successor, 1, 0, alpha, beta)
            if actionValue > Maxfunc:
                Maxfunc = actionValue
                best_action = action
            alpha = max(alpha, Maxfunc) #Updating alpha with the max value that we can find

        return best_action
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        moves moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
