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
        'color': '#8100FF',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'taunt': 'Insert meme here',
        'color': '#8100FF',
        'head': head_url,
        'head_type': 'safe',
        'tail_type': 'round-bum',
        'name': 'avoids-death-snake'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    direction = "derp"

    # Snake ID:
    mySnakeID = data["you"]

    # Get Own Snake
    mySnake = getOwnSnake(data)
    mySnakeHealthState = getCurrentHealthState(mySnake["health_points"])
    mySnakeLengthState = getCurrentLengthState(len(mySnake["coords"]))

    mySnakeHeadPos = getMySnakeHeadPos(mySnake)
    mySnakeNeckPos = getMySnakeNeckPos(mySnake)


    graph, TRANSLATE = buildMatrix(data)

    snake_state = "normal"

    height = data["height"]
    width = data["width"]


    taunt = 'I hope I dont die lol'

    possibleMoves = getPossibleMovesSansGraph(mySnakeHeadPos,mySnakeNeckPos,data["snakes"],height,width)
    possibleMoveStrings = []
    for move in possibleMoves:
        possibleMoveStrings.append(getMoveStringFromMoveVector(move))
    direction = random.choice(possibleMoveStrings)
    print "DIRECTION"
    print direction
    # Get next move from path
    if direction == 'derp':
        # We're screwed at this point
        taunt = 'nvm'
    else:
        taunt = 'I will not die this turn.'

    return {
        'move': direction,
        'taunt': taunt
    }

def getOwnSnake(data):
    snakes = data["snakes"]
    print data
    mySnake = None
    for snake in snakes:
        if snake["id"] == data["you"]:
            mySnake = snake
            break
    print mySnake
    return mySnake

def getNextMoveFromPath():
    pass

def getPossibleMovesSansGraph(headPos,neckPos,snakes,height,width):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    moves_to_remove = []
    for move in moves:
        removed = False
        # check if out of bounds
        if not (0 <= headPos[0] + move[0] < height and 0 <= headPos[1] + move[1] < width):
            moves_to_remove.append(move)
        elif headPos[0] + move[0] == neckPos[0] and headPos[1] + move[1] == neckPos[1]:
            #run into our own neck: no thanks
            moves_to_remove.append(move)
        else:
            for snake in snakes:
                if not removed:
                    for coord in snake["coords"]:
                        # if snake["coords"].index(coord) == 0:
                        #     # is head. Avoid nearby
                        #     coord1 = (coord[0]+1,coord[1])
                        #     coord2 = (coord[0]-1,coord[1])
                        #     coord3 = (coord[0],coord[1]+1)
                        #     coord4 = (coord[0],coord[1]-1)
                        #     adjacent_coords = [coord1,coord2,coord3,coord4]
                        #     for othercoord in adjacent_coords:
                        #         if headPos[0] + move[0] == othercoord[0] and headPos[1] + move[1] == othercoord[1]:
                        #             moves_to_remove.append(move)
                        if headPos[0] + move[0] == coord[0] and headPos[1] + move[1] == coord[1]:
                            # we have overlap
                            moves_to_remove.append(move)
                            removed = True
                else:
                    break
    print "MOVES TO REMOVE: "
    for move in moves_to_remove:
        print move
        moves.remove(move)
    print "POSSIBLE MOVES: "
    for move in moves:
        print move
    return moves


def getPossibleMoves(headPos,neckPos,graph):
    dist = getDistance(headPos,neckPos)
    possibleMoves = []
    disallowedMoves = []
    if dist == (-1,0):
        disallowedMoves.append("left")
    elif dist == (0,-1):
        disallowedMoves.append("down")
    elif dist == (1,0):
        disallowedMoves.append("right")
    elif dist == (0,1):
        disallowedMoves.append("up")
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
    print "MOVE VECTOR IS "
    print moveVector

    move = "up"
    if moveVector == (-1,0):
        move = "left"
    elif moveVector == (0,1):
        move = "down"
    elif moveVector == (1,0):
        move = "right"
    elif moveVector == (0,-1):
        move = "up"

    print "AND THAT TURNED INTO "
    print moveVector
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
        length = len(coords)
        headPos = coords[0]
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
    headPos = coordList[0]
    print "headpos:" + str(headPos)
    return headPos

def getMySnakeNeckPos(mySnake):
    coordList = mySnake["coords"]
    length = len(coordList)
    neckPos = coordList[1]
    print "neckPos:" + str(neckPos)
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

    translate = {}
    # init graph with all 0s
    for n in range(height):
        for m in range(width):
            tempNode = Node(0,(m,n))
            translate[str((m,n))] = 0 # new

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
            translate[str(position)] = 1 # new

            rowList = rows[coord[1]]
            rowList[coord[0]] = tempNode
            rows[coord[1]] = rowList
            # 1 = obstacle

    foods = data["food"]
    for food in foods:
        # print snake

        position = (coord[0],coord[1])
        tempNode = Node(2,position)
        translate[str(position)] = 2 # new

        rowList = rows[coord[1]]
        rowList[coord[0]] = tempNode
        rows[coord[1]] = rowList
        # 2 = food/coin

    return rows, translate

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
        'taunt': 'fml'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
