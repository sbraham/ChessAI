############################
# Chess Board ~ v0.2 ~ SAB #
############################

import random as r
import chess  as pychess
from tkinter import * 

import Gilgamesh_Blue as g

### Create tkinter window ###
chess_TK = Tk()

#FEN
oneMoveCheck_fen = '7K/7R/7R/7R/7R/7R/6QR/k7 w - - 0 1'
oneMoveStale_fen = '1RRRRRRR/6KR/7R/7R/7R/6QR/8/k7 w - - 0 1'
realStartFen_fen = pychess.STARTING_FEN

colorPick_fen = '8/8/8/1KK2kk1/1KK2kk1/8/8/8 b - - 0 0'
startGame_fen = realStartFen_fen

# 0 = HUMAN
# 1 = RANDOME
# AIs
# 2 = GILGAMESH-BLUE-xxx
# 3 = GILGAMESH-BLUE-xxx
white = True
black = False

algorithem = {white: 1, black: 1}

Gilgamesh_Blue_Alpha_1 = None

# Def images
blackBishop = PhotoImage(file = r'Sprites\blackBishop.png')
blackKing   = PhotoImage(file = r'Sprites\blackKing.png')
blackKnight = PhotoImage(file = r'Sprites\blackKnight.png')
blackPawn   = PhotoImage(file = r'Sprites\blackPawn.png')
blackQueen  = PhotoImage(file = r'Sprites\blackQueen.png')
blackRook   = PhotoImage(file = r'Sprites\blackRook.png')
whiteBishop = PhotoImage(file = r'Sprites\whiteBishop.png')
whiteKing   = PhotoImage(file = r'Sprites\whiteKing.png')
whiteKnight = PhotoImage(file = r'Sprites\whiteKnight.png')
whitePawn   = PhotoImage(file = r'Sprites\whitePawn.png')
whiteQueen  = PhotoImage(file = r'Sprites\whiteQueen.png')
whiteRook   = PhotoImage(file = r'Sprites\whiteRook.png')
error       = PhotoImage(file = r'Sprites\error.png')
blank       = PhotoImage(file = r'Sprites\blank.png')

### Global Variables ###
logQueue = ['Temp-Log']

tiles = []

colorPick = {'bool': True , 'pick': True, 'fen': colorPick_fen}
promoting = {'bool': False, 'move': None}
endOfGame = {'bool': False, 'claimDraw': False, 'winner': None, "endType": {True: None,False: None}}
autoGame  = {'bool': False}

board = pychess.Board(fen = colorPick['fen'])

pieces_legal_moves = []

movablePiecesToggle = True

### Classes ###

#class for a square on the board
class Square(object):
	def __init__(self, square, x, y, Btn):
		global tiles

		#Position on board; pychess.square = int
		self.square = square
		#Position in window; rid(column = x, row = (9-y))
		self.x     = x
		self.y     = y

		#What is on me; {'color': pychess.Color, 'piece': pychess.PieceType}
		self.contents = None

		#If a selected piece can move here, what would that move be
		self.potentialmove = None

		#The button the user will user to interact with the board
		self.btn = Button(
				### master ###
				board_framge,
				### widget look ###
				bg = 'deep pink',
				height = 50,
				width = 50,
				bd = 2,
				relief = 'solid',
				### on press ###
				command = lambda: _squareBtnFunction(tiles[self.square]),
				activebackground = 'brown',
				### other ###
				image = error
			)

		#Change some button parts to create that hex pattern
		if   Btn == 'Btn1': 
			self.btn.configure(bg = 'orange1')
		elif Btn == 'Btn2': 
			self.btn.configure(bg = 'orange4')
		else:
			# if button is set up wrong it will be clear
			self.btn.configure(bg = 'red')

		if self.square > 63 or self.x > 8 or self.y > 8 or Btn not in ('Btn1', 'Btn2'):
			# if button is set up wrong it will be clear
			self.btn.configure(bg = 'red')

