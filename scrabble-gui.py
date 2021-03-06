#!/usr/bin/env python3

import sys
from PyQt4 import QtCore, QtGui, uic
import scrabble
import pickle

class ScrabbleGUI(QtGui.QMainWindow):
	def __init__(self, parent=None, filename="data"):
		QtGui.QMainWindow.__init__(self, parent)
		# Load layout
		uic.loadUi("scrabble-gui.ui", self)

		# Create solver instance
		self.solver = scrabble.Solver(scrabble.WORDSWITHFRIENDS)

		# save file name
		self.filename = filename

		# Create tile backgrounds
		for x in range(0, 15):
			for y in range(0, 15):
				self.board.setItem(y, x, QtGui.QTableWidgetItem(' '))
				self.board.item(y, x).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
				self.board.item(y, x).setFont(QtGui.QFont("Sans", 10, QtGui.QFont.Bold))
				# Double letter
				if self.solver.letter_mult[y][x] == 2:
					self.board.item(y, x).setBackground(QtGui.QColor(0, 0, 127, 100))
				# Triple letter
				elif self.solver.letter_mult[y][x] == 3:
					self.board.item(y, x).setBackground(QtGui.QColor(0, 170, 0, 100))
				# Double word
				elif self.solver.word_mult[y][x] == 2:
					self.board.item(y, x).setBackground(QtGui.QColor(170, 0, 0, 100))
				# Triple word
				elif self.solver.word_mult[y][x] == 3:
					self.board.item(y, x).setBackground(QtGui.QColor(255, 170, 0, 100))
		# Center
		self.board.item(7, 7).setBackground(QtGui.QColor(0, 0, 0, 100))


		# Event handlers
		self.connect(self.solve_btn, QtCore.SIGNAL("clicked()"), self.solve)
		self.connect(self.save_btn, QtCore.SIGNAL("clicked()"), self.save)
		self.connect(self.load_btn, QtCore.SIGNAL("clicked()"), self.load)

		self.load()

		# Show window
		self.show()
	def add(self, text):
		self.results.append(text)

	def solve(self):
		self.solve_btn.setEnabled(False)
		self.solve_btn.setText("Solving...")
		self.results.clear()

		self.solver.blanks = []
		for x in range(0, 15):
			for y in range(0, 15):
				char = self.board.item(y, x).text()
				if char in "abcdefghijklmnopqrstuvwxyz":
					self.solver.board[y][x] = char
				elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
					self.solver.board[y][x] = char.lower()
					self.solver.blanks.append((x,y))
				else:
					self.board.item(y, x).setText(' ')
					self.solver.board[y][x] = ' '
		# Start solver thread
		self.thread = WorkThread(self.solver, self.letters.text())
		self.connect( self.thread, QtCore.SIGNAL("update(QString)"), self.add )
		self.connect( self.thread, QtCore.SIGNAL("finished()"), self.solve_done )
		self.thread.start()

	def solve_done(self):
		self.solve_btn.setEnabled(True)
		self.solve_btn.setText("Solve")

	def save(self):
		data = {
			"board": self.solver.board,
			"tiles": ""
		}
		for x in range(0, 15):
			for y in range(0, 15):
				char = self.board.item(y, x).text()
				if char in "abcdefghijklmnopqrstuvwxyz":
					data["board"][y][x] =  char
				else:
					self.board.item(y, x).setText(' ')
					data["board"][y][x] = ' '
		data["tiles"] = self.letters.text()

		# TODO choose save file
		save_file = open(self.filename + ".pkl", 'wb')
		pickle.dump(data, save_file)
		save_file.close()

	def load(self):
		# TODO choose save file
		try:
			save_file = open(self.filename + ".pkl", 'rb')
			data = pickle.load(save_file)
			save_file.close()

			self.letters.setText(data["tiles"])
			for x in range(0, 15):
				for y in range(0, 15):
					self.board.item(y, x).setText(data["board"][y][x])
		except:
			print("Couldn't load file")

class WorkThread(QtCore.QThread):
	def __init__(self, solver, tiles):
		QtCore.QThread.__init__(self)
		self.solver = solver
		self.tiles = tiles
	
	def __del__(self):
		self.wait()
	
	def run(self):
		valid_words = self.solver.solve(self.tiles)
		for word in valid_words:
			if word[3] == scrabble.HORIZONTAL:
				self.emit(QtCore.SIGNAL("update(QString)"),
					"Horz: x: %2i  y: %2i weight: %i score: %i word: %s" % (word[1]+1, word[2]+1, word[4], word[5], word[0]))
			if word[3] == scrabble.VERTICAL:
				self.emit(QtCore.SIGNAL("update(QString)"),
					"Vert: x: %2i  y: %2i weight: %i score: %i word: %s" % (word[1]+1, word[2]+1, word[4], word[5], word[0]))
		return

def main():
	app = QtGui.QApplication(sys.argv)
	if len( sys.argv ) == 1:
		window = ScrabbleGUI()
	else:
		window = ScrabbleGUI(filename=sys.argv[1])
	window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
