#!/usr/bin/env python3

import sys
from PyQt4 import QtCore, QtGui, uic
import scrabble
import pickle

class ScrabbleGUI(QtGui.QMainWindow):
	def __init__(self):
		# Load layout
		self.ui = uic.loadUi("scrabble-gui.ui")

		# Create tile backgrounds
		for x in range(0, 15):
			for y in range(0, 15):
				self.ui.board.setItem(y, x, QtGui.QTableWidgetItem(' '))
				self.ui.board.item(y, x).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
				self.ui.board.item(y, x).setFont(QtGui.QFont("Sans", 10, QtGui.QFont.Bold))
				# Double letter
				if scrabble.letter_mult[y][x] == 2:
					self.ui.board.item(y, x).setBackground(QtGui.QColor(0, 0, 127, 100))
				# Triple letter
				elif scrabble.letter_mult[y][x] == 3:
					self.ui.board.item(y, x).setBackground(QtGui.QColor(0, 170, 0, 100))
				# Double word
				elif scrabble.word_mult[y][x] == 2:
					self.ui.board.item(y, x).setBackground(QtGui.QColor(170, 0, 0, 100))
				# Triple word
				elif scrabble.word_mult[y][x] == 3:
					self.ui.board.item(y, x).setBackground(QtGui.QColor(255, 170, 0, 100))
		# Center
		self.ui.board.item(7, 7).setBackground(QtGui.QColor(0, 0, 0, 100))


		# Event handlers
		self.connect(self.ui.solve, QtCore.SIGNAL("clicked()"), self.solve)
		self.connect(self.ui.save, QtCore.SIGNAL("clicked()"), self.save)
		self.connect(self.ui.load, QtCore.SIGNAL("clicked()"), self.load)

		self.load()

		# Show window
		self.ui.show()
	def solve(self):
		scrabble.tiles = self.ui.letters.text()

		for x in range(0, 15):
			for y in range(0, 15):
				char = self.ui.board.item(y, x).text()
				if char in "abcdefghijklmnopqrstuvwxyz":
					scrabble.board[y][x] = char
				else:
					self.ui.board.item(y, x).setText(' ')
					scrabble.board[y][x] = ' '

		valid_words = scrabble.solve()

		self.ui.results.clear()
		for word in sorted(scrabble.unique(valid_words), key=lambda word: word[4]):
			if word[3] == scrabble.HORIZONTAL:
				self.ui.results.append("Horz: x: %2i  y: %2i score: %i word: %s" % (word[1]+1, word[2]+1, word[4], word[0]))
			if word[3] == scrabble.VERTICAL:
				self.ui.results.append("Vert: x: %2i  y: %2i score: %i word: %s" % (word[1]+1, word[2]+1, word[4], word[0]))

	def save(self):
		data = {
			"board": scrabble.board,
			"tiles": ""
		}
		for x in range(0, 15):
			for y in range(0, 15):
				char = self.ui.board.item(y, x).text()
				if char in "abcdefghijklmnopqrstuvwxyz":
					data["board"][y][x] =  char
				else:
					self.ui.board.item(y, x).setText(' ')
					data["board"][y][x] = ' '
		data["tiles"] = self.ui.letters.text()

		# TODO choose save file
		save_file = open('data.pkl', 'wb')
		pickle.dump(data, save_file)
		save_file.close()

	def load(self):
		# TODO choose save file
		try:
			save_file = open('data.pkl', 'rb')
			data = pickle.load(save_file)
			save_file.close()

			self.ui.letters.setText(data["tiles"])
			for x in range(0, 15):
				for y in range(0, 15):
					self.ui.board.item(y, x).setText(data["board"][y][x])
		except:
			print("Couldn't load file")


def main():
	app = QtGui.QApplication(sys.argv)
	window = ScrabbleGUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
