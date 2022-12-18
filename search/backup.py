    def distance(x, y):
        return mazeDistance(x, y, problem.startingGameState)
        # return abs(x[0] - y[0]) + abs(x[1] - y[1])

    distance = lambda x: mazeDistance(x, position, problem.startingGameState)

    position, foodGrid = state
    foodList = foodGrid.asList()
    totalDistance = 0

    # initial-cleanedv1 (incorrect) (160/6.5)
    foodList.sort(key=lambda food: distance(food))
    while foodList:
        nearestFood = foodList.pop(0)
        totalDistance += distance(nearestFood)
        position = nearestFood

    # initial-cleanedv2 (incorrect) (160/6.4)
    foodList.sort(key=lambda food: distance(food))
    for nearestFood in foodList:
        totalDistance += distance(nearestFood)
        position = nearestFood

    # optimized (160/4.6)
    foodList.sort(key=lambda food: distance(food))
    for nearestFood in foodList:
        key = position + nearestFood
        if key not in problem.heuristicInfo:
            problem.heuristicInfo[key] = distance(nearestFood)

        totalDistance += problem.heuristicInfo[key]
        position = nearestFood

    # slow but better (134/155)
    while foodList:
        foodList.sort(key=lambda x: distance(x))
        nearestFood = foodList.pop(0)
        key = position + nearestFood

        if key not in problem.heuristicInfo:
            problem.heuristicInfo[key] = distance(nearestFood)

        totalDistance += problem.heuristicInfo[key]
        position = nearestFood

    # optimized (129.4/155)
    while foodList:
        nearestFood = min(foodList, key=lambda x: distance(x))
        foodList.remove(nearestFood)
        key = position + nearestFood

        if key not in problem.heuristicInfo:
            problem.heuristicInfo[key] = distance(nearestFood)

        totalDistance += problem.heuristicInfo[key]
        position = nearestFood


    # corect mine
    foodList.sort(key=distance)
    foodList.reverse()
    return distance(foodList[0])

    # corect mine optimized
    return max([distance(food) for food in foodList])


    # correct
    maxDistance = 0
    for food in foodList:
        key = position + food
        if key not in problem.heuristicInfo:
            problem.heuristicInfo[key] = mazeDistance(position, food, problem.startingGameState)

        distance = problem.heuristicInfo[key]

        if distance > maxDistance:
            maxDistance = distance

    return maxDistance

    def manhattanDistance(foodPos, position):
        return abs(foodPos[0] - position[0]) + abs(foodPos[1] - position[1])

    def foodManhattanDistance(foodPos):
        return abs(foodPos[0] - position[0]) + abs(foodPos[1] - position[1])

    def FoodQueue(foodList):
        foodQueue = util.PriorityQueueWithFunction(foodManhattanDistance)
        for food in foodList:
            foodQueue.push(food)
        return foodQueue

    # initial
    totalDistance = 0
    while foodList:
        foodList.sort(key=lambda food: foodManhattanDistance(food, position))
        foodPos = foodList.pop(0)
        totalDistance += foodManhattanDistance(foodPos, position)
        position = foodPos

    # initial with queue
    foodList = foodGrid.asList()
    queue = util.PriorityQueueWithFunction(foodManhattanDistance)
    for food in foodList:
        queue.push(food)

    totalDistance = 0
    while not queue.isEmpty():
        foodPos = queue.pop()
        totalDistance += foodManhattanDistance(foodPos)
        # position = foodPos



def bestFirstSearch(problem: SearchProblem, f=nullHeuristic):
    """Search the node that has the lowest heuristic first."""
    startState = problem.getStartState()
    startNode = Node(startState, [], 0)
    frontier = util.PriorityQueue()
    frontier.push(startNode, f(startNode, problem))
    # explored = set(startState)
    explored = dict()
    # explored = {startState: startNode}
    path = []

    while not frontier.isEmpty():
        node = frontier.pop()

        if problem.isGoalState(node.state):
            return node.path

        if node.state not in explored or node.pathCost < explored[node.state].pathCost:
            explored[node.state] = node
            frontier.update(node, f(node, problem))

        path = node.path

        for successor, action, cost in problem.getSuccessors(node.state)[::-1]:
            path = path + [action]
            child = Node(successor, path, node.pathCost + cost)
            # if child.state not in explored or child.pathCost < explored[child.state].pathCost:
            if child.state not in explored:
                # explored[successor] = child
                frontier.push((child), f(child, problem))

    # while not frontier.isEmpty():
    #     state, path = frontier.pop()
    #     if problem.isGoalState(state):
    #         return path
    #     if state not in explored:
    #         explored.add(state)
    #         for successor, action, cost in problem.getSuccessors(state):
    #             frontier.push((successor, path + [action]), heuristic(successor, problem))
    return path




# 2&3
def bestFirstSearch(problem: SearchProblem, f=nullHeuristic):
    """Search the node that has the lowest heuristic first."""
    startState = problem.getStartState()
    startNode = Node(startState, [], 0)
    frontier = util.PriorityQueue()
    frontier.push(startNode, f(startNode, problem))
    # explored = set(startState)
    # explored = dict()
    explored = {startState: startNode}
    path = []

    while not frontier.isEmpty():
        node = frontier.pop()
        path = node.path

        if problem.isGoalState(node.state):
            return node.path

        # if node.state not in explored or node.pathCost < explored[node.state].pathCost:
        #     explored[node.state] = node
        #     frontier.update(node, f(node, problem))

        for successor, action, cost in problem.getSuccessors(node.state)[::-1]:
            path = node.path + [action]
            child = Node(successor, path, node.pathCost + cost)
            if child.state not in explored or child.pathCost < explored[child.state].pathCost:
                explored[successor] = child
                frontier.push((child), f(child, problem))

    # while not frontier.isEmpty():
    #     state, path = frontier.pop()
    #     if problem.isGoalState(state):
    #         return path
    #     if state not in explored:
    #         explored.add(state)
    #         for successor, action, cost in problem.getSuccessors(state):
    #             frontier.push((successor, path + [action]), heuristic(successor, problem))
    return path