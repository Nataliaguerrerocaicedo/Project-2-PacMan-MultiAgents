# multiAgents.py
# --------------
# Grupo: Alejandro Ayala y Natalia Guerrero

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #PUNTO 1
        """
        Un agente de reflejos capaz tendrá que considerar tanto la ubicación de los
        alimentos como la ubicación de los fantasmas para funcionar bien
        """
        #El pacman se centra en comer, si el fantasma está cerca, el pacman no se aproxima

        comidaPos = successorGameState.getFood().asList() #Lista que contiene las posiciones en donde se encuentra la comida
        minComida = float("inf") #Distancia mínima entra la posición del pacman y la comida, inicializado como "infinito"
        for comida in comidaPos:
            ##Iterando sobre todas las posiciones de la comida, buscando la distancia más corta entre el pacman y la comida
            if( manhattanDistance(newPos,comida) < minComida ):
                #Calcula la distancia de manhattan, si la distancia que calculó es menor que la distancia que tenía entonces la actualiza
                minComida = manhattanDistance(newPos,comida)

        #Verificando si hay algún fanstasma cerca
        for fantasma in successorGameState.getGhostPositions():
            ##Iterando sobre todas las posiciones de los fantasmas
            if(manhattanDistance(newPos, fantasma) < 2):
                #La posición del fantasma está a una casilla de adyacencia, es decir, está súper cerca
                return -float('inf') #Como el fantasma está muy cerca el puntaje que debe retornar debe ser el más pequeño dado que entre más alto el puntaje que retorne mejor puntaje tiene

        ##Entre más pequeña haya sido la menor distancia entre el pacman y la comida, significa que el puntaje será más alto debido a que al dividir 1 entre esa distancia no va a tender tanto a 0.
        return successorGameState.getScore() + 1.0/minComida

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #PUNTO 2
        return self.maxval(gameState, 0, 0)[0]

    def minimax(self, gameState, agentIndex, depth):
        if depth is self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            ##Si en la profundidad del arbol se llega a que el estado es final
            ##Evalúa el estado en el que se encuentra con la función de evaluación
            return self.evaluationFunction(gameState)
        if agentIndex is 0:
            ##Si es el pacman, es decir el indice es 0, el pacman intentará sacar el puntaje máximo para él mismo
            return self.maxval(gameState, agentIndex, depth)[1]
        else:
            ##Si no es el pacman, es decir son los fantasmas, ellos intentarán sacar el mínimo puntaje para el pacman, es decir, un puntaje que empeore a pacman
            return self.minval(gameState, agentIndex, depth)[1]

    def maxval(self, gameState, agentIndex, depth):
        ## Empieza con el gameState, agentIndex = 0, depth = 0

        ## El pacman necesita sacar el mayor puntaje posible
        mejorJugada = ("max", -float("inf")) # ("max", -inf), para sacar el mayor
        for accion in gameState.getLegalActions(agentIndex):
            #las acciones que puede hacer según el indice del agente, es decir el pacman
            accionSucesora = (accion, self.minimax(gameState.generateSuccessor(agentIndex, accion),
                                                (depth + 1)%gameState.getNumAgents(), depth +1))
            if accionSucesora[1] > mejorJugada[1]:
                #Aquí se cumple que puede tener un mayor puntaje que el que tenía antes
                mejorJugada = accionSucesora
        return mejorJugada

    def minval(self, gameState, agentIndex, depth):
        ## Los fantasmas necesitan empeorar el puntaje de pacman, es decir, necesitan hacer que pacman saque el menor puntaje

        peorJugada = ("min", float("inf")) # ("min", inf)
        for accion in gameState.getLegalActions(agentIndex): #las acciones que puede hacer segun el agente
            accionSucesora = (accion, self.minimax(gameState.generateSuccessor(agentIndex, accion),
                                                (depth + 1)%gameState.getNumAgents(), depth +1))
            if accionSucesora[1] < peorJugada[1]:
                ##Aquí se cumple que se puede empeorar el puntaje que tenía el pacman, entonces se actualiza la peor jugada para el pacman
                peorJugada = accionSucesora
        return peorJugada

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #PUNTO 3

        return self.maxval(gameState, 0, 0, -float("inf"), float("inf"))[0]


    #se agrega alpha y beta
    def alphaBeta(self, gameState, agentIndex, depth, alpha, beta):
        if depth is self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            #Llega al final del arbol, gana o pierde, condicion terminal
            return self.evaluationFunction(gameState)
        if agentIndex is 0:
            #Si es el pacman se busca maximizar (alpha)
            return self.maxval(gameState, agentIndex, depth, alpha, beta)[1]
        else:
            #Si son los fantasmas se busca minimizar (beta)
            return self.minval(gameState, agentIndex, depth, alpha, beta)[1]

    def maxval(self, gameState, agentIndex, depth, alpha, beta):
        #Esta función es la del pacman, se busca maximizar alpha
        mejorJugada = ("max", -float("inf")) #("max", -inf)
        for accion in gameState.getLegalActions(agentIndex):
            #las acciones que puede hacer segun el agente (pacman)
            accionSucesora = (accion, self.alphaBeta(gameState.generateSuccessor(agentIndex, accion),
                                                (depth + 1)%gameState.getNumAgents(), depth +1, alpha, beta))
            if accionSucesora[1] > mejorJugada[1]:
                mejorJugada = accionSucesora
            #La poda se produce si en algún momento α≥β
            #alpha es para nodos MAX

            if mejorJugada[1] > beta:
                ##El pacman consiguió ganarle a los fantasmas
                return mejorJugada
            else:
                if mejorJugada[1] > alpha:
                    alpha = mejorJugada[1]

        return mejorJugada

    def minval(self, gameState, agentIndex, depth, alpha, beta):
        #Esta función es la de los fantasmas, se busca minimizar beta
        peorJugada = ("min", float("inf")) # ("min", inf)
        for accion in gameState.getLegalActions(agentIndex): #las acciones que puede hacer segun el agente
            accionSucesora = (accion, self.alphaBeta(gameState.generateSuccessor(agentIndex, accion),
                                            (depth + 1)%gameState.getNumAgents(), depth +1, alpha, beta))
            if accionSucesora[1] < peorJugada[1]:
                peorJugada = accionSucesora

            #beta es para nodos MIN

            if peorJugada[1] < alpha:
                #Logró encontrar una jugada que le gana al pacman
                return peorJugada
            else:
                if peorJugada[1] < beta:
                    ##Encontró una peor jugada
                    beta = peorJugada[1]

        return peorJugada

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxval(gameState, 0, 0)[0]

    def minimax(self, gameState, agentIndex, depth):
        if depth is self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin(): #que llega al final del arbol?? si gana o pierde, condicion terminal
            return self.evaluationFunction(gameState)
        if agentIndex is 0: # es el pacman
            return self.maxval(gameState, agentIndex, depth)[1]
        else:
            return self.minval(gameState, agentIndex, depth)[1]

    def maxval(self, gameState, agentIndex, depth):
        mejorJugada = ("max", -float("inf"))
        for accion in gameState.getLegalActions(agentIndex): #las acciones que puede hacer segun el agente
            succAccion = (accion, self.minimax(gameState.generateSuccessor(agentIndex, accion), (depth + 1)%gameState.getNumAgents(), depth +1))
            mejorJugada = max(mejorJugada, succAccion, key = lambda x:x[1])
        return mejorJugada

    def minval(self, gameState, agentIndex, depth):
        mejorJugada = ("min", float("inf"))
        for accion in gameState.getLegalActions(agentIndex): #las acciones que puede hacer segun el agente
            succAccion = (accion, self.minimax(gameState.generateSuccessor(agentIndex, accion), (depth + 1)%gameState.getNumAgents(), depth +1))
            mejorJugada = min(mejorJugada, succAccion, key = lambda x:x[1])
        return mejorJugada

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #PUNTO 5
    posPacman = currentGameState.getPacmanPosition() #Posición del pacman
    stateFantasmas = currentGameState.getGhostStates() #Estado en el que se encuentran los fantasmas
    posFood = currentGameState.getFood().asList() #Lista de la posición de cada una de las comiditas
    score = currentGameState.getScore() #Puntaje
    numFood = currentGameState.getNumFood() #Cantidad de comiditas restantes
    
    disFood = [manhattanDistance(Food, posPacman) for Food in posFood] #Lista del manhattan entre cada comida y la posicion del pacman

    """
    Se revisa si hay comiditas en el mapa y considera la menor distancia de las comiditas como su peso
    """

    if len(disFood):
        minDisFood = min(disFood)
    else:
        minDisFood = 0

    """
    Se revisa la posición de cada uno de los fantasmas y se le da un peso a estos en el momento en el que el pacman
    tiene permitido comerlos
    """  
    scoreGhost = 0

    for ghost in stateFantasmas:
        disGhost = manhattanDistance(ghost.getPosition(), posPacman)
        if ghost.scaredTimer > disGhost:
            scoreGhost = scoreGhost - disGhost + 50
    
    return score - minDisFood - numFood + scoreGhost

# Abbreviation
better = betterEvaluationFunction