### FUNCTIONS ###

#Function to log events in the window
def log(textInpt):
	global logQueue
	textInpt = str(textInpt)

	print(textInpt)

	logQueue.append(textInpt)
	if len(logQueue) > 26:
		logQueue.pop(0)
	else: pass

	bigLog = 'Log:'
	for i in logQueue:
		if i != 'Temp-Log':
			bigLog = bigLog + '\n' + i
	log_Lbl.config(text = bigLog)
	return logQueue

def _translateColor(color):
	if color == True:
		return 'white'
	elif color == False:
		return 'black'
	else:
		log('Error:')
		log(' _translateColor(color)')
		return 'ERROR'

#Update all tile images on the board so pieces are represented in the right place
def _updateBoard():
	global board
	global colorPick
	global promoting
	global endOfGame
	global movablePiecesToggle
	global whatAIDoToggle

	movablePiecesToggle = True

	oneAutoGame_Btn.configure(bg = 'gray')

	if not colorPick['bool']:
		if board.is_checkmate():
			log('Game End:')
			log(' Checkmate')
			endOfGame['bool'] = True
			if board.is_variant_win():
				endOfGame['winner'] = board.turn
			else:
				endOfGame['winner'] = not board.turn
			endOfGame["endType"] = "won"
			log((' {0} has won').format(_translateColor(endOfGame['winner'])))
		elif board.is_stalemate():
			log('Game End:')
			log(' Stalemate')
			endOfGame['bool'] = True
			endOfGame["endType"][board.turn]     = "stalemate-ed"
			endOfGame["endType"][not board.turn] = "stalemate-er"

		if board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
			if autoGame['bool']:
				if board.is_insufficient_material():
					log('Claim draw:')
					log(' Insufficient')
					log(' material')
					log(' for the game')
					log(' to be won')
					endOfGame["endType"] = "can't win"
				elif board.is_seventyfive_moves():
					log('Claim draw:')
					log(' Seventy five')
					log(' since the last')
					log(' capture or')
					log(' pawn move')
					endOfGame["endType"] = "to many moves"
				elif board.is_fivefold_repetition():
					log('Claim draw:')
					log(' Same move')
					log(' repeated')
					endOfGame["endType"] = "is repetition"
					
				endOfGame['bool'] = True
			else:
				if board.is_insufficient_material():
					log('Claim draw:')
					log(' Insufficient')
					log(' material')
					log(' for the game')
					log(' to be won')
					endOfGame["endType"] = "can't win"
				elif board.is_seventyfive_moves():
					log('Claim draw:')
					log(' Seventy five')
					log(' since the last')
					log(' capture or')
					log(' pawn move')
					endOfGame["endType"] = "to many moves"
				elif board.is_fivefold_repetition():
					log('Claim draw:')
					log(' Same move')
					log(' repeated')
					endOfGame["endType"] = "is repetition"

				endOfGame['claimDraw'] = True

	if endOfGame['bool']:
		reset_Btn.config(bg = 'cyan4')
	else:
		reset_Btn.config(bg = 'gray')

	if endOfGame['claimDraw']:
		claimDraw_Btn.config(bg = 'cyan4')
	else:
		claimDraw_Btn.config(bg = 'gray')

	print(('Turn: {0}, Half-Turn: {1}').format(board.fullmove_number, board.halfmove_clock))
	print(board)
	print('---------------')
	
	for i in tiles:
		try:
			i.contents = board.piece_map()[i.square]
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
		elif i.contents.piece_type == 6 and i.contents.color == True:
			i.btn.config(image = whiteKing)

		if colorPick['pick'] == True:
			i.btn.grid(column = i.x, row = (9-i.y))
		if colorPick['pick'] == False:
			i.btn.grid(column = i.x, row = (i.y))

