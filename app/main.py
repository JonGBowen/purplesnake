import bottle
import pdb
import random
import os

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': ''
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data

    # Snake ID:
    mySnakeID = "ef9c2d70-3a48-4b40-a20f-7b02afcc9e5b"

    # Get Own Snake
    mySnake = getOwnSnake(data)
    mySnakeHealthState = getCurrentHealthState(mySnake["health"])
    mySnakeLengthState = getCurrentLengthState(len(mySnake["coords"]))

    mySnakeHeadPos = getMySnakeHeadPos(mySnake)
    mySnakeNeckPos = getMySnakeNeckPos(mySnake)

    graph = buildMatrix(data)

    snake_state = "normal"

    validMoves = getPossibleMoves(mySnakeHeadPos,mySnakeNeckPos,graph)
    # Transform int matrix to Node matrix.
    TRANSLATE = {0: 'o', 1: 'x', 2: 'g'}
    graph = [[Node(TRANSLATE[x], (i, j)) for j, x in enumerate(row)] for i, row in enumerate(graph)]
    # Find path
    path = None
    try:
        path = bfs(graph, mySnakeHeadPos)
        print("Path found: {!r}".format(path))
    except Exception as ex:
        # Learn to use exceptions. In your original code, "no path" situation
        # is not handled at all!
        print('ERROR')
        print(ex)

    taunt = ''
    # NEW STUFF HERE
    if path:
        closest_food = findClosestFoodFromPath(path)
        is_closest_to_food = check_if_closest_snake_head(data,mySnakeHeadPos,closest_food)
    else:
        is_closest_to_food = False

    if is_closest_to_food and Path:
        # move towards the food
        tempDist = getDistance(mySnakeHeadPos,path[1])
        move = getMoveStringFromMoveVector(tempDist)
        taunt = "this food pellet is mine"

        # TODO: Avoid bucket traps, L-traps

    # END NEW STUFF
    if path == None:
        path = [(0,0),(0,1)]
    # Get Possible Moves
    possibleMoves = getPossibleMoves(getMySnakeHeadPos,mySnakeNeckPos,graph)
    print path

    # Get next move from path
    if not move:
        # We're screwed at this point
        taunt = 'I hate you all !!!'
        movelist = ['north', 'south', 'east', 'west']
        move = random.choice(movelist)

    return {
        'move': move,
        'taunt': taunt
    }

def getOwnSnake(data):
    snakes = data["snakes"]
    mySnake = None
    for snake in snakes:
        if snake["id"] == "ef9c2d70-3a48-4b40-a20f-7b02afcc9e5b":
            mySnake = snake
            break
    print mySnake
    return mySnake

def getNextMoveFromPath():
    pass

def getPossibleMoves(headPos,neckPos,graph):
    dist = getDistance(headPos,neckPos)
    possibleMoves = []
    disallowedMoves = []
    if dist == (-1,0):
        disallowedMoves.append()
    elif dist == (0,-1):
        disallowedMoves.append("south")
    elif dist == (1,0):
        disallowedMoves.append("east")
    elif dist == (0,1):
        disallowedMoves.append("north")
    disallowedMoves.append(dist)

    if (-1,0) not in disallowedMoves:
        possibleMoves.append((-1,0))
    if (0,-1) not in disallowedMoves:
        possibleMoves.append((0,-1))
    if (1,0) not in disallowedMoves:
        possibleMoves.append((1,0))
    if (0,1) not in disallowedMoves:
        possibleMoves.append((0,1))

    return possibleMoves

def getMoveStringFromMoveVector(moveVector):
    move = "north"
    if moveVector == (-1,0):
        move = "west"
    elif moveVector == (0,-1):
        move = "south"
    elif moveVector == (1,0):
        move = "east"
    elif moveVector == (0,1):
        move = "north"
    return move

def getDistance(coord1,coord2):
    print "GET DISTANCE HERE"
    print coord1
    print coord2
    dX = coord1[0] - coord2[0]
    dY = coord1[1] - coord2[1]
    vectorDistance = (dX,dY)
    return vectorDistance

def findClosestFood(data):
    pass

def findClosestFoodFromPath(Path):
    length = len(Path)
    return Path[length-1]
    pass

def manhattan(a, b):
   # Manhattan distance on a square grid
   return abs(a.x - b.x) + abs(a.y - b.y)

def get_x_distance(a, b):
   # Manhattan distance on a square grid
   return abs(a.x - b.x)

def get_y_distance(a, b):
   # Manhattan distance on a square grid
   return abs(a.y - b.y)

def super_conservative_closest():
    return "Jon"

def check_if_closest_snake_head(data,my_head_pos,closest_food_coord):
    snakes = data["snakes"]
    for snake in snakes:
        # print snake
        coords = snake.get("coords")[0]
        length = len(coordList)
        headPos = coordList[length-1]
        other_snake_distance_to_food = manhattan(closest_food_coord,headPos)
        if other_snake_distance_to_food > manhattan(closest_food_coord,my_head_pos):
            return True
    return False


