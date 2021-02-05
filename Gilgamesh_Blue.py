import numpy as np
import random as r
import matplotlib.pyplot as plt
import chess  as pychess
import sab

allPawns_fen     = 'pppppppp/pppppppp/pppppppp/pppppppp/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP w - - 0 1'
oddOnesOut_fen   = 'pppppppp/pppppQpp/pppppppp/pppppppp/PPPPPPPP/PKPPPPPP/PPPPPPPP/PPPPPPPP w - - 0 1'
wowSuchEmpty_fen = '8/8/8/8/8/8/8/8 w - - 0 1'
stripyBoi_fen    = '8/pppppppp/8/PPPPPPPP/8/pppppppp/8/PPPPPPPP w - - 0 1'
realStartFen_fen = pychess.STARTING_FEN

board = pychess.Board()
board.set_fen(realStartFen_fen)

#print(board.piece_map())

class Gilgamesh_Gold(object):
	pass

class Gilgamesh_Blue(object):
	def __init__(self, name, runNum, genCount, popNum):
		self.name = name
	
		self.brainType = "G-Blue"
		self.runNum   = runNum
		self.genCount = genCount
		self.popNum   = popNum
		self.brain = [
			NN(385, 64, 3, [100, 100, 100]),
			NN(385, 64, 3, [100, 100, 100]),
			NN(385, 4 , 3, [100, 100, 100])
		]

		self.fitness = 0

	def pickPiece(self):
		boardImage = readBoard(board)
		possiblePieceArr = self.brain[0].propagate(boardImage)
		possiblePiece = []
		for i in range(65):
			if i != 0:
				possiblePiece.append(possiblePieceArr[i])
			else: pass

		return possiblePiece.index(max(possiblePiece))

	def makeMove(self):
		boardImage = readBoard(board)
		possibleMovesArr = self.brain[1].propagate(boardImage)
		possibleMoves = []
		for i in range(65):
			if i != 0:
				possibleMoves.append(possibleMovesArr[i])
			else: pass

		return possibleMoves.index(max(possibleMoves))

	def promotion(self):
		boardImage = readBoard(board)
		possiblePromotionArr = self.brain[2].propagate(boardImage)
		possiblePromotion = []
		for i in range(5):
			if i != 0:
				possiblePromotion.append(possiblePromotionArr[i])
			else: pass

		print(possiblePromotion)
		return 2+possiblePromotion.index(max(possiblePromotion))

	def gradeFitness(self, win, endType, successfulMoves, failedThoughts):
		fitness = 0

		if successfulMoves != 0:
			if endType != "dumb":
				if win == True:
					fitness += 200
				elif win == False:
					fitness -= 200
				else:
					if endType == "stalemate-ed":
						fitness += 50
					elif endType == "stalemate-er":
						fitness -= 50
					else:
						fitness -= 100

			if successfulMoves <= 100:
				fitness += successfulMoves
			else: pass
		else:
			failedThoughts = 25

		fitness -= (2*failedThoughts)
		

		return fitness

class Gilgamesh_Life(object):
	pass

