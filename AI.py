import time, copy

# Function to calculate the best move for the AI
# It takes the current state of the game and tries out every outcome for the highest chance to win
def bestMove(currentState):
    bestScore = float("-inf")
    command = ""
    moves = possibleMovesSingle(currentState)
    for move in moves:
        newState = updateState(copy.deepcopy(currentState), move)
        score = minimax(newState, 0, False)
        if score > bestScore:
            bestScore = score
            command = move
    return command

# RIGHT NOW THE FUNCTION FAILS AS IT KEEPS THE APPENDED VERSION OF THE LIST
def minimax(currentState, depth, isMaximizing):
    result = checkGameOver(currentState)
    if result:
        if depth % 2 == 0:
            return 1
        else:
            return -1
    moves = possibleMovesSingle(currentState)
    if isMaximizing:
        for move in moves:
            newState = updateState(copy.deepcopy(currentState), move)
            bestScore = float("-inf")
            score = 0
            score = minimax(newState, depth + 1, False)
            bestScore = max(score, bestScore)
    else:
        for move in moves:
            newState = updateState(copy.deepcopy(currentState), move)
            bestScore = float("inf")
            score = 0
            score = minimax(newState, depth + 1, True)
            bestScore = min(score, bestScore)
    return bestScore

# This function checks the current state of the board and returns the remaining valid moves
def possibleMoves(currentState):
    possibleMoves = []
    for i, point in enumerate(currentState):
        amount = len(point)
        if amount < 2:
            possibleMoves.append("%d %d" % (i+1, i+1))
        if amount != 3:
            for j, x in enumerate(currentState):
                if i == j:
                    continue
                elif len(x) != 3:
                    possibleMoves.append("%d %d" % (i+1, j+1))
    return possibleMoves

# This function checks the current state of the board and returns the remaining valid moves (no duplicates)
def possibleMovesSingle(currentState):
    possibleMoves = []
    for i, point in enumerate(currentState):
        amount = len(point)
        if amount < 2:
            possibleMoves.append("%d %d" % (i+1, i+1))
        if amount != 3:
            for j, x in enumerate(currentState):
                if i >= j:
                    continue
                elif len(x) != 3:
                    possibleMoves.append("%d %d" % (i+1, j+1))
    return possibleMoves

# This function checks if a command is valid in the current state of the game
def checkValidMove(currentState, command):
    moves = possibleMoves(currentState)
    for move in moves:
        if move == command:
            return True
    return False

# This function takes the current state of the game and a command and returns the new game state
def updateState(currentState, command):
    p1, p2 = command.split()
    p1 = int(p1)
    p2 = int(p2)
    currentState.append([p1,p2])
    currentState[p1-1].append(len(currentState))
    currentState[p2-1].append(len(currentState))
    return currentState

# This function creates a new game with a specified amount of points
def startGame(amount):
    state = []
    for i in range(amount):
        state.append([])
    return state

# This function checks whether the player if they want to play against another player or the AI
def chooseSecondPlayer():
    opponent = ""
    while opponent == "":
        print("Choose if oppenent should be: 'player' or 'AI'")
        opponent = input()
        if opponent != 'player' and opponent != 'AI':
            opponent = ""
        else:
            if opponent == 'player':
                return "player 2"
            else:
                return "AI"

# This function checks whether the player wants the player or the AI to go first if the oppenent is the AI
def choosePlayerOne():
    player1 = ""
    while player1 == "":
        print("Choose if you are going first or second: 'first' or 'second'")
        player1 = input()
        if player1 != 'first' and player1 != 'second':
            player1 = ""
        else:
            if player1 == 'first':
                return ["player 1","AI"]
            else:
                return ["AI","player 1"]

# This function checks the amount of start points the player wants in a new game
def choosePointAmount():
    amount = ""
    while 1:
        print("How many points do you want?")
        try:
            amount = int(input())
            if 0 <= amount:
                break
        except ValueError:
            continue
    return amount

# This function returns the next player in line
# It can handle more than 2 players
def nextPlayer(currentPlayer, players):
    if currentPlayer == len(players)-1:
        return 0
    else:
        return currentPlayer + 1

# This function checks if there are any valid moves left in the current game state
# Also used by the AI to check for states where the AI wins and where the player wins
def checkGameOver(currentState):
    moves_remaining = possibleMoves(currentState)
    if len(moves_remaining) == 0:
        return True
    return False

second_player = chooseSecondPlayer()
if second_player == 'AI':
    players = choosePlayerOne()
else:
    players = ["player 1", "Player 2"]
currentPlayer = 0

amount = choosePointAmount()

currentState = startGame(amount)

while 1:
    print("")
    print(currentState)
    print("")

    if players[currentPlayer] == 'AI':
        command = bestMove(currentState)
        print("The AI entered the command: %s" % (command))
    else:
        command = input("Please enter a command %s: " % (players[currentPlayer]))
    if checkValidMove(currentState,command):
        currentState = updateState(currentState, command)
    else:
        print("Invalid move, try again")
        if players[currentPlayer] == 'AI':
            break
    if checkGameOver(currentState):
        print("Game Over - %s wins" % (players[currentPlayer]))
        break
    else:
        currentPlayer = nextPlayer(currentPlayer, players)

