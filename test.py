import scrabble
import pickle
import cProfile

data = {'tiles': 'htmohoc', 'board': [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'y', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p', 'r', 'i', 'g'], [' ', ' ', ' ', 'a', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'e', ' ', ' ', ' '], [' ', ' ', 'e', 'm', 'o', 't', 'i', 'v', 'e', ' ', ' ', 't', ' ', 'g', ' '], [' ', ' ', ' ', 'u', ' ', 'i', ' ', ' ', ' ', ' ', 'f', 'u', 'l', 'l', ' '], [' ', ' ', ' ', 'n', ' ', 't', ' ', 'q', 'u', 'e', 'a', 'n', ' ', 'e', ' '], [' ', ' ', ' ', ' ', ' ', 'a', 'h', 'a', ' ', 'n', ' ', 'i', ' ', 'e', ' '], [' ', ' ', ' ', ' ', ' ', 'n', 'a', 'n', ' ', 'j', ' ', 'a', ' ', 'd', ' '], [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'a', ' ', 'o', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', 'r', 'u', 't', ' ', 'y', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', 'a', ' ', 's', 'e', 'e', 'r', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', 'r', 'e', 'f', 'e', 'd', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'v', 'i', 's', 'e', 'e', 'd', ' ', ' ']]}

save_file = open("lor.pkl", 'rb')
data = pickle.load(save_file)

solver = scrabble.Solver(scrabble.WORDSWITHFRIENDS)
solver.board = data['board']

# print(solver.solve('htmohoc'))

cProfile.run("solver.solve(data['tiles'])")

# a = solver._Solver__get_frame(2, 14, 5, 0)
# print(a)
# print(solver._Solver__fill_frame(a, "99998"))