class NN(object):
	# Creation of NN requires 
	# inputUnitNum       = Number of units in input layer
	# outputUnitNum      = Number of units in output layer
	# hiddenLayerNum = Number of hidden layers
	# hiddenUnitNum  = A list of number when the Nth item in the list is the number of units in the Nth hidden layer
	
	def __init__(self, inputUnitNum, outputUnitNum, hiddenLayerNum, hiddenUnitNum):
		# Creating the activation array
		# a is a list of lists/vecters of the neuron activations (level of activation; number between -1 and 1, 0 is no activation)
		# the activation the ith neuron in the jth layer can be found at a[j][i]
		# a[j] is a vector of activations in layer j
		# input and hidden layers also have 1 offset neuron that is always +1 - (controls the significants of 0) - is always neuron 0

		self.inputUnitNum   = inputUnitNum
		self.outputUnitNum  = outputUnitNum
		self.hiddenLayerNum = hiddenLayerNum
		self.hiddenUnitNum  = hiddenUnitNum
		self.outputLayerJ   = 0 + hiddenLayerNum + 1

		if hiddenLayerNum != len(hiddenUnitNum):
			print("Error:")
			print(" number of hidden layers not equal to number of hidden units given")
			print(" difference: " + str(len(hiddenUnitNum)) - len(hiddenLayerNum))

		else:
			self.a = []

			inputLayerList_activ = []
			inputLayerList_activ.append(1)
			for i in range(inputUnitNum):
				inputLayerList_activ.append(0)
			#next i
			inputLayerArr_activ  = inputLayerList_activ

			outputLayerList_activ = []
			outputLayerList_activ.append(1)
			for i in range(outputUnitNum):
				outputLayerList_activ.append(0)
			#next i
			outputLayerArr_activ  = outputLayerList_activ

			hiddenLayersFullList_activ = []
			for j in range(hiddenLayerNum):
				#print(hiddenUnitNum[j])
				hiddenLayerList_activ = []
				hiddenLayerList_activ.append(1)
				for i in range(hiddenUnitNum[j]):
					#print(i)
					hiddenLayerList_activ.append(0)
				#next i
				hiddenLayersFullList_activ.append(hiddenLayerList_activ)
			#next j
			hiddenLayersArr_activ  = hiddenLayersFullList_activ

			#print(inputLayerArr_activ)
			#print(hiddenLayersArr_activ)
			#print(outputLayerArr_activ)

			self.a.append(inputLayerArr_activ)
			for j in range(hiddenLayerNum):
				self.a.append(hiddenLayersArr_activ[j])
			self.a.append(outputLayerArr_activ)

			#print(self.a)

			# Creating weight arrays
			# ϴ is a matrix of weights
			# a[layer2][unit1] = ϴ[layer1][to unit 1][from unit 0] * a[layer1][unit0] +  ϴ[layer1][to unit 1][from unit 1] * a[layer1][unit1] + ... ϴ[layer1][to unit 1][from unit UnitNum] * a[layer1][unit UnitNum]
			# weight for the connection from unit i₁ in layer j to i₂ in layer j+1 is ϴ[j][i₂][i₁]
			# ϴ[j] is a matrix of waights for layer j

			self.ϴ = []

			for j in range(1 + hiddenLayerNum):
				toUnitList_theta = []
				for i1 in range(len(self.a[j])):
					fromUnitList_theta = []
					for i2 in range(len(self.a[j+1])):
						fromUnitList_theta.append(r.uniform(-1, 1))
					#next i₂
					toUnitList_theta.append(fromUnitList_theta)
				#next i₁
				self.ϴ.append(toUnitList_theta)
			#next j

			#print("")
			#print(self.ϴ)
			#print("")
			#print(self.ϴ[0])
			#print(self.ϴ[0].shape)
			#print(self.ϴ[0].ndim)

	def propagate(self, inputList):
		if len(inputList) != (len(self.a[0]) - 1):
			print("Error:")
			print(" not enough/to many inputs")
			print(" difference: " + str(len(self.a[0]) - len(inputList)))

		else:
			#print(inputList)

			for i in range(len(inputList)):
				#print(i)
				
				#print(str(inputList[i]) + " -> " + str(sab.σ(inputList[i])))
				normalisedInput = sab.σ(inputList[i])
				#print("normalisedInput " + str(normalisedInput))
				#print(self.a[0][i])
				self.a[0][i+1] = normalisedInput
				#print(self.a[0][i])
				
				self.a[0][0] = 1
			#next i

			#print(self.a[0])
			#print()

			for j in range(len(self.a)-1):
				j = j+1
				self.a[j] = np.dot(np.array(self.a[j-1]), np.array(self.ϴ[j-1]))
				for i in range(len(self.a[j])):
					#print(str(self.a[j][i]) + " -> " + str(sab.σ(self.a[j][i])))
					self.a[j][i] = sab.σ(self.a[j][i])
				self.a[j][0] = 1

			#print(self.a[0])
			#print()

			#for j in range(self.hiddenLayerNum):
			#	print(self.a[j+1])
			#	print()

			#print(self.a[self.outputLayerJ])
			return self.a[self.outputLayerJ]

	def breed():
		pass

