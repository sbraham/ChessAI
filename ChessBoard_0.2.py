############################
# Chess Board ~ v0.2 ~ SAB #
############################

import random as r
import chess  as pychess
from tkinter import * 

### Create tkinter window ###
Board_INF = Tk()

### Variable definition ###
btnLogQueue = ["Temp-Log"]
mveLogQueue = ["Temp-Log"]

tiles = []

board = pychess.Board()

WHITE_ALG = "RAND"
BLACK_ALG = "RAND"

pieces_legal_moves = []

promoting = {"Bool": False, "Move": None}

# Def images
blackBishop = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\blackBishop.png")
blackKing   = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\blackKing.png")
blackKnight = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\blackKnight.png")
blackPawn   = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\blackPawn.png")
blackQueen  = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\blackQueen.png")
blackRook   = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\blackRook.png")
whiteBishop = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\whiteBishop.png")
whiteKing   = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\whiteKing.png")
whiteKnight = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\whiteKnight.png")
whitePawn   = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\whitePawn.png")
whiteQueen  = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\whiteQueen.png")
whiteRook   = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\whiteRook.png")
error       = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\error.png")
blank       = PhotoImage(file = r"C:\Users\Sam.Braham\Documents\Code\Chess\Sprites\blank.png")

### Classes ###

#class for a square on the board
class Square(object):
	def __init__(self, square, x, y, btn):
		#Position on board; pychess.square = int
		self.square = square
		#Position in window; rid(column = x, row = (9-y))
		self.x     = x
		self.y     = y

		#What is on me; {'color': pychess.Color, 'piece': pychess.PieceType}
		self.contents = None

		#If a selected piece can move here, what would that move be
		self.potentialMove = None

		#The button the user will user to interact with the board
		self.btn = Button(
				### master ###
				board_framge,
				### widget look ###
				bg = "deep pink",
				height = 50,
				width = 50,
				bd = 2,
				relief = "solid",
				### on press ###
				command = lambda: TILE_BUTTON_FUNCTION(tiles[self.square]),
				activebackground = "brown",
				### other ###
				image = error
			)

		#Change some button parts to create that hex pattern
		if   btn == "btn1": 
			self.btn.configure(bg = "orange1")
		elif btn == "btn2": 
			self.btn.configure(bg = "orange4")
		else:
			# if button is set up wrong it will be clear
			self.btn.configure(bg = "red")

		if self.square > 63 or self.x > 8 or self.y > 8 or btn not in ("btn1", "btn2"):
			# if button is set up wrong it will be clear
			self.btn.configure(bg = "red")

	def log(self):
		Log(pychess.square_name(self.square))

### FUNCTIONS ###

#Reset the board to initial position
def _reset():
	promotionReset()
	board.reset()
	mveLogQueue.clear
	MveLog("Moves - New:")
	_cleanBoard()
	_updateBoard()

#Update all tile images on the board so pieces are represented in the right place
def _updateBoard():
	print(board)
	for i in tiles:
		square = i.square
		try:
			i.contents = board.piece_map()[square]
		except:
			i.contents = None

		if i.contents == None:
			i.btn.config(image = blank)
		elif i.contents.piece_type == 1 and i.contents.color == False:
			i.btn.config(image = blackPawn)
		elif i.contents.piece_type == 1 and i.contents.color == True:
			i.btn.config(image = whitePawn)
		elif i.contents.piece_type == 2 and i.contents.color == False:
			i.btn.config(image = blackKnight)
		elif i.contents.piece_type == 2 and i.contents.color == True:
			i.btn.config(image = whiteKnight)
		elif i.contents.piece_type == 3 and i.contents.color == False:
			i.btn.config(image = blackBishop)
		elif i.contents.piece_type == 3 and i.contents.color == True:
			i.btn.config(image = whiteBishop)
		elif i.contents.piece_type == 4 and i.contents.color == False:
			i.btn.config(image = blackRook)
		elif i.contents.piece_type == 4 and i.contents.color == True:
			i.btn.config(image = whiteRook)
		elif i.contents.piece_type == 5 and i.contents.color == False:
			i.btn.config(image = blackQueen)
		elif i.contents.piece_type == 5 and i.contents.color == True:
			i.btn.config(image = whiteQueen)
		elif i.contents.piece_type == 6 and i.contents.color == False:
			i.btn.config(image = blackKing)
			if board.is_check() and board.turn == i.contents.color:
				i.btn.config(bg = 'red')
		elif i.contents.piece_type == 6 and i.contents.color == True:
			i.btn.config(image = whiteKing)
			if board.is_check() and board.turn == i.contents.color:
				i.btn.config(bg = 'red')

		i.btn.grid(column = i.x, row = (9-i.y))

