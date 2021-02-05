############################
# Chess Board ~ v0.1 ~ SAB #
############################

import random as r
import chess  as pychess
from tkinter import * 

Board_INF = Tk()

Board_INF.title("Chess")
Board_INF.geometry('840x500')

control_frame = Frame(Board_INF, width=100, height= 455)
control_frame.grid(row=0, column=0, padx=5, pady=5)

board_framge = Frame(Board_INF, width=200, height= 455, bg='white', bd = 2, relief = "solid")
board_framge.grid(row=0, column=1, padx=5, pady=5)
 
log_frame = Frame(Board_INF, width=200, height=455, bg='white', bd = 2, relief = "solid")
log_frame.grid(row=0, column=2, padx=5, pady=5)

#Control buttons
if True:
	DoAutoTurn = Button(control_frame,
				bg = "gray",
				text=("Do Auto Turn"),
				font=("TkDefaultFont", 10),
				height = 2,
				width = 10,
				command= lambda: TILE_BUTTON_FUNCTION(tiles[self.square]),
				activebackground = "orange4")
	DoAutoTurn.pack(pady=10)
	StartLearningLoop = Button(control_frame,
				bg = "gray",
				text=("Start Learning\nLoop"),
				font=("TkDefaultFont", 10),
				height = 2,
				width = 10,
				command= lambda: board.reset(),
				activebackground = "orange4")
	StartLearningLoop.pack(pady=10)
	PickDifferent = Button(control_frame,
				bg = "gray",
				text=("Pick Different"),
				font=("TkDefaultFont", 10),
				height = 2,
				width = 10,
				command= lambda: TILE_BUTTON_FUNCTION(tiles[self.square]),
				activebackground = "orange4")
	PickDifferent.pack(pady=10)
	Reset = Button(control_frame,
				bg = "gray",
				text=("Reset"),
				font=("TkDefaultFont", 10),
				height = 2,
				width = 10,
				command= lambda: _reset(),
				activebackground = "orange4")
	Reset.pack(pady=10)

def _reset():
	board.reset()
	_updateBoard()
	print(board)

#BUTTON LOG
if True:
	BtnLog_lbl = Label(
		# master
		log_frame,
		# widget look
		bg = "white",
		height = 28,
		width = 15,
		bd = 2,
		relief = "solid",
		# text
		text = "Log:",
		font=("Courier", 10),
		anchor = "nw",
		justify = "left"
	)
	BtnLog_lbl.grid(row=0, column=0)

	btnLogQueue = ["Temp-Log"]
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

if True:
	MveLog_lbl = Label(
		# master
		log_frame,
		# widget look
		bg = "white",
		height = 28,
		width = 15,
		bd = 2,
		relief = "solid",
		# text
		text = "Moves:",
		font=("Courier", 10),
		anchor = "nw",
		justify = "left"
	)
	MveLog_lbl.grid(row=0, column=1)

	mveLogQueue = ["Temp-Log"]
	def MveLog(mveTextInput):
		mveTextInput = str(mveTextInput)

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

# def images
if True:
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

tiles = []

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

		if   btn == "btn1": 
			self.btn = Button(
				### master ###
				board_framge,
				### widget look ###
				bg = "orange1",
				height = 50,
				width = 50,
				bd = 2,
				relief = "solid",
				### on press ###
				command = lambda: TILE_BUTTON_FUNCTION(tiles[self.square]),
				activebackground = "red4",
				### other ###
				image = error
			)
		elif btn == "btn2": 
			self.btn = Button(
				### master ###
				board_framge,
				### widget look ###
				bg = "orange4",
				height = 50,
				width = 50,
				bd = 2,
				relief = "solid",
				### on press ###
				command = lambda: TILE_BUTTON_FUNCTION(tiles[self.square]),
				activebackground = "red4",
				### other ###
				image = error
			)
		else:
			self.btn = Button(
				### master ###
				board_framge,
				### widget look ###
				bg = "red",
				height = 50,
				width = 50,
				bd = 2,
				relief = "solid",
				### on press ###
				command = lambda: TILE_BUTTON_FUNCTION(tiles[self.square]),
				activebackground = "red4",
				### other ###
				image = whitePawn
			)

	def log(self):
		Log(pychess.square_name(self.square))