def _cleanBoard():
	movablePieces_Btn.config(bg = 'gray')
	for i in [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]:
		if board.is_check() and tiles[i].contents != None and tiles[i].contents.piece_type == 6 and board.turn == tiles[i].contents.color:
			tiles[i].btn.configure(bg = 'red')
		else:
			tiles[i].btn.configure(bg = 'orange1')
	for i in [0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63]:
		if board.is_check() and tiles[i].contents != None and tiles[i].contents.piece_type == 6 and board.turn == tiles[i].contents.color:
			tiles[i].btn.configure(bg = 'red')
		else:
			tiles[i].btn.configure(bg = 'orange4')

#This program runs when a Tile Button is pressed
def _squareBtnFunction(self):
	global board
	global tiles
	global colorPick
	global promoting
	global endOfGame
	global pieces_legal_moves

	#if you are picking colors
	if colorPick['bool']:
		if self.contents.piece_type != 6:
			pass
		else:
			colorPick['pick'] = self.contents.color
			log(('Color: {0}').format(_translateColor(colorPick['pick'])))
				
			colorPick['bool'] = False
			board.set_fen(startGame_fen)

		_cleanBoard()
		_updateBoard()
		return

	elif endOfGame['bool']:
		log('Error:')
		log(' Game has ended')
		return

	#if a piece is currently being promoted
	elif promoting['bool']:
		log('Error:')
		log(' Waiting for')
		log(' promotion')
		return

	elif self.contents == None and pieces_legal_moves == []:
		return

	elif self.contents != None and pieces_legal_moves == [] and self.contents.color is not board.turn:
		if self.contents.color == True:
			log('Error:')
			log(' BLACKS TURN')
		else:
			log('Error:')
			log(' WHITES TURN')
		return
		
	#if you have not yet picked a piece OR you pick a new piece
	elif self.contents != None and self.contents.color == board.turn and (pieces_legal_moves != [] or pieces_legal_moves == []):
		pieces_legal_moves.clear()
		_cleanBoard()

		#for all the legal moves on this board
		for move in board.legal_moves:
			#if this piece has legal moves
			if move.from_square == self.square:
				#highlight me
				self.btn.configure(bg = 'green4')
				#highlight possible moves
				if board.is_en_passant(move) or board.is_castling(move) or move.promotion != None:
					tiles[move.to_square].btn.configure(bg = 'cyan')
				else:
					tiles[move.to_square].btn.configure(bg = 'pale green')
				#create a list of this pieces possible moves
				pieces_legal_moves.append(move)
			else: pass
				
		if pieces_legal_moves == []:
			log('Error:')
			log(' Piece has no')
			log(' legal moves')
		else: pass

		return

	elif pieces_legal_moves != []:
		moved = False
		for move in pieces_legal_moves:
			if self.square == move.to_square:
				if move.promotion != None:
					_pickPromotion(move)
				else:
					board.push(move)
					_cleanBoard()
					_updateBoard()
				moved = True
				pieces_legal_moves.clear()
				break
			else: pass

		if moved == False:
			log('Error:')
			log(' Not a move')
		else: pass

	else:
		log('Error:')
		log(' _squareBtnFunction(self)')

def _pickPromotion(move):
	global promoting

	piece = tiles[move.from_square].contents

	if piece.color == True:
		promotionToQueen_Btn.configure(  bg = 'cyan4', image = whiteQueen)
		promotionToKnight_Btn.configure( bg = 'cyan4', image = whiteKing)
		promotionToRook_Btn.configure(   bg = 'cyan4', image = whiteRook)
		promotionToBishop_Btn.configure( bg = 'cyan4', image = whiteBishop)
	else:
		promotionToQueen_Btn.configure(  bg = 'cyan4', image = blackQueen)
		promotionToKnight_Btn.configure( bg = 'cyan4', image = blackKing)
		promotionToRook_Btn.configure(   bg = 'cyan4', image = blackRook)
		promotionToBishop_Btn.configure( bg = 'cyan4', image = blackBishop)

	_cleanBoard()
	tiles[move.from_square].btn.configure(bg = 'green4')
	tiles[move.to_square].btn.configure(  bg = 'cyan4')

	promoting = {'bool': True, 'move': move}

