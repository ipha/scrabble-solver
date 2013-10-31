#!/usr/bin/env python3
import itertools

# User input
# 

tiles = "seoezit"
board = [
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ','e',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ','l',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ','u',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ','g',' ',' ','t',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ','c','r','a','n','e',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	['j',' ','a','h',' ',' ',' ',' ',' ',' ','c',' ',' ',' ',' '],
	['u',' ','d','i',' ',' ',' ','h','o','u','r','i',' ',' ',' '],
	['m',' ','u',' ','f','i','n','e',' ',' ','y',' ',' ',' ',' '],
	['p','e','a','h','e','n',' ','r',' ','w',' ',' ',' ',' ',' '],
	['e',' ','l',' ',' ',' ',' ','b','y','e',' ',' ',' ',' ',' '],
	['d',' ','s',' ',' ',' ',' ','e',' ','i',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ','d',' ','g',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ','h',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ','r','o','o','s','t','e','d',' ',' ']]

# Import wordlist
# 

wordlist = set()
wordfile = open("wordlist.txt")
for line in wordfile:
	wordlist.add(line.strip().lower())
wordfile.close()

# Board structure
# 
# (Replace 1s with ' ' to make it easier to read
HORIZONTAL = 0
VERTICAL = 1

# # Scrabble
# letter_mult = [
# 	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
# 	[1,1,1,1,1,3,1,1,1,3,1,1,1,1,1],
# 	[1,1,1,1,1,1,2,1,2,1,1,1,1,1,1],
# 	[2,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
# 	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# 	[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
# 	[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
# 	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
# 	[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
# 	[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
# 	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# 	[2,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
# 	[1,1,1,1,1,1,2,1,2,1,1,1,1,1,1],
# 	[1,1,1,1,1,3,1,1,1,3,1,1,1,1,1],
# 	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1]]

# word_mult = [
# 	[3,1,1,1,1,1,1,3,1,1,1,1,1,1,3],
# 	[1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
# 	[1,1,2,1,1,1,1,1,1,1,1,1,2,1,1],
# 	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
# 	[1,1,1,1,2,1,1,1,1,1,2,1,1,1,1],
# 	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# 	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# 	[3,1,1,1,1,1,1,1,1,1,1,1,1,1,3],
# 	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# 	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# 	[1,1,1,1,2,1,1,1,1,1,2,1,1,1,1],
# 	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
# 	[1,1,2,1,1,1,1,1,1,1,1,1,2,1,1],
# 	[1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
# 	[3,1,1,1,1,1,1,3,1,1,1,1,1,1,3]]

# Words with Friends
letter_mult = [
	[1,1,1,1,1,1,3,1,3,1,1,1,1,1,1],
	[1,1,2,1,1,1,1,1,1,1,1,1,2,1,1],
	[1,2,1,1,2,1,1,1,1,1,2,1,1,2,1],
	[1,1,1,3,1,1,1,1,1,1,1,3,1,1,1],
	[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
	[1,1,1,1,1,3,1,1,1,3,1,1,1,1,1],
	[3,1,1,1,2,1,1,1,1,1,2,1,1,1,3],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[3,1,1,1,2,1,1,1,1,1,2,1,1,1,3],
	[1,1,1,1,1,3,1,1,1,3,1,1,1,1,1],
	[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
	[1,1,1,3,1,1,1,1,1,1,1,3,1,1,1],
	[1,2,1,1,2,1,1,1,1,1,2,1,1,2,1],
	[1,1,2,1,1,1,1,1,1,1,1,1,2,1,1],
	[1,1,1,1,1,1,3,1,3,1,1,1,1,1,1]]

word_mult = [
	[1,1,1,3,1,1,1,1,1,1,1,3,1,1,1],
	[1,1,1,1,1,2,1,1,1,2,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[3,1,1,1,1,1,1,2,1,1,1,1,1,1,3],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,2,1,1,1,1,1,1,1,2,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[3,1,1,1,1,1,1,2,1,1,1,1,1,1,3],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,2,1,1,1,2,1,1,1,1,1],
	[1,1,1,3,1,1,1,1,1,1,1,3,1,1,1]]

# Letter value
# 

# # Scrabble
# letter_value = {
# 	'a': 1,
# 	'b': 3,
# 	'c': 3,
# 	'd': 2,
# 	'e': 1,
# 	'f': 4,
# 	'g': 2,
# 	'h': 4,
# 	'i': 1,
# 	'j': 8,
# 	'k': 5,
# 	'l': 1,
# 	'm': 3,
# 	'n': 1,
# 	'o': 1,
# 	'p': 3,
# 	'q': 10,
# 	'r': 1,
# 	's': 1,
# 	't': 1,
# 	'u': 1,
# 	'v': 4,
# 	'w': 4,
# 	'x': 8,
# 	'y': 4,
# 	'z': 10}

# Words with Friends
letter_value = {
	'a': 1,
	'b': 4,
	'c': 4,
	'd': 2,
	'e': 1,
	'f': 4,
	'g': 3,
	'h': 3,
	'i': 1,
	'j': 10,
	'k': 5,
	'l': 2,
	'm': 4,
	'n': 2,
	'o': 1,
	'p': 4,
	'q': 10,
	'r': 1,
	's': 1,
	't': 1,
	'u': 2,
	'v': 5,
	'w': 4,
	'x': 8,
	'y': 3,
	'z': 10}

# Functions
# 

def unique(seq):
	seen = set()
	return [ x for x in seq if str( x ) not in seen and not seen.add( str( x ) )]

# Check if new word will fit
def check_spot(x, y, length, direction):
	al = length
	ax = x
	ay = y

	if board[x][y] != ' ':
		return False 
	elif direction == HORIZONTAL:
		while al > 0:
			if board[ay][ax] == ' ':
				al -= 1
			ax += 1
			# Too long
			if ax >= 15:
				return False

		# Make sure word touches other letters
		# 
		# Word intersects other letter(s)
		if ax > x + length:
			return True
		# Touches on left
		if (x > 0) and (board[y][x-1] != ' '):
			return True
		# Touches on right
		if (x+length < 14) and (board[y][x+length] != ' '):
			return True
		for i in range(x,x+length):
			# Touches on top
			if(y > 0) and (board[y-1][i] != ' '):
				return True
			# Touches on bottom
			if (y < 14) and (board[y+1][i] != ' '):
				return True
	elif direction == VERTICAL:
		while al > 0:
			if board[ay][ax] == ' ':
				al -= 1
			ay += 1
			# Too long
			if ay >= 15:
				return False
		# Make sure word touches other letters
		# 
		# Word intersects other letter(s)
		if ay > y+length:
			return True
		# Touches on top
		if (y > 0) and (board[y-1][x] != ' '):
			return True
		# Touches on bottom
		if (y+length < 14) and (board[y+length][x] != ' '):
			return True
		for i in range(y,y+length):
			# Touches on left
			if (x > 0) and (board[i][x-1] != ' '):
				return True
			# Touches on right
			if (x < 14) and (board[i][x+1] != ' '):
				return True
	# Bad spot
	return False

def get_full_word(x, y, string, direction):
	word = ""
	length = len(string)
	strpos = 0

	# Special case for existing spaces
	if board[y][x] != ' ':
		return (board[y][x], x, y)

	if direction == HORIZONTAL:
		# Scan left
		x_start = x
		while x_start > 0:
			if board[y][x_start-1] != ' ':
				x_start -= 1
			else:
				break
		# Scan right and build word
		x_end = x_start
		while x_end < 15:
			if board[y][x_end] != ' ':
				word += board[y][x_end]
			elif strpos == length:
				break
			else:
				word += string[strpos]
				strpos += 1
			x_end += 1
		return (word, x_start, x_end)
	elif direction == VERTICAL:
		# Scan up
		y_start = y;
		while y_start > 0:
			if board[y_start-1][x] != ' ':
				y_start -= 1
			else:
				break
		# Scan down and build word
		y_end = y_start
		while y_end < 15:
			if board[y_end][x] != ' ':
				word += board[y_end][x]
			elif strpos == length:
				break
			else:
				word += string[strpos]
				strpos += 1
			y_end += 1
		return (word, y_start, y_end)

def calculate_score(x, y, word, direction):
	used_count = 0
	score = 0
	score_mult = 1
	secondary_score = 0

	if direction == HORIZONTAL:
		for i in range(0,len(word)):
			# Tile we placed
			if board[y][x+i] == ' ':
				used_count += 1
				score += letter_value[word[i]] * letter_mult[y][x+i]
				score_mult *= word_mult[y][x+i]

				# Check new veritcal words
				(vert_word, y_start, y_end) = get_full_word(x+i, y, word[i], VERTICAL)
				if len(vert_word) > 1:
					vert_score = 0
					for j in range(0,len(vert_word)):
						vert_score += letter_value[vert_word[j]]
					vert_score += letter_value[word[i]] * (letter_mult[y][x+i]-1)
					secondary_score += (vert_score * word_mult[y][x+i])

			# Existing tile
			else:
				score += letter_value[word[i]]
	if direction == VERTICAL:
		for i in range(0,len(word)):
			# Tile we placed
			if board[y+i][x] == ' ':
				used_count += 1
				score += letter_value[word[i]] * letter_mult[y+i][x]
				score_mult *= word_mult[y+i][x]

				# Check new horrizontal words
				(horz_word, x_start, x_end) = get_full_word(x, y+i, word[i], HORIZONTAL)
				if len(horz_word) > 1:
					horz_score = 0
					for j in range(0,len(horz_word)):
						horz_score += letter_value[horz_word[j]]
					horz_score += letter_value[word[i]] * (letter_mult[y+i][x]-1)
					secondary_score += (horz_score * word_mult[y+i][x])
			# Existing tile
			else:
				score += letter_value[word[i]]

	return (score * score_mult) + (35 if used_count == 7 else 0) + secondary_score

# Main
# 

def solve():

	# Generate tile permutations
	# 
	# (Better way of doing this?)

	tiles_perm = [
		set(),
		set(),
		set(),
		set(),
		set(),
		set(),
		set()]
	if '*' in tiles:
		for char in "abcdefghijklmnopqrstuvwxyz":
			tiles_perm[0].update(itertools.permutations(tiles.replace('*', char), 1))
			tiles_perm[1].update(itertools.permutations(tiles.replace('*', char), 2))
			tiles_perm[2].update(itertools.permutations(tiles.replace('*', char), 3))
			tiles_perm[3].update(itertools.permutations(tiles.replace('*', char), 4))
			tiles_perm[4].update(itertools.permutations(tiles.replace('*', char), 5))
			tiles_perm[5].update(itertools.permutations(tiles.replace('*', char), 6))
			tiles_perm[6].update(itertools.permutations(tiles.replace('*', char), 7))
	else:
		tiles_perm[0].update(itertools.permutations(tiles, 1))
		tiles_perm[1].update(itertools.permutations(tiles, 2))
		tiles_perm[2].update(itertools.permutations(tiles, 3))
		tiles_perm[3].update(itertools.permutations(tiles, 4))
		tiles_perm[4].update(itertools.permutations(tiles, 5))
		tiles_perm[5].update(itertools.permutations(tiles, 6))
		tiles_perm[6].update(itertools.permutations(tiles, 7))

	valid_words = []

	for length in range(0,7):
		# Horizontal pass
		print("Checking length %i, horizontal" % (length + 1))
		for y in range(0,15):
			for x in range(0,15-length):
				if check_spot(x, y, length+1, HORIZONTAL):
					# Valid starting spot, check every permutation
					for word in tiles_perm[length]:
						# Check new horizontal word
						(new_word, x_start, x_end) = get_full_word(x, y, word, HORIZONTAL)
						if new_word in wordlist:
							# Check each new vertical word
							valid = True
							for i in range(x_start, x_end):
								(vert_word, y_start, y_end) = get_full_word(i, y, new_word[i-x_start], VERTICAL)
								if not(vert_word in wordlist) and len(vert_word) > 1:
									valid = False
									break
							if valid:
								valid_words.append([new_word, x_start, y, HORIZONTAL, 
									calculate_score(x_start, y, new_word, HORIZONTAL)])
		# Vertical pass
		print("Checking length %i, vertical" % (length + 1))
		for y in range(0,15-length):
			for x in range(0,15):
				if check_spot(x, y, length+1, VERTICAL):
					# Valid starting spot, check every permutation
					for word in tiles_perm[length]:
						(new_word, y_start, y_end) = get_full_word(x, y, word, VERTICAL)
						if new_word in wordlist:
							# Check each new horizontal word
							valid = True
							for i in range(y_start, y_end):
								(horz_word, x_start, x_end) = get_full_word(x, i, new_word[i-y_start], HORIZONTAL)
								if not(horz_word in wordlist) and len(horz_word) > 1:
									valid = False
									break
							if valid:
								valid_words.append([new_word, x, y_start, VERTICAL,
									calculate_score(x, y_start, new_word, VERTICAL)])


	# Print words sorted by score
	for word in sorted(unique(valid_words), key=lambda word: word[4]):
		if word[3] == HORIZONTAL:
			print("Horz: x: %2i  y: %2i score: %i word: %s" % (word[1]+1, word[2]+1, word[4], word[0]))
		if word[3] == VERTICAL:
			print("Vert: x: %2i  y: %2i score: %i word: %s" % (word[1]+1, word[2]+1, word[4], word[0]))
	return valid_words

if __name__ == "__main__":
    solve()