# def tiles
if True:
	A1 = Square( 0, 1, 1, "btn1")
	B1 = Square( 1, 2, 1, "btn2")
	C1 = Square( 2, 3, 1, "btn1")
	D1 = Square( 3, 4, 1, "btn2")
	E1 = Square( 4, 5, 1, "btn1")
	F1 = Square( 5, 6, 1, "btn2")
	G1 = Square( 6, 7, 1, "btn1")
	H1 = Square( 7, 8, 1, "btn2")
	A2 = Square( 8, 1, 2, "btn2")
	B2 = Square( 9, 2, 2, "btn1")
	C2 = Square(10, 3, 2, "btn2")
	D2 = Square(11, 4, 2, "btn1")
	E2 = Square(12, 5, 2, "btn2")
	F2 = Square(13, 6, 2, "btn1")
	G2 = Square(14, 7, 2, "btn2")
	H2 = Square(15, 8, 2, "btn1")
	A3 = Square(16, 1, 3, "btn1")
	B3 = Square(17, 2, 3, "btn2")
	C3 = Square(18, 3, 3, "btn1")
	D3 = Square(19, 4, 3, "btn2")
	E3 = Square(20, 5, 3, "btn1")
	F3 = Square(21, 6, 3, "btn2")
	G3 = Square(22, 7, 3, "btn1")
	H3 = Square(23, 8, 3, "btn2")
	A4 = Square(24, 1, 4, "btn2")
	B4 = Square(25, 2, 4, "btn1")
	C4 = Square(26, 3, 4, "btn2")
	D4 = Square(27, 4, 4, "btn1")
	E4 = Square(28, 5, 4, "btn2")
	F4 = Square(29, 6, 4, "btn1")
	G4 = Square(30, 7, 4, "btn2")
	H4 = Square(31, 8, 4, "btn1")
	A5 = Square(32, 1, 5, "btn1")
	B5 = Square(33, 2, 5, "btn2")
	C5 = Square(34, 3, 5, "btn1")
	D5 = Square(35, 4, 5, "btn2")
	E5 = Square(36, 5, 5, "btn1")
	F5 = Square(37, 6, 5, "btn2")
	G5 = Square(38, 7, 5, "btn1")
	H5 = Square(39, 8, 5, "btn2")
	A6 = Square(40, 1, 6, "btn2")
	B6 = Square(41, 2, 6, "btn1")
	C6 = Square(42, 3, 6, "btn2")
	D6 = Square(43, 4, 6, "btn1")
	E6 = Square(44, 5, 6, "btn2")
	F6 = Square(45, 6, 6, "btn1")
	G6 = Square(46, 7, 6, "btn2")
	H6 = Square(47, 8, 6, "btn1")
	A7 = Square(48, 1, 7, "btn1")
	B7 = Square(49, 2, 7, "btn2")
	C7 = Square(50, 3, 7, "btn1")
	D7 = Square(51, 4, 7, "btn2")
	E7 = Square(52, 5, 7, "btn1")
	F7 = Square(53, 6, 7, "btn2")
	G7 = Square(54, 7, 7, "btn1")
	H7 = Square(55, 8, 7, "btn2")
	A8 = Square(56, 1, 8, "btn2")
	B8 = Square(57, 2, 8, "btn1")
	C8 = Square(58, 3, 8, "btn2")
	D8 = Square(59, 4, 8, "btn1")
	E8 = Square(60, 5, 8, "btn2")
	F8 = Square(61, 6, 8, "btn1")
	G8 = Square(62, 7, 8, "btn2")
	H8 = Square(63, 8, 8, "btn1")

	tiles = [
		A1, B1, C1, D1, E1, F1, G1, H1,
		A2,	B2, C2, D2, E2, F2, G2, H2,
		A3,	B3, C3, D3, E3, F3, G3, H3,
		A4, B4, C4, D4, E4, F4, G4, H4,
		A5, B5, C5, D5, E5, F5, G5, H5,
		A6, B6, C6, D6, E6, F6, G6, H6,
		A7, B7, C7, D7, E7, F7, G7, H7,
		A8, B8, C8, D8, E8, F8, G8, H8
	]

	for i in tiles:
		i.btn.grid(column = i.x, row = (9-i.y))

board = pychess.Board()
print(board)

	# piece_map() → Dict[pychess.Square, pychess.Piece]
	# Gets a dictionary of pieces by square index.

	# set_piece_map(pieces: Mapping[pychess.Square, pychess.Piece]) → None
	# Sets up the board from a dictionary of pieces by square index.

	# set_piece_at(square: pychess.Square, piece: Optional[pychess.Piece], promoted: bool = False)
	# Sets a piece at the given square.
	# An existing piece is replaced. Setting piece to None is equivalent to remove_piece_at().