#Do a random move
def randMove():
	moveSet = []
	for i in board.legal_moves:
		moveSet.append(i)
	if moveSet == []:
		if board.is_checkmate():
			if board.turn is True:
				Log("BLACK WINS")
				reset = True
				return
			else:
				Log("WHITE WINS")
				reset = True
				return
		if board.is_stalemate():
			Log("STALEMATE")
			return
		#if other chess rules:
			#Log("WHY")
	move = r.choice(moveSet)
	if board.turn == True:
		MveLog("WHITE: " + str(move))
	else:
		MveLog("BLACK: " + str(move))

	if move.promotion != None:
		move.promotion = r.choice([2, 3, 4, 5])

	board.push(move)
	_updateBoard()

#Function to log events in the window
def Log(btnTextInpt):
	textInpt = str(btnTextInpt)

	print(btnTextInpt)

	btnLogQueue.append(btnTextInpt)
	if len(btnLogQueue) > 26:
		btnLogQueue.pop(0)
	else: pass

	bigLog = "Log:"
	for i in btnLogQueue:
		if i != "Temp-Log":
			bigLog = bigLog + "\n" + i
	BtnLog_lbl.config(text = bigLog)
	return btnLogQueue

#Function to log moves in the window
def MveLog(mveTextInput):
	print(mveTextInput)

	mveLogQueue.append(mveTextInput)
	if len(mveLogQueue) > 26:
		mveLogQueue.pop(0)
	else: pass

	bigLog = "Moves:"
	for i in mveLogQueue:
		if i != "Temp-Log":
			bigLog = bigLog + "\n" + i
	MveLog_lbl.config(text = bigLog)
	return mveLogQueue

def _cleanBoard():
	for i in [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]:
		tiles[i].btn.configure(bg = "orange1")
	for i in [0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63]:
		tiles[i].btn.configure(bg = "orange4")

#This program runs when a Tile Button is pressed
def TILE_BUTTON_FUNCTION(self):
	ListOfGlobals = globals()

	if pieces_legal_moves == [] or (self.contents != None and self.contents.color == board.turn):
		pieces_legal_moves.clear()
		if self.contents == None:
			Log("-" + pychess.square_name(self.square) + " pressed")
			return
		elif self.contents.color != board.turn:
			if self.contents.color == True:
				Log("BLACKS TURN")
			else:
				Log("WHITES TURN")
			return

		elif ListOfGlobals['promoting']["Bool"] == True:
			Log("PROMOTING")

		else:
			Log(str(self.contents) + pychess.square_name(self.square) + " pressed")
			_cleanBoard()
			for move in board.legal_moves:
				if move.from_square == self.square:
					self.btn.configure(bg = "green4")
					if board.is_en_passant(move) or board.is_castling(move) or move.promotion != None:
						tiles[move.to_square].btn.configure(bg = "cyan")
					else:
						tiles[move.to_square].btn.configure(bg = "pale green")
					pieces_legal_moves.append(move)
				if pieces_legal_moves == []:
					if board.is_checkmate():
						if board.turn is True:
							Log("BLACK WINS")
							reset = True
						else:
							Log("WHITE WINS")
							reset = True
					if board.is_stalemate():
						Log("STALEMATE")
					#if other chess rules:
						#Log("WHY")


	elif pieces_legal_moves != []:
		if promoting["Bool"] == True:
			Log("PROMOTING")
		else:
			moved = False
			for move in pieces_legal_moves:
				if self.square == move.to_square:
					if move.promotion != None:
						promotion(move)
					else:
						if board.turn == True:
							MveLog("WHITE: " + str(move))
						else:
							MveLog("BLACK: " + str(move))
						board.push(move)
						_cleanBoard()
					moved = True
					break
				else: pass

			if moved == False:
				Log("-" + pychess.square_name(self.square) + " pressed")
				Log("Not a legal move")

			pieces_legal_moves.clear()

	_updateBoard()

