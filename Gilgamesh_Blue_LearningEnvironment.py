import numpy as np
import random as r
import matplotlib.pyplot as plt
import chess  as pychess

import Gilgamesh_Blue as g

board         = pychess.Board()
startGame_fen = pychess.STARTING_FEN

endOfGame = {'winner': None, "endType": {True: None, False: None}}

popList = g.create_first_generation(10, "G-Blue", 1)
popDict = {}
for i in range(len(popList)):
	popDict[i] = {"obj": popList[i], "dumb": False, "successfulMoves": 0, "failedThoughts": 0, "fitness": 0}
#next i

generationNumber = 2

def _translateColor(color):
	if color == True:
		return 'white'
	elif color == False:
		return 'black'
	else:
		log('Error:')
		log(' _translateColor(color)')
		return 'ERROR'

def _randMove():
	global board

	moveSet = []
	for move in board.legal_moves:
		moveSet.append(move)

	move = r.choice(moveSet)

	if move.promotion != None:
		move.promotion = r.choice([2, 3, 4, 5])
	else: pass

	print("returning random Move - {0}".format(board.san(move)))
	return move

def _gilgMove(popNum):
	global board
	global popDict

	gilg = popDict[popNum]
	print(gilg["obj"].name)

	if gilg["dumb"] is True:
		print("{0} is dumb - doing random move".format(popDict[popNum]["obj"].name))
		move = _randMove()
		return move
	else: 
		moveSet = []
		for move in board.legal_moves:
			moveSet.append(move)

		move = pychess.Move(gilg["obj"].pickPiece(), gilg["obj"].makeMove())
		if move.promotion != None:
			move.promotion = gilg["obj"].promotion()
		else: pass

		if move in moveSet:
			gilg["successfulMoves"] += 1
			print("returning Gilg Move - {0}".format(board.san(move)))
		else:
			gilg["failedThoughts"] += 1

			if gilg["failedThoughts"] >= 25:
				gilg["dumb"] = True

				print("{0} is dumb - Random agent taking over".format(popDict[popNum]["obj"].name))
				print("{0} is dumb - doing random move".format(popDict[popNum]["obj"].name))
				move = _randMove()
			else: 
				move = _randMove()

		print("{0} so far: {1} failedThoughts - {2} successfulMoves".format(popDict[popNum]["obj"].name, gilg["failedThoughts"], gilg["successfulMoves"]))
	return move

for genCount in range(generationNumber):
	genCount += 1
	print("Generation: " + str(genCount))

	for p1 in range(len(popDict)):
		for p2 in range(len(popDict)):
			# p1 is white
			# p2 is black

			if p2 > p1:
				board.set_fen(startGame_fen)

				while not board.is_game_over() and not (popDict[p1]["dumb"] and popDict[p2]["dumb"]):
					print("------------")
					print(popDict[p1]["obj"].name + " VS " + popDict[p2]["obj"].name)
					print(('Turn: {0}, Half-Turn: {1}').format(board.fullmove_number, board.halfmove_clock))
					print("Is {0}'s Turn".format(_translateColor(board.turn)))
					print(board)
					print("------------")
					print("")

					print("attampt Gilgamesh Move")
					if   board.turn == True:
						board.push(_gilgMove(p1))
					elif board.turn == False:
						board.push(_gilgMove(p2))
				#continue while

				print("")
				print("------------")
				print(popDict[p1]["obj"].name + " VS " + popDict[p2]["obj"].name)
				print(('Turn: {0}, Half-Turn: {1}').format(board.fullmove_number, board.halfmove_clock))
				print("Is {0}'s Turn".format(_translateColor(board.turn)))
				print(board)
				print("------------")

				if board.is_checkmate():
					endOfGame["winner"] = board.turn
					print(_translateColor(board.turn) + " has Won - Checkmate")
				if board.is_game_over() and not board.is_check():
					if board.is_stalemate():
						endOfGame["endType"][board.turn]     = "stalemate-ed"
						endOfGame["endType"][not board.turn] = "stalemate-er"
						print("Stalemate")
					else:
						endOfGame["endType"][True]  = "Other"
						endOfGame["endType"][False] = "Other"
						print("Draw")

				if popDict[p1]["successfulMoves"] == 0:
					popDict[p1]["dumb"] = True
				if popDict[p2]["successfulMoves"] == 0:
					popDict[p2]["dumb"] = True

				if popDict[p1]["dumb"] is True:
					endOfGame["endType"][True]  = "dumb"
					print(popDict[p1]["obj"].name + " is dumb - random took over")
				if popDict[p2]["dumb"] is True:
					endOfGame["endType"][False] = "dumb"
					print(popDict[p2]["obj"].name + " is dumb - random took over")

				print("------------")

				# if white wins endOfGame["winner"] = True, if black wins endOfGame["winner"] = False, else it = None
				if endOfGame["winner"] == None:
					win_p1     = None
					endType_p1 = endOfGame["endType"][True]
				else:
					win_p1     = endOfGame["winner"]
					endType_p1 = None

				successfulMoves_p1 = popDict[p1]["successfulMoves"]
				failedThoughts_p1  = popDict[p1]["failedThoughts"]

				if endOfGame["winner"] == None:
					win_p2     = None
					endType_p2 = endOfGame["endType"][False]
				else:
					win_p2     = not endOfGame["winner"]
					endType_p2 = None

				successfulMoves_p2 = popDict[p2]["successfulMoves"]
				failedThoughts_p2  = popDict[p2]["failedThoughts"]

				tempFitness_p1 = popDict[p1]["obj"].gradeFitness(win_p1, endType_p1, successfulMoves_p1, failedThoughts_p1)
				tempFitness_p2 = popDict[p2]["obj"].gradeFitness(win_p2, endType_p2, successfulMoves_p2, failedThoughts_p2)

				popDict[p1]["fitness"] = popDict[p1]["fitness"] + tempFitness_p1
				popDict[p2]["fitness"] = popDict[p2]["fitness"] + tempFitness_p2

				popDict[p1]["dumb"]            = False
				popDict[p1]["successfulMoves"] = 0
				popDict[p1]["failedThoughts"]  = 0

				popDict[p2]["dumb"]            = False
				popDict[p2]["successfulMoves"] = 0
				popDict[p2]["failedThoughts"]  = 0

				print("Grading:")
				print("{0} fitness so far: {1}".format(popDict[p1]["obj"].name, popDict[p1]["fitness"]))
				print("{0} fitness so far: {1}".format(popDict[p2]["obj"].name, popDict[p2]["fitness"]))

	# all games are played
	print("------------")
	print("Fitness of G-Blue-0." + str(genCount))
	old_pop = []
	for i in range(len(popDict)):
		print(popDict[i]["obj"].name + ": " + str(popDict[i]["fitness"]))
		popDict[i]["obj"].fitness = popDict[i]["fitness"]
		popDict[i]["fitness"] = 0
		old_pop.append(popDict[i]["obj"])
	#next i

	new_pop = g.breed(old_pop)

	for i in range(len(popDict)):
		popDict[i]["obj"] = new_pop[i]
	#next i
	print("------------")