def getCurrentHealthState(health):
    if (health > 55):
        return "healthy"
    elif (health > 40):
        return "intermediate"
    elif (health > 20):
        return "hungry"
    else:
        return "berserk"

def getCurrentLengthState(length_of_snake):
    if (length_of_snake > 20):
        return "large"
    elif (length_of_snake  > 10):
        return "medium"
    elif (length_of_snake  > 4):
        return "short"
    else:
        return "super_short"

def getTaunt(snake_state):
    return "DEFAULT TAUNT!!!!"

def getMySnakeHeadPos(mySnake):
    coordList = mySnake["coords"]
    length = len(coordList)
    headPos = coordList[length-1]
    print headPos
    return headPos

def getMySnakeNeckPos(mySnake):
    coordList = mySnake["coords"]
    length = len(coordList)
    neckPos = coordList[length-2]
    return neckPos

class Node:
    def __init__(self, val, pos):
        self.val = val
        # Position info is stored here and ALSO as index in graph -
        # this is a form of data duplication, which is evil!
        self.pos = pos
        self.visited = False
    def __repr__(self):
        # nice repr for pprint
        return repr(self.pos)

# You had mistake here, "arena" instead of "graph"
# Before posting questions on stackoverflow, make sure your examples
# at least produce some incorrect result, not just crash.
# Don't make people fix syntax errors for you!

def buildMatrix(data):
    width = data['width']
    height = data["height"]
    tempRow = []
    rows = []
    # init graph with all 0s
    for n in range(height):
        for m in range(width):
            tempNode = Node(0,(m,n))
            tempRow.append(tempNode)
        rows.append(tempRow)
        tempRow = []
    # add obstacles
    snakes = data["snakes"]
    for snake in snakes:
        # print snake
        coords = snake.get("coords")
        # coords = snake["coords"]
        for coord in coords:
            position = (coord[0],coord[1])
            tempNode = Node(1,position)

            rowList = rows[coord[1]]
            rowList[coord[0]] = tempNode
            rows[coord[1]] = rowList
            # 1 = obstacle

    if "walls" in data:
        walls = data["walls"]
        for wall in walls:
            position = (wall[0],wall[1])
            tempNode = Node(3,position)

            rowList = rows[coord[1]]
            rowList[coord[0]] = tempNode
            rows[coord[1]] = rowList

    foods = data["food"]
    for food in foods:
        # print snake

        position = (coord[0],coord[1])
        tempNode = Node(2,position)

        rowList = rows[coord[1]]
        rowList[coord[0]] = tempNode
        rows[coord[1]] = rowList
        # 2 = food/coin

    # coins = data["gold"]
    # for coin in coins:
    #     # print snake

    #     position = (coord[0],coord[1])
    #     tempNode = Node(2,position)

    #     rowList = rows[coord[1]]
    #     rowList[coord[0]] = tempNode
    #     rows[coord[1]] = rowList
    #     # 2 = food/coin

    return rows

def bfs(graph, startPos):
    start = Node(1,startPos)
    fringe = [[start]]
    # Special case: start == goal
    if start.val == 2:
        return [start]
    start.visited = True
    # Calculate width and height dynamically. We assume that "graph" is dense.
    width = len(graph[0])
    height = len(graph)
    print "width "
    print width
    print "height "
    print height
    # List of possible moves: up, down, left, right.
    # You can even add chess horse move here!
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Remove backwards move as it is invalid
    while fringe:
        # # Print fringe at each step
        # print fringe
        # print('')
        # Get first path from fringe and extend it by possible moves.
        path = fringe.pop(0)
        node = path[-1]
        pos = node.pos
        # Using moves list (without all those if's with +1, -1 etc.) has huge benefit:
        # moving logic is not duplicated. It will save you from many silly errors.
        # The example of such silly error in your code:
        # graph[pos[0-1]][pos[1]].visited = True
        #           ^^^
        # Also, having one piece of code instead of four copypasted pieces
        # will make algorithm much easier to change (e.g. if you want to move diagonally).
        for move in moves:
            # Check out of bounds. Note that it's the ONLY place where we check it. Simple and reliable!
            if not (0 <= pos[0] + move[0] < height and 0 <= pos[1] + move[1] < width):
                continue
            neighbor = graph[pos[0] + move[0]][pos[1] + move[1]]
            print(type(neighbor))
            print(neighbor.val)
            if neighbor.val == 2:
                print ("found something")
                return path + [neighbor]
            elif neighbor.val == 1 and not neighbor.visited:
                neighbor.visited = True
                fringe.append(path + [neighbor])  # creates copy of list
    raise Exception('Path not found!')
#pdb.set_trace()
@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'we got disssssss'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