def _updateBoard():
	for i in tiles:
		square = i.square
		try:
			i.contents = board.piece_map()[square]
		except:
			i.contents = None

		if i.contents == None:
			i.btn['image'] = blank
		elif i.contents.piece_type == 1 and i.contents.color == False:
			i.btn['image'] = blackPawn
		elif i.contents.piece_type == 1 and i.contents.color == True:
			i.btn['image'] = whitePawn
		elif i.contents.piece_type == 2 and i.contents.color == False:
			i.btn['image'] = blackKnight
		elif i.contents.piece_type == 2 and i.contents.color == True:
			i.btn['image'] = whiteKnight
		elif i.contents.piece_type == 3 and i.contents.color == False:
			i.btn['image'] = blackBishop
		elif i.contents.piece_type == 3 and i.contents.color == True:
			i.btn['image'] = whiteBishop
		elif i.contents.piece_type == 4 and i.contents.color == False:
			i.btn['image'] = blackRook
		elif i.contents.piece_type == 4 and i.contents.color == True:
			i.btn['image'] = whiteRook
		elif i.contents.piece_type == 5 and i.contents.color == False:
			i.btn['image'] = blackQueen
		elif i.contents.piece_type == 5 and i.contents.color == True:
			i.btn['image'] = whiteQueen
		elif i.contents.piece_type == 6 and i.contents.color == False:
			i.btn['image'] = blackKing
		elif i.contents.piece_type == 6 and i.contents.color == True:
			i.btn['image'] = whiteKing

		i.btn.grid(column = i.x, row = (9-i.y))

def _updateTile(tile):
	square = tile.square
	try:
		tile.contents = board.piece_map()[square]
	except:
		tile.contents = None

	if tile.contents == None:
		tile.btn['image'] = blank
	elif tile.contents.piece_type == 1 and tile.contents.color == False:
		tile.btn['image'] = blackPawn
	elif tile.contents.piece_type == 1 and tile.contents.color == True:
		tile.btn['image'] = whitePawn
	elif tile.contents.piece_type == 2 and tile.contents.color == False:
		tile.btn['image'] = blackKnight
	elif tile.contents.piece_type == 2 and tile.contents.color == True:
		tile.btn['image'] = whiteKnight
	elif tile.contents.piece_type == 3 and tile.contents.color == False:
		tile.btn['image'] = blackBishop
	elif tile.contents.piece_type == 3 and tile.contents.color == True:
		tile.btn['image'] = whiteBishop
	elif tile.contents.piece_type == 4 and tile.contents.color == False:
		tile.btn['image'] = blackRook
	elif tile.contents.piece_type == 4 and tile.contents.color == True:
		tile.btn['image'] = whiteRook
	elif tile.contents.piece_type == 5 and tile.contents.color == False:
		tile.btn['image'] = blackQueen
	elif tile.contents.piece_type == 5 and tile.contents.color == True:
		tile.btn['image'] = whiteQueen
	elif tile.contents.piece_type == 6 and tile.contents.color == False:
		tile.btn['image'] = blackKing
	elif tile.contents.piece_type == 6 and tile.contents.color == True:
		tile.btn['image'] = whiteKing

	tile.btn.grid(column = tile.x, row = (9-tile.y))

pieces_legal_moves = []

def randMove():
	moveSet = []
	for i in board.legal_moves:
		moveSet.append(i)
	move = r.choice(moveSet)
	MveLog(move)
	board.push(move)

WHITE_ALG = 'RAND'
WHITE_ALG = 'HUMAN'

def TILE_BUTTON_FUNCTION(self):
	#if self.contents != None:
	#	Log(str(self.contents) + pychess.square_name(self.square) + " pressed")
	#else:
	#	Log(        "-"        + pychess.square_name(self.square) + " pressed")

	if pieces_legal_moves == []:
		if self.contents != None:
			Log(str(self.contents) + pychess.square_name(self.square) + " pressed")
			for i in board.legal_moves:
				if i.from_square == self.square:
					self.btn.configure(bg = "green4")
					tiles[i.to_square].btn.configure(bg = "pale green")
					pieces_legal_moves.append(i)
			if pieces_legal_moves == [] and board.turn == self.contents.color:
				Log("No legal move")
			if pieces_legal_moves == [] and board.turn != self.contents.color:
				if self.contents.color == True:
					Log("Not white's turn")
				else:
					Log("Not black's turn")
			Log("")
		else:
			Log(        "-"        + pychess.square_name(self.square) + " pressed")
			Log("")

	elif pieces_legal_moves != []:
		for i in pieces_legal_moves:
			if self.square == i.to_square:
				move = i
			else:
				pass

		MveLog(move)
		board.push(move)
		pieces_legal_moves.clear()

		for i in [0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63]:
			tiles[i].btn.configure(bg = "orange1")
		for i in [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]:
			tiles[i].btn.configure(bg = "orange4")

		randMove()

	_updateBoard()
	print(board)

_updateBoard()

Board_INF.mainloop()