def promotion(move):
	ListOfGlobals = globals()

	piece = tiles[move.from_square].contents
	if piece.color == True:
		promotionToQueen_btn.configure(bg = "cyan4", image = whiteQueen)
		promotionToKnight_btn.configure(bg = "cyan4", image = whiteKing)
		promotionToRook_btn.configure(bg = "cyan4", image = whiteRook)
		promotionToBishop_btn.configure(bg = "cyan4", image = whiteBishop)
	else:
		promotionToQueen_btn.configure(bg = "cyan4", image = blackQueen)
		promotionToKnight_btn.configure(bg = "cyan4", image = blackKing)
		promotionToRook_btn.configure(bg = "cyan4", image = blackRook)
		promotionToBishop_btn.configure(bg = "cyan4", image = blackBishop)

	_cleanBoard()
	tiles[move.to_square].btn.configure(bg = "cyan4")

	ListOfGlobals['promoting'] = {"Bool": True, "Move": move}

def promotionReset():
	ListOfGlobals = globals()
	ListOfGlobals['promoting'] = {"Bool": False, "Move": None}
	promotionToQueen_btn.configure(bg = "gray", image = blank)
	promotionToKnight_btn.configure(bg = "gray", image = blank)
	promotionToRook_btn.configure(bg = "gray", image = blank)
	promotionToBishop_btn.configure(bg = "gray", image = blank)

def promotionToQueen():
	ListOfGlobals = globals()

	if ListOfGlobals['promoting']["Bool"] == True:
		move = ListOfGlobals['promoting']["Move"]
		move.promotion = 5
		if board.turn == True:
			MveLog("WHITE: " + str(move))
		else:
			MveLog("BLACK: " + str(move))
		board.push(move)
		_cleanBoard()
		_updateBoard()
		promotionReset()
	else:
		Log("NOT PROMOTING")

def promotionToKnight():
	ListOfGlobals = globals()

	if ListOfGlobals['promoting']["Bool"] == True:
		move = ListOfGlobals['promoting']["Move"]
		move.promotion = 2
		if board.turn == True:
			MveLog("WHITE: " + str(move))
		else:
			MveLog("BLACK: " + str(move))
		board.push(move)
		_cleanBoard()
		_updateBoard()
		promotionReset()
	else:
		Log("NOT PROMOTING")

def promotionToRook():
	ListOfGlobals = globals()

	if ListOfGlobals['promoting']["Bool"] == True:
		move = ListOfGlobals['promoting']["Move"]
		move.promotion = 4
		if board.turn == True:
			MveLog("WHITE: " + str(move))
		else:
			MveLog("BLACK: " + str(move))
		board.push(move)
		_cleanBoard()
		_updateBoard()
		promotionReset()
	else:
		Log("NOT PROMOTING")

def promotionToBishop():
	ListOfGlobals = globals()

	if ListOfGlobals['promoting']["Bool"] == True:
		move = ListOfGlobals['promoting']["Move"]
		move.promotion = 3
		if board.turn == True:
			MveLog("WHITE: " + str(move))
		else:
			MveLog("BLACK: " + str(move))
		board.push(move)
		_cleanBoard()
		_updateBoard()
		promotionReset()
	else:
		Log("NOT PROMOTING")

def _MovablePieces():
	_cleanBoard()
	for i in board.legal_moves:
		tiles[i.from_square].btn.configure(bg = "green4")
	pieces_legal_moves = []

def _DoAutoTurn():
	_cleanBoard()
	if board.turn == True:
		if WHITE_ALG == "HUMAN":
			Log("Waiting for Tile Press")
		elif WHITE_ALG == "RAND":
			randMove()
		elif WHITE_ALG == "GILG-BLUE":
			pass
		else:
			Log("Unknown algorithm for this user - " + str(WHITE_ALG))
	elif board.turn == False:
		if BLACK_ALG == "HUMAN":
			Log("Waiting for \nTile Press")
		elif BLACK_ALG == "RAND":
			randMove()
		elif BLACK_ALG == "GILG-BLUE":
			pass
		else:
			Log("Unknown algorithm for this user - " + str(WHITE_ALG))

def _StartLearningLoop():
	for i in range(1):
		_reset()
		win = False
		count = 0
		while win == False:
			count += 1
			_DoAutoTurn()
			if count > 300:
				win = True
		

