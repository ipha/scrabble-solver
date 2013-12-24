#!/usr/bin/env python3
import itertools

SCRABBLE = 0
WORDSWITHFRIENDS = 1

HORIZONTAL = 0
VERTICAL = 1

class Solver:
	def __init__(self, game_type=WORDSWITHFRIENDS, wordfile="wordlist.txt"):
		# Import wordlist
		self.wordlist = set(open(wordfile).read().split())

		# Init structures
		self.board = [[' '] * 15 for x in range(15)]

		self.blanks = []

		# Left/Up scan cache
		# self.left_cache = [[0] * 15 for x in range(15)]
		# self.up_cache = [[0] * 15 for x in range(15)]

		# Scrabble
		if game_type == SCRABBLE:
			self.letter_mult = (
				(1,1,1,2,1,1,1,1,1,1,1,2,1,1,1),
				(1,1,1,1,1,3,1,1,1,3,1,1,1,1,1),
				(1,1,1,1,1,1,2,1,2,1,1,1,1,1,1),
				(2,1,1,1,1,1,1,2,1,1,1,1,1,1,2),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,3,1,1,1,3,1,1,1,3,1,1,1,3,1),
				(1,1,2,1,1,1,2,1,2,1,1,1,2,1,1),
				(1,1,1,2,1,1,1,1,1,1,1,2,1,1,1),
				(1,1,2,1,1,1,2,1,2,1,1,1,2,1,1),
				(1,3,1,1,1,3,1,1,1,3,1,1,1,3,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(2,1,1,1,1,1,1,2,1,1,1,1,1,1,2),
				(1,1,1,1,1,1,2,1,2,1,1,1,1,1,1),
				(1,1,1,1,1,3,1,1,1,3,1,1,1,1,1),
				(1,1,1,2,1,1,1,1,1,1,1,2,1,1,1))

			self.word_mult = (
				(3,1,1,1,1,1,1,3,1,1,1,1,1,1,3),
				(1,2,1,1,1,1,1,1,1,1,1,1,1,2,1),
				(1,1,2,1,1,1,1,1,1,1,1,1,2,1,1),
				(1,1,1,2,1,1,1,1,1,1,1,2,1,1,1),
				(1,1,1,1,2,1,1,1,1,1,2,1,1,1,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(3,1,1,1,1,1,1,1,1,1,1,1,1,1,3),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,1,1,1,2,1,1,1,1,1,2,1,1,1,1),
				(1,1,1,2,1,1,1,1,1,1,1,2,1,1,1),
				(1,1,2,1,1,1,1,1,1,1,1,1,2,1,1),
				(1,2,1,1,1,1,1,1,1,1,1,1,1,2,1),
				(3,1,1,1,1,1,1,3,1,1,1,1,1,1,3))

			self.letter_value = {
				'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,  'f': 4,
				'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5,  'l': 1,
				'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
				's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4,  'x': 8,
				'y': 4, 'z': 10,
				'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0,  'F': 0,
				'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0,  'L': 0,
				'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0,  'R': 0,
				'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0,  'X': 0,
				'Y': 0, 'Z': 0}
			self.all_tiles_bonus = 50

		# Words with Friends
		else:
			self.letter_mult = (
				(1,1,1,1,1,1,3,1,3,1,1,1,1,1,1),
				(1,1,2,1,1,1,1,1,1,1,1,1,2,1,1),
				(1,2,1,1,2,1,1,1,1,1,2,1,1,2,1),
				(1,1,1,3,1,1,1,1,1,1,1,3,1,1,1),
				(1,1,2,1,1,1,2,1,2,1,1,1,2,1,1),
				(1,1,1,1,1,3,1,1,1,3,1,1,1,1,1),
				(3,1,1,1,2,1,1,1,1,1,2,1,1,1,3),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(3,1,1,1,2,1,1,1,1,1,2,1,1,1,3),
				(1,1,1,1,1,3,1,1,1,3,1,1,1,1,1),
				(1,1,2,1,1,1,2,1,2,1,1,1,2,1,1),
				(1,1,1,3,1,1,1,1,1,1,1,3,1,1,1),
				(1,2,1,1,2,1,1,1,1,1,2,1,1,2,1),
				(1,1,2,1,1,1,1,1,1,1,1,1,2,1,1),
				(1,1,1,1,1,1,3,1,3,1,1,1,1,1,1))

			self.word_mult = (
				(1,1,1,3,1,1,1,1,1,1,1,3,1,1,1),
				(1,1,1,1,1,2,1,1,1,2,1,1,1,1,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(3,1,1,1,1,1,1,2,1,1,1,1,1,1,3),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,2,1,1,1,1,1,1,1,1,1,1,1,2,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,1,1,2,1,1,1,1,1,1,1,2,1,1,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,2,1,1,1,1,1,1,1,1,1,1,1,2,1),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(3,1,1,1,1,1,1,2,1,1,1,1,1,1,3),
				(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
				(1,1,1,1,1,2,1,1,1,2,1,1,1,1,1),
				(1,1,1,3,1,1,1,1,1,1,1,3,1,1,1))

			self.letter_value = {
				'a': 1, 'b': 4, 'c': 4, 'd': 2,  'e': 1,  'f': 4, 
				'g': 3, 'h': 3, 'i': 1, 'j': 10, 'k': 5,  'l': 2,
				'm': 4, 'n': 2, 'o': 1, 'p': 4,  'q': 10, 'r': 1,
				's': 1, 't': 1, 'u': 2, 'v': 5,  'w': 4,  'x': 8,
				'y': 3, 'z': 10,
				'A': 0, 'B': 0, 'C': 0, 'D': 0,  'E': 0,  'F': 0,
				'G': 0, 'H': 0, 'I': 0, 'J': 0,  'K': 0,  'L': 0,
				'M': 0, 'N': 0, 'O': 0, 'P': 0,  'Q': 0,  'R': 0,
				'S': 0, 'T': 0, 'U': 0, 'V': 0,  'W': 0,  'X': 0,
				'Y': 0, 'Z': 0}

			self.all_tiles_bonus = 35

	# Cache the location of connected letters
	def __update_cache(self):
		left_cache = [[0] * 15 for x in range(15)]
		up_cache = [[0] * 15 for x in range(15)]
		for x in range(15):
			for y in range(15):
				x_start = x
				y_start = y

				while (x_start > 0) and (self.board[y][x_start-1] != ' ' ):
					x_start -= 1
				while (y_start > 0) and (self.board[y_start-1][x] != ' ' ):
					y_start -= 1

				left_cache[y][x] = x_start
				up_cache[y][x] = y_start
		self.left_cache = tuple(tuple(i) for i in left_cache)
		self.up_cache = tuple(tuple(i) for i in up_cache)

	# Check if word fits on board
	def __check_spot(self, x, y, length, direction):

		al = length
		ax = x
		ay = y

		# Special case for first word
		if (x == 7) and (y == 7) and (self.board[7][7] == ' '):
			return True

		if self.board[y][x] != ' ':
			return False

		elif direction == HORIZONTAL:
			while (al > 0) and (ax < 15):
				if self.board[ay][ax] == ' ':
					al -= 1
				ax += 1
			# Too long
			if al != 0:
				return False
			# Make sure word touches other letters
			# 
			# Intersects other letter(s)
			elif ax > x + length:
				return True
			# Touches on left
			elif (x > 0) and (self.board[y][x-1] != ' '):
				return True
			# Touches on right
			elif (x + length < 15) and (self.board[y][x + length] != ' '):
				return True
			# Touches on top or bottom
			for i in range(x, x + length):
				if (y > 0) and (self.board[y-1][i] != ' '):
					return True
				elif (y < 14) and (self.board[y+1][i] != ' '):
					return True
		elif direction == VERTICAL:
			while (al > 0) and (ay < 15):
				if self.board[ay][ax] == ' ':
					al -= 1
				ay += 1
			# Too long
			if al != 0:
				return False
			# Make sure word touches other letters
			# 
			# Intersects other letter(s)
			if ay > y + length:
				return True
			# Touches on top
			elif (y > 0) and (self.board[y-1][x] != ' '):
				return True
			# Touches on bottom
			elif (y + length < 15) and (self.board[y + length][x] != ' '):
				return True
			# Touches on left or right
			for i in range(y, y + length):
				if (x > 0) and (self.board[i][x-1] != ' '):
					return True
				elif (x < 14) and (self.board[i][x+1] != ' '):
					return True
		# Bad spot
		return False

	# Get frame of word
	# @profile
	def __get_frame(self, x, y, length, direction):
		frame = []
		if direction == HORIZONTAL:
			xi = self.left_cache[y][x]
			while (xi < 15) and (self.board[y][xi] != ' '):
				frame.append(self.board[y][xi])
				xi += 1
			for j in range(length):
				frame.append(self.board[y][xi])
				xi += 1
				while (xi < 15) and (self.board[y][xi] != ' '):
					frame.append(self.board[y][xi])
					xi += 1
				
		if direction == VERTICAL:
			yi = self.up_cache[y][x]
			while (yi < 15) and (self.board[yi][x] != ' '):
				frame.append(self.board[yi][x])
				yi += 1
			for j in range(length):
				frame.append(self.board[yi][x])
				yi += 1
				while (yi < 15) and (self.board[yi][x] != ' '):
					frame.append(self.board[yi][x])
					yi += 1
		return ''.join(frame).replace(' ', '%c')

	# Get new word created
	# TODO: use frames?
	def __get_full_word(self, x, y, string, direction):
		word = ""

		if direction == HORIZONTAL:
			x_start = self.left_cache[y][x]
			x_end = x_start

			while (x_end < 15) and (self.board[y][x_end] != ' '):
				word += self.board[y][x_end]
				x_end += 1
			for char in string:
				word += char
				x_end += 1
				while (x_end < 15) and (self.board[y][x_end] != ' '):
					word += self.board[y][x_end]
					x_end += 1
			return (word, x_start, x_end)

		elif direction == VERTICAL:
			y_start = self.up_cache[y][x]
			y_end = y_start

			while (y_end < 15) and (self.board[y_end][x] != ' '):
				word += self.board[y_end][x]
				y_end += 1
			for char in string:
				word += char
				y_end += 1
				while (y_end < 15) and (self.board[y_end][x] != ' '):
					word += self.board[y_end][x]
					y_end += 1
			return (word, y_start, y_end)

	def __calculate_score(self, x, y, word, direction):
		used_count = 0
		score = 0
		score_mult = 1
		secondary_score = 0
		words_created = 1
		triple_word_used = False

		if direction == HORIZONTAL:
			for i in range(0, len(word)):
				# Tile we placed
				if self.board[y][x+i] == ' ':
					used_count += 1
					score += self.letter_value[word[i]] * self.letter_mult[y][x+i]
					score_mult *= self.word_mult[y][x+i]
					if self.word_mult[y][x+i] == 3:
						triple_word_used = True

					# Check new veritcal words
					(vert_word, y_start, y_end) = self.__get_full_word(x+i, y, word[i], VERTICAL)
					if len(vert_word) > 1:
						words_created += 1
						vert_score = 0
						for char in vert_word:
							vert_score += self.letter_value[char]
						vert_score += self.letter_value[word[i]] * (self.letter_mult[y][x+i]-1)
						secondary_score += (vert_score * self.word_mult[y][x+i])
				# Existing tile
				elif (x+i, y) not in self.blanks:
					score += self.letter_value[word[i]]
		if direction == VERTICAL:
			for i in range(0, len(word)):
				# Tile we placed
				if self.board[y+i][x] == ' ':
					used_count += 1
					score += self.letter_value[word[i]] * self.letter_mult[y+i][x]
					score_mult *= self.word_mult[y+i][x]
					if self.word_mult[y+i][x] == 3:
						triple_word_used = True

					# Check new horrizontal words
					(horz_word, x_start, x_end) = self.__get_full_word(x, y+i, word[i], HORIZONTAL)
					if len(horz_word) > 1:
						words_created += 1
						horz_score = 0
						for char in horz_word:
							horz_score += self.letter_value[char]
						horz_score += self.letter_value[word[i]] * (self.letter_mult[y+i][x]-1)
						secondary_score += (horz_score * self.word_mult[y+i][x])
				# Existing tile
				elif (x, y+i) not in self.blanks:
					score += self.letter_value[word[i]]
		total_score = (score * score_mult) + (self.all_tiles_bonus if used_count == 7 else 0) + secondary_score
		# Weight score
		# +20% if triple word is used
		# -5% for each word created over 2
		# -20% for 2 letter words
		weight_score = total_score
		if triple_word_used:
			weight_score *= 1.2
		if words_created > 2:
			weight_score *= 0.95**(words_created-2)
		if len(word) == 2:
			weight_score *= 0.8
		return (total_score, weight_score)
	# @profile
	def solve(self, tiles):
		self.__update_cache()

		valid_words = []

		# Generate tile permutations
		# 
		# (Better way of doing this?)
		tiles_perm = [ set() for i in range(7) ]
		if '*' in tiles:
			if tiles.count('*') > 1:
				print("Multiple blanks not yet supported")
				return []
			for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				for i in range(7):
					tiles_perm[i].update(itertools.permutations(tiles.replace('*', char), i+1))
		else:
			for i in range(7):
				tiles_perm[i].update(itertools.permutations(tiles, i+1))


		for length in range(7):
			# Horizontal pass
			print("Checking length %i, horizontal" % (length + 1))
			for y in range(15):
				for x in range(15 - length):
					if self.__check_spot(x, y, length+1, HORIZONTAL):
						# Get frame for spot
						frame = self.__get_frame(x, y, length+1, HORIZONTAL)
						# Valid starting spot, check every permutation
						for word in tiles_perm[length]:
							# Check new horizontal word
							if (frame % word).lower() in self.wordlist:
								# Check each new vertical word
								(new_word, x_start, x_end) = self.__get_full_word(x, y, word, HORIZONTAL)
								print("%2i, %2i: %s" % (x, y, new_word))
								valid = True
								for i in range(x_start, x_end):
									if self.board[y][i] == ' ':
										(vert_word, y_start, y_end) = self.__get_full_word(i, y, new_word[i - x_start], VERTICAL)
										if not(vert_word.lower() in self.wordlist) and len(vert_word) > 1:
											valid = False
											break
								if valid:
									(total_score, weight_score) = self.__calculate_score(x_start, y, new_word, HORIZONTAL)
									valid_words.append([new_word, x_start, y, HORIZONTAL, weight_score, total_score])
			print("Checking length %i, vertical" % (length + 1))
			for y in range(15-length):
				for x in range(15 ):
					if self.__check_spot(x, y, length+1, VERTICAL):
						# Get frame for spot
						frame = self.__get_frame(x, y, length+1, VERTICAL)
						if(y == 12 and x == 5):
							print(frame)

						# Valid starting spot, check every permutation
						for word in tiles_perm[length]:
							# Check new vertical word
							if (frame % word).lower() in self.wordlist:
								# Check each new horizontal word
								(new_word, y_start, y_end) = self.__get_full_word(x, y, word, VERTICAL)
								print("%2i, %2i: %s" % (x, y, new_word))
								valid = True
								for i in range(y_start, y_end):
									if self.board[i][x] == ' ':
										(horz_word, x_start, x_end) = self.__get_full_word(x, i, new_word[i - y_start], HORIZONTAL)
										if not(horz_word.lower() in self.wordlist) and len(horz_word) > 1:
											valid = False
											break
								if valid:
									(total_score, weight_score) = self.__calculate_score(x, y_start, new_word, VERTICAL)
									valid_words.append([new_word, x, y_start, VERTICAL, weight_score, total_score])

		return sorted(valid_words, key=lambda word: word[4])