def readBoard(board):
	# 1 turn  neurons = 1 if white turn, -1 if black turn
	# 64 fields each with 6 piece neurons (1 for white, -1 for black and 0 for empty)
	# all within the list boardImage - len(boardImage) = 388

	pieceMap = board.piece_map()
	boardImage = []

	if board.turn == True:
		boardImage.append(1)
	else:
		boardImage.append(-1)

	for i in range(64):
		if sab.valueInGroup(i, pieceMap):
			piece = pieceMap[i].symbol()
			#print(piece)

			for i in ['P', 'N', 'B', 'R', 'Q', 'K']:
				if   piece == i.upper():
					boardImage.append(1)
				elif piece == i.lower():
					boardImage.append(-1)
				else:
					boardImage.append(0)
		else:
			for i in [1, 2, 3, 4, 5, 6]:
				boardImage.append(0)

	return boardImage

def crossover(a, b):
	if isinstance(a, Gilgamesh_Gold):
		print("Error:")
		print(" Gilgamesh Gold still in development")

		new_a = a
		new_b = b

	elif isinstance(a, Gilgamesh_Blue):
		new_a = Gilgamesh_Blue("G-Blue - Crossover", a.runNum, a.genCount, a.popNum)
		new_b = Gilgamesh_Blue("G-Blue - Crossover", b.runNum, b.genCount, b.popNum)
		
	elif isinstance(a, Gilgamesh_Life):
		print("Error:")
		print(" Gilgamesh Gold still in development")

		new_a = a
		new_b = b

	else:
		print("Error:")
		print(" Unknown crossover object")

		return a, b

	for i in range(len(a.brain)):
		randCutPoint = r.randint(0, len(a.brain[i].ϴ))

		new_aϴCut1 = a.brain[i].ϴ[:randCutPoint]
		new_aϴCut2 = a.brain[i].ϴ[randCutPoint:]

		new_bϴCut1 = a.brain[i].ϴ[:randCutPoint]
		new_bϴCut2 = a.brain[i].ϴ[randCutPoint:]

		new_aϴ = new_aϴCut1 + new_bϴCut2
		new_bϴ = new_bϴCut1 + new_aϴCut2

		new_a.brain[i].ϴ = new_aϴ
		new_b.brain[i].ϴ = new_bϴ
	#next i

	return new_a, new_b

def mutate(member, probability):
	new_member = member

	for NN in range(len(member.brain)):
		for j in range(len(member.brain[NN].ϴ)):
			for from_unit in range(len(member.brain[NN].ϴ[j])):
				for to_unit in range(len(member.brain[NN].ϴ[j][from_unit])):
					if r.random() <= probability:
						new_member.brain[NN].ϴ[j][from_unit][to_unit] = r.uniform(-1, 1)
	#next i

	return new_member

def create_first_generation(genSize, brainType, runNum):
	Gen1 = []
	genCount = 1

	if genSize % 10 != 0: 
		print("Error:")
		print(" genSize must be multilple of 10")

	elif brainType == "G-Gold":
		print("Error:")
		print(" Gilgamesh Gold still in development")

	elif brainType == "G-Blue":
		for i in range(genSize):
			i = i + 1
			Gen1.append(Gilgamesh_Blue(brainType + "-" + str(runNum) + "." + str(genCount) + "." + str(i), runNum, genCount, i))

	elif brainType == "G-Life":
		print("Error:")
		print(" Gilgamesh Life is still in development")

	else:
		print("Error:")
		print(" " + str(brainType) + " is not a valid brainType")

	return Gen1

def popSortFunc(e):
	try:
		return e.fitness
	except:
		print("Error:")
		print(" e is not a Gilgamesh Object")