### Set Tkinter Window ###
Board_INF.title("Chess")
Board_INF.geometry('860x500')

log_frame = Frame(Board_INF, width=200, height=455, bg='white', bd = 2, relief = "solid")
log_frame.grid(row=0, column=0, padx=5, pady=5)

board_framge = Frame(Board_INF, width=200, height= 455, bg='white', bd = 2, relief = "solid")
board_framge.grid(row=0, column=1, padx=5, pady=5)

control_frame = Frame(Board_INF, width=100, height= 455)
control_frame.grid(row=0, column=2, padx=5, pady=5)

### Log Frame ###
BtnLog_lbl = Label(log_frame, bg = "white", height = 28, width = 15, bd = 2, relief = "solid", text = "Log:", font=("Courier", 10), anchor = "nw", justify = "left")
BtnLog_lbl.grid(row=0, column=0)

MveLog_lbl = Label(log_frame, bg = "white", height = 28, width = 15, bd = 2, relief = "solid", text = "Moves:", font=("Courier", 10), anchor = "nw", justify = "left")
MveLog_lbl.grid(row=0, column=1)

### Board Frame ###
count = 0
Xcount = 1
Ycount = 1
while count < 64:
	#print("count: " + str(count))
	#print("X: "     + str(Xcount))
	#print("Y: "     + str(Ycount))

	if count in [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]:
		tiles.append(Square(count, Xcount, Ycount, "btn1"))
	if count in [0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63]:
		tiles.append(Square(count, Xcount, Ycount, "btn2"))

	Xcount += 1
	if Xcount > 8:
		Xcount = 1
		Ycount += 1

	count += 1

### Controle Frame ###
promotion_frame = Frame(control_frame, width=100, height= 100, bd = 2, relief = "solid")
promotion_frame.pack(pady=5)

MovablePieces = Button(control_frame, bg = "gray", text=("Movable\npieces?"), font=("TkDefaultFont", 10), height = 2, width = 10, command = _MovablePieces, activebackground = "gray30")
MovablePieces.pack(pady=5)

MovablePieces = Button(control_frame, bg = "gray", text=("Movable\npieces?"), font=("TkDefaultFont", 10), height = 2, width = 10, command = _MovablePieces, activebackground = "gray30")
MovablePieces.pack(pady=5)

AIsPick = Button(control_frame, bg = "gray", text=("AIs Pick"), font=("TkDefaultFont", 10), height = 2, width = 10, command = print, activebackground = "gray30")
AIsPick.pack(pady=5)

DoAutoTurn = Button(control_frame, bg = "gray", text=("Do Auto Turn"), font=("TkDefaultFont", 10), height = 2, width = 10, command = _DoAutoTurn, activebackground = "gray30")
DoAutoTurn.pack(pady=5)

StartLearningLoop = Button(control_frame, bg = "gray", text=("Start Learning\nLoop"), font=("TkDefaultFont", 10), height = 2, width = 10, command= _StartLearningLoop, activebackground = "gray30")
StartLearningLoop.pack(pady=5)

Reset = Button(control_frame, bg = "gray", text=("Reset"), font=("TkDefaultFont", 10), height = 2, width = 10, command = _reset, activebackground = "gray30")
Reset.pack(pady=5)

### Promotion Frame ###
promotionToQueen_btn  = Button(promotion_frame, bg = "gray", height = 50, width = 50, bd = 2, relief = "solid", command = promotionToQueen , activebackground = "brown", image = blank)
promotionToQueen_btn.grid(row=0 , column=0)

promotionToKnight_btn = Button(promotion_frame, bg = "gray", height = 50, width = 50, bd = 2, relief = "solid", command = promotionToKnight, activebackground = "brown", image = blank)
promotionToKnight_btn.grid(row=1 , column=0)

promotionToRook_btn   = Button(promotion_frame, bg = "gray", height = 50, width = 50, bd = 2, relief = "solid", command = promotionToRook  , activebackground = "brown", image = blank)
promotionToRook_btn.grid(row=0 , column=1)

promotionToBishop_btn = Button(promotion_frame, bg = "gray", height = 50, width = 50, bd = 2, relief = "solid", command = promotionToBishop, activebackground = "brown", image = blank)
promotionToBishop_btn.grid(row=1 , column=1)

### Built Window ###
_updateBoard()

Board_INF.mainloop()