def _promotionToQueen():
	global promoting

	if promoting['bool'] == True:
		move = promoting['move']
		move.promotion = 5
		board.push(move)
		_cleanBoard()
		_updateBoard()
		_promotionReset()
	else:
		log('Error:')
		log(' Not promoting')

def _promotionToKnight():
	global promoting

	if promoting['bool'] == True:
		move = promoting['move']
		move.promotion = 2
		board.push(move)
		_cleanBoard()
		_updateBoard()
		_promotionReset()
	else:
		log('Error:')
		log(' Not promoting')

def _promotionToRook():
	global promoting

	if promoting['bool'] == True:
		move = promoting['move']
		move.promotion = 4
		board.push(move)
		_cleanBoard()
		_updateBoard()
		_promotionReset()
	else:
		log('Error:')
		log(' Not promoting')

def _promotionToBishop():
	global promoting

	if promoting['bool'] == True:
		move = promoting['move']
		move.promotion = 3
		board.push(move)
		_cleanBoard()
		_updateBoard()
		_promotionReset()
	else:
		log('Error:')
		log(' Not promoting')

def _promotionReset():
	global promoting

	promoting = {'bool': False, 'move': None}

	promotionToQueen_Btn.configure( bg = 'gray', image = blank)
	promotionToKnight_Btn.configure(bg = 'gray', image = blank)
	promotionToRook_Btn.configure(  bg = 'gray', image = blank)
	promotionToBishop_Btn.configure(bg = 'gray', image = blank)

#reset_Btn the board to initial position
def _reset():
	global board
	global colorPick
	global promoting
	global endOfGame
	global pieces_legal_moves

	if not colorPick['bool']:
		log(' - New Game - ')

	colorPick = {'bool': True , 'pick': True, 'fen': colorPick_fen}
	promoting = {'bool': False, 'move': None}
	endOfGame = {'bool': False, 'claimDraw': False, 'winner': None, "endType": None}
	autoGame  = {'bool': False}

	pieces_legal_moves = []

	board.set_fen(colorPick['fen'])

	log('Pick A Color')

	_cleanBoard()
	_updateBoard()
	_promotionReset()

def _claimDraw():
	if (board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition()) and not colorPick['bool']:
		log('Draw:')
		log(' A draw was')
		log(' claimed')
		_reset()
	else:
		log('Error:')
		log(' Cannot claim')
		log(' draw')

def _movablePieces():
	global tiles
	global colorPick
	global promoting
	global endOfGame
	global movablePiecesToggle

	if not colorPick['bool'] and not promoting['bool'] and not endOfGame['bool']:
		if movablePiecesToggle == True:
			_cleanBoard()
			for i in board.legal_moves:
				tiles[i.from_square].btn.configure(bg = 'green4')
			pieces_legal_moves = []
			movablePieces_Btn.config(bg = 'cyan4')
		else:
			_cleanBoard()
			movablePieces_Btn.config(bg = 'gray')
	
	elif endOfGame['bool']:
		log("Moveables:")
		log(" Game ended")

	elif colorPick['bool'] or promoting['bool']:
		log("Moveables:")
		log(" No moves to")
		log(" highlight")

	else:
		log("Error:")
		log(" movablePieces-1")


	movablePiecesToggle = not movablePiecesToggle

#Do a random move
def _randMove():
	global board

	moveSet = []
	for move in board.legal_moves:
		moveSet.append(move)

	move = r.choice(moveSet)

	if move.promotion != None:
		move.promotion = r.choice([2, 3, 4, 5])
	else: pass

	return move

def _gilgMove(popNum):
	move = _randMove()
	return move

def _doAutoTurn():
	global board
	global colorPick
	global promoting
	global endOfGame

	if algorithem[board.turn] == 0:
		log("Auto Turn:")
		log(" Waiting for")
		log(" human move")
		pass
	elif algorithem[board.turn] == 1:
		if not colorPick['bool'] and not promoting['bool'] and not endOfGame['bool']:
			board.push(_randMove())
			_cleanBoard()
			_updateBoard()

		elif endOfGame['bool']:
			log("Auto Turn:")
			log(" Game ended")

		elif colorPick['bool'] or promoting['bool']:
			log("Auto Turn:")
			log(" Cannot auto")
			log(" pick")

		else:
			log("Error:")
			log(" doAutoTurn-2")
	elif algorithem[board.turn] == 2:
		if not colorPick['bool'] and not promoting['bool'] and not endOfGame['bool']:
			board.push(_gilgMove())
			_cleanBoard()
			_updateBoard()

		elif endOfGame['bool']:
			log("Auto Turn:")
			log(" Game ended")

		elif colorPick['bool'] or promoting['bool']:
			log("Auto Turn:")
			log(" Cannot auto")
			log(" pick")

		else:
			log("Error:")
			log(" doAutoTurn-2")
	elif algorithem[board.turn] == 3:
		pass
	else:
		log("Error:")
		log(" doAutoTurn-1")

def _whatAIDo():
	global board
	global tiles
	global colorPick
	global promoting
	global endOfGame

	if not colorPick['bool'] and not promoting['bool'] and not endOfGame['bool']:
		_cleanBoard()
		move = _randMove()

		for i in tiles:
			if i.square == move.from_square:
				i.btn.config(bg = "green4")
			elif i.square == move.to_square:
				if board.is_en_passant(move) or board.is_castling(move) or move.promotion != None:
					i.btn.config(bg = "cyan")
				else:
					i.btn.config(bg = "pale green")
			else: pass
	
	elif endOfGame['bool']:
		log("whatAIDo?:")
		log(" Game ended")

	elif colorPick['bool'] or promoting['bool']:
		log("whatAIDo?:")
		log(" No moves to")
		log(" highlight")

	else:
		log("Error:")
		log(" whatAIDo?-1")

def _oneAutoGame():
	global board
	global colorPick
	global endOfGame
	global autoGame

	if colorPick['bool'] or endOfGame['bool']:
		_reset()
		autoGame['bool']  = True
		colorPick['bool'] = False
		log(('Color: {0}').format(_translateColor(colorPick['pick'])))
		board.set_fen(startGame_fen)
		_updateBoard()
		while not endOfGame['bool']:
			board.push(_randMove())
			_cleanBoard()
			_updateBoard()

	else:
		log("Auto Game:")
		log(" Must reset")
		log(" game")

### Set Tkinter Window ###
chess_TK.title('Chess')
chess_TK.geometry('860x500')

log_Frame = Frame(chess_TK, width=200, height=455, bg='white', bd = 2, relief = 'solid')
log_Frame.grid(row=0, column=0, padx=5, pady=5)

board_framge = Frame(chess_TK, width=200, height= 455, bg='white', bd = 2, relief = 'solid')
board_framge.grid(row=0, column=1, padx=5, pady=5)

control_Frame = Frame(chess_TK, width=100, height= 455)
control_Frame.grid(row=0, column=2, padx=5, pady=5)

### Log Frame ###
log_Lbl = Label(log_Frame, bg = 'white', height = 28, width = 15, bd = 2, relief = 'solid', text = 'Log:', font=('Courier', 10), anchor = 'nw', justify = 'left')
log_Lbl.grid(row=0, column=0)

mveLog_Lbl = Label(log_Frame, bg = 'white', height = 28, width = 15, bd = 2, relief = 'solid', text = 'moves:', font=('Courier', 10), anchor = 'nw', justify = 'left')
mveLog_Lbl.grid(row=0, column=1)