def breed(population):
	genCount = population[0].genCount

	genSize = len(population)
	tenth   = int(genSize/10)

	print("Breeding: " + population[0].brainType + "-" + str(population[0].runNum) + "." + str(population[0].genCount))

	population.sort(reverse=True, key = popSortFunc)

	#print("population")
	#print(population)

	#for i in population:
	#	print(i.fitness)

	#gen1st10th = population[:tenth]
	#print("")

	#for i in gen1st10th:
	#	print(i.fitness)

	gen1st10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 1)):
		gen1st10th.remove(r.choice(gen1st10th))

	gen2nd10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 2)):
		gen2nd10th.remove(r.choice(gen2nd10th))

	gen3rd10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 3)):
		gen3rd10th.remove(r.choice(gen3rd10th))

	gen4th10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 4)):
		gen4th10th.remove(r.choice(gen4th10th))

	gen5th10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 5)):
		gen5th10th.remove(r.choice(gen5th10th))

	gen6th10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 6)):
		gen6th10th.remove(r.choice(gen6th10th))

	gen7th10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 7)):
		gen7th10th.remove(r.choice(gen7th10th))

	gen8th10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 8)):
		gen8th10th.remove(r.choice(gen8th10th))

	gen9th10th = population[:tenth]
	population = population[tenth:]
	for i in range(int(tenth/10 * 9)):
		gen9th10th.remove(r.choice(gen9th10th))

	breading_pool = gen1st10th + gen1st10th + gen2nd10th + gen3rd10th + gen4th10th + gen5th10th + gen6th10th + gen7th10th + gen8th10th + gen9th10th + [r.choice(population)]

	#print("")
	#print("Breading pool")
	#print(breading_pool)

	#print(len(breading_pool))

	new_pop = []
	for i in range(int(50 * tenth/10)):
		#print("i: " + str(i))
		parent_a = r.choice(breading_pool)
		breading_pool.remove(parent_a)
		#print(len(breading_pool))
		parent_b = r.choice(breading_pool)
		#print(len(breading_pool))
		child_a, child_b = crossover(parent_a, parent_b)
		new_pop.append(child_a)
		new_pop.append(child_b)

	#print(len(new_pop))

	for i in range(len(new_pop)):
		new_pop[i] = mutate(new_pop[i], 0.05)

	for i in range(len(new_pop)):
		new_pop[i].genCount = genCount + 1
		new_pop[i].popNum   = i + 1

		new_pop[i].name = new_pop[i].brainType + "-" + str(new_pop[i].runNum) + "." + str(new_pop[i].genCount) + "." + str(new_pop[i].popNum)

	return new_pop

if False:
	#print(readBoard(board, 1))

	#NN = NN(385, 64, 5, [5, 5, 5, 5, 5])

	#print(NN.propagate(readBoard(board, 1)))

	#GB = Gilgamesh_Blue("G1")

	'''
	listOfStrings = []
	for i in range(64):
		listOfStrings.append(str(i))

	pickCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in range(50000):
		print(i)
		G1 = Gilgamesh_Blue("G1")
		pick = G1.pickPiece()
		if pick <= 63 and pick >= 0:
			pickCount[pick] += 1
		else: 
			print("1: " + str(pick))
	#next i
	print("1: " + str(pickCount))
	plt.bar(listOfStrings, pickCount)
	plt.show()

	pickCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in range(50000):
		print(i)
		G1 = Gilgamesh_Blue("G1")
		pick = G1.makeMove()
		if pick <= 63 and pick >= 0:
			pickCount[pick] += 1
		else:
			print("2: " + str(pick))
	#next i
	print("2: " + str(pickCount))
	plt.bar(listOfStrings, pickCount)
	plt.show()

	pickCount = [0, 0, 0, 0, 0, 0, 0] 
	for i in range(50000):
		print(i)
		G1 = Gilgamesh_Blue("G1")
		pick = G1.promotion()
		print(pick)
		if pick <= 5 and pick >= 2:
			pickCount[pick] += 1
		else:
			print("3: " + str(pick))
	#next i
	print("3: " + str(pickCount))
	plt.bar(["0", "1", "2", "3", "4", "5", "6"], pickCount)
	plt.show()
	'''

	#print(G1.pickPiece())
	#print(G1.makeMove() )
	#print(G1.promotion())

	#a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	#b = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

	#print(crossover(a, b))


	#print(GB.brain[2].ϴ[2][2][2])
	#GB = mutate(GB, 0.5)

	#print(GB.brain[2].ϴ[2][2][2])

	#population = create_first_generation(10, "G-Blue", 0)

	#for i in population:
	#	print(i.name)

	#population = create_first_generation(100, "G-Blue", 0)

	#for i in population:
	#	print(i.name)

	#print(population[1].name)

	#print("")
	#population = breed(population)
	#print("")

	#for i in population:
	#	print(i.name)

	#print(population[1].name)

	#GB = Gilgamesh_Blue("Gilg-Blue-Test", 0, 0, 1)

	#for i in range(100):
	#	print(GB.pickPiece())