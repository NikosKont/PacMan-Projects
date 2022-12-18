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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if successorGameState.isWin():
          return float("inf")

        nearestGhostDist = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        if nearestGhostDist < 2:
          return float("-inf")

        pos = currentGameState.getPacmanPosition()
        food = currentGameState.getFood()
        capsules = successorGameState.getCapsules()
        foodLeft = len(food.asList())
        newFoodLeft = len(newFood.asList())
        minFoodDist = min([manhattanDistance(newPos, food) for food in newFood.asList()])
        maxFoodDist = max([manhattanDistance(newPos, food) for food in newFood.asList()])

        scoreDiff = successorGameState.getScore() - currentGameState.getScore()
        foodChanged = bool(foodLeft - newFoodLeft)
        minMaxDist = maxFoodDist - minFoodDist
        minCapsDist = 0 if not capsules \
                    else min([manhattanDistance(newPos, capsule) for capsule in capsules])

        return scoreDiff + minMaxDist -5*minCapsDist - (minFoodDist if not foodChanged else 0)

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
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        def max_value(state, depth=0):
          if depth == self.depth or state.isWin() or state.isLose():
              return self.evaluationFunction(state)

          v = float("-inf")
          for action in state.getLegalActions(0):
            v2 = min_value(state.generateSuccessor(0, action), depth=depth)

            if v2 > v:
              v = v2
              if depth == 0:
                move = action

          if depth == 0:
            return move
          return v

        def min_value(state, agent=1, depth=0):
          if state.isWin() or state.isLose():
              return self.evaluationFunction(state)

          v = float("inf")
          for action in state.getLegalActions(agent):
            if agent == state.getNumAgents() - 1:
              v2 = max_value(state.generateSuccessor(agent, action), depth + 1)
            else:
              v2 = min_value(state.generateSuccessor(agent, action), agent + 1, depth)

            if v2 < v:
              v = v2

          return v


        return max_value(gameState)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def max_value(state, alpha=float("-inf"), beta=float("inf"), depth=0):
          if depth == self.depth or state.isWin() or state.isLose():
              return self.evaluationFunction(state)

          v = float("-inf")
          for action in state.getLegalActions(0):
            v2 = min_value(state.generateSuccessor(0, action),
                          alpha=alpha, beta=beta, depth=depth)

            if v2 > v:
              v = v2
              if depth == 0:
                move = action
            if v > beta:
              return v
            alpha = max(alpha, v)

          if depth == 0:
            return move
          return v

        def min_value(state, agent=1, alpha=float("-inf"), beta=float("inf"), depth=0):
          if state.isWin() or state.isLose():
              return self.evaluationFunction(state)

          v = float("inf")
          for action in state.getLegalActions(agent):
            if agent == state.getNumAgents() - 1:
              v2 = max_value(state.generateSuccessor(agent, action), alpha, beta, depth + 1)
            else:
              v2 = min_value(state.generateSuccessor(agent, action), agent + 1, alpha, beta, depth)

            if v2 < v:
              v = v2
            if v < alpha:
              return v
            beta = min(beta, v)

          return v


        return max_value(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
          The expectimax function returns a tuple of (actions,
        """

        def max_value(state, depth=0):
          if depth == self.depth or state.isWin() or state.isLose():
              return self.evaluationFunction(state)

          v = float("-inf")
          for action in state.getLegalActions(0):
            v2 = exp_value(state.generateSuccessor(0, action), depth=depth)

            if v2 > v:
              v = v2
              if depth == 0:
                move = action

          if depth == 0:
            return move
          return v

        def exp_value(state, agent=1, depth=0):
          if state.isWin() or state.isLose():
              return self.evaluationFunction(state)

          v = float(0)
          for action in state.getLegalActions(agent):
            if agent == state.getNumAgents() - 1:
              v2 = max_value(state.generateSuccessor(agent, action), depth + 1)
            else:
              v2 = exp_value(state.generateSuccessor(agent, action), agent + 1, depth)

            v += float(v2)

          return v / float(len(state.getLegalActions(agent)))


        return max_value(gameState)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
      Evaluate state by  :
            * closest food
            * food left
            * capsules left
            * distance to ghost
    """

    if currentGameState.isWin():
      return float("inf")

    pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    nearestGhostDist = min([manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates])
    if nearestGhostDist < 1:
      return float("-inf")

    score = currentGameState.getScore()
    food = currentGameState.getFood()
    foodLeft = len(food.asList())
    capsules = currentGameState.getCapsules()
    capsulesLeft = len(capsules)
    closestFoodDist = min([manhattanDistance(pos, food) for food in food.asList()])
    closestCapsDist = 0 if not capsulesLeft \
                else min([manhattanDistance(pos, capsule) for capsule in capsules])

    return score -closestFoodDist -closestCapsDist -5*foodLeft -15*capsulesLeft

# Abbreviation
better = betterEvaluationFunction