### Board Frame ###
count = 0
Xcount = 1
Ycount = 1
while count < 64:
	#print('count: ' + str(count))
	#print('X: '     + str(Xcount))
	#print('Y: '     + str(Ycount))

	if count in [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]:
		tiles.append(Square(count, Xcount, Ycount, 'Btn1'))
	if count in [0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63]:
		tiles.append(Square(count, Xcount, Ycount, 'Btn2'))

	Xcount += 1
	if Xcount > 8:
		Xcount = 1
		Ycount += 1

	count += 1

### Controle Frame ###
def _drawBar1():
	newLine_Canv = Canvas(control_Frame, width=50, height=2.5)
	newLine_Canv.create_line(0, 0, 400, 0, width = 10)
	newLine_Canv.pack(pady=0.625)

promotion_Frame = Frame(control_Frame, width=100, height= 100, bd = 2, relief = 'solid')
promotion_Frame.pack(pady=2)

_drawBar1()

reset_Btn = Button(control_Frame, bg = 'gray', text=('Reset Game'), font=('TkDefaultFont', 10), height = 2, width = 12, command = _reset, activebackground = 'gray30')
reset_Btn.pack(pady=2)

claimDraw_Btn = Button(control_Frame, bg = 'gray', text=('Claim Draw'), font=('TkDefaultFont', 10), height = 2, width = 12, command = _claimDraw, activebackground = 'gray30')
claimDraw_Btn.pack(pady=2)

_drawBar1()

movablePieces_Btn = Button(control_Frame, bg = 'gray', text=('Movable Pieces?'), font=('TkDefaultFont', 10), height = 2, width = 12, command = _movablePieces, activebackground = 'gray30')
movablePieces_Btn.pack(pady=2)

_drawBar1()

doAutoTurn_Btn = Button(control_Frame, bg = 'gray', text=('Do Auto Turn'), font=('TkDefaultFont', 10), height = 2, width = 12, command = _doAutoTurn, activebackground = 'gray30')
doAutoTurn_Btn.pack(pady=2)

whatAIDo_Btn = Button(control_Frame, bg = 'gray', text=('AIs Suggestion'), font=('TkDefaultFont', 10), height = 2, width = 12, command = _whatAIDo, activebackground = 'gray30')
whatAIDo_Btn.pack(pady=2)

oneAutoGame_Btn = Button(control_Frame, bg = 'gray', text=('One Auto Game'), font=('TkDefaultFont', 10), height = 2, width = 12, command= _oneAutoGame, activebackground = 'gray30')
oneAutoGame_Btn.pack(pady=2)

empty_Btn = Button(control_Frame, bg = 'gray', text=(''), font=('TkDefaultFont', 10), height = 2, width = 12, command= print, activebackground = 'gray30')
empty_Btn.pack(pady=2)

_drawBar1()

### Promotion Frame ###
promotionToQueen_Btn  = Button(promotion_Frame, bg = 'gray', height = 40, width = 40, bd = 2, relief = 'solid', command = _promotionToQueen , activebackground = 'brown', image = blank)
promotionToQueen_Btn.grid(row=0 , column=0)

promotionToKnight_Btn = Button(promotion_Frame, bg = 'gray', height = 40, width = 40, bd = 2, relief = 'solid', command = _promotionToKnight, activebackground = 'brown', image = blank)
promotionToKnight_Btn.grid(row=1 , column=0)

promotionToRook_Btn   = Button(promotion_Frame, bg = 'gray', height = 40, width = 40, bd = 2, relief = 'solid', command = _promotionToRook  , activebackground = 'brown', image = blank)
promotionToRook_Btn.grid(row=0 , column=1)

promotionToBishop_Btn = Button(promotion_Frame, bg = 'gray', height = 40, width = 40, bd = 2, relief = 'solid', command = _promotionToBishop, activebackground = 'brown', image = blank)
promotionToBishop_Btn.grid(row=1 , column=1)

### Built Window ###
log(' - New Game - ')
_reset()
chess_TK.mainloop()