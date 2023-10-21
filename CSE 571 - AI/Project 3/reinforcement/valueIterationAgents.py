# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.states = mdp.getStates()
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for iter in range(self.iterations):
            newValues = util.Counter() # new counter for the new values
            for state in self.states:
                if not self.mdp.isTerminal(state):      #to check whether it isnt a terminal state
                    qValues = []
                    actions = self.mdp.getPossibleActions(state)    #getting them actions for us to move
                    for action in actions:
                        qValues.append(self.computeQValueFromValues(state,action))      #append the values of the next states
                        newValues[state] = max(qValues)         #finding the max 
            self.values = newValues
            iter = iter + 1


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transitionState = self.mdp.getTransitionStatesAndProbs(state, action)   #getting the new transition states
        qValue = 0.0      
        for nextState,prob in transitionState:
            qValue = qValue + (prob*(self.mdp.getReward(state,action,nextState) + self.discount*self.values[nextState]))    #Finding new Qvalue

        return qValue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        qMax = -float('inf')
        bestAction = None
        for action in actions:
            qValue = self.computeQValueFromValues(state,action)         
            if qValue > qMax:
                qMax = qValue
                bestAction = action
        
        return bestAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        for iteration in range(self.iterations):
            state = self.states[iteration % len(self.states)]
            if not self.mdp.isTerminal(state):
                # Initialize the value of the state to a low value
                newValue = -float('inf')
                # Calculate the new value for the state (state)
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.computeQValueFromValues(state, action)
                    newValue = max(newValue, qValue)
                # Update self.values[state] with the new value
                self.values[state] = newValue

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def computePredecessors(self):
        predecessors = {}
        states = self.mdp.getStates()
        for state in states:
            predecessors[state] = set()

        for state in states:
            for action in self.mdp.getPossibleActions(state):
                transitions = self.mdp.getTransitionStatesAndProbs(state, action)
                for nextState, prob in transitions:
                    if prob > 0:
                        predecessors[nextState].add(state)

        return predecessors

    def runValueIteration(self):
        predecessors = self.computePredecessors()
        queue = util.PriorityQueue()

        for state in self.states:
            if not self.mdp.isTerminal(state):
                qValues = [self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)]
                diff = abs(self.values[state] - max(qValues))
                queue.update(state, -diff)

        for _ in range(self.iterations):
            if queue.isEmpty():
                break

            state = queue.pop()

            if not self.mdp.isTerminal(state):
                qValues = [self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)]
                self.values[state] = max(qValues)

            for predecessor in predecessors[state]:
                qValues = [self.computeQValueFromValues(predecessor, action) for action in self.mdp.getPossibleActions(predecessor)]
                diff = abs(self.values[predecessor] - max(qValues))
                if diff > self.theta:
                    queue.update(predecessor, -diff)


