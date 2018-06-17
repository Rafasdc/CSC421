from random import randint


def roll_dice():
	dice_1 = randint(1,6)
	dice_2 = randint(1,6)
	return (dice_1,dice_2)

def get_chance_card():
	#Define chance cards here, and draw from them.
	#After drawing the card is placed at the back of
	#'Deck' again.

	deck = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] 

	cards = {
	1:  ('Card', 0),
	2:  ('Card', 0),
	3:  ('Card', 0),
	4:  ('Card', 0),
	5:  ('Card', 0),
	6:  ('Card', 0),
	7:  ('Card', 0),
	8:  ('Card', 0),
	9:  ('Card', 0),
	10: ('Card', 0),
	11: ('Card', 0),
	12: ('Card', 0),
	13: ('Card', 0),
	14: ('Card', 0),
	15: ('Card', 0),
	16: ('Card', 0),
	}


	return 1

def play_monopoly():
	#Create each monopoly square and hold it
	board = {
	1: ('Go',0),
	2: ('Mediterranean', 0),
	3: ('Community Chest',0),
	4: ('Baltic',0),
	5: ('Income Tax',0),
	6: ('Reading Railroad',0),
	7: ('Oriental Avenue',0),
	8: ('Chance',0),
	9: ('Vermont',0),
	10: ('Connecticut',0),
	11:('Jail',0),
	12:('St. Charles',0),
	13:('Electric Company',0),
	14:('States Avenue',0),
	15:('Virginia Avenue',0),
	16:('Pennsylvania Railroad',0),
	17:('St. James',0),
	18:('Commnity Chest',0),
	19:('Teneesee',0),
	20:('New York',0),
	21:('Free Parking',0),
	22:('Kentucky',0),
	23:('Chance',0),
	24:('Indiana Avenue',0),
	25:('Illinois Avenue',0),
	26:('B.A.O Railroad',0),
	27:('Atlantic',0),
	28:('Venthos',0),
	29:('Water Works',0),
	30:('Maine',0),
	31:('Go To Jail',0),
	32:('Pacific',0),
	33:('North Carolina',0),
	34:('Community Chest',0),
	35:('Pennsylvania',0),
	36:('Short Line',0),
	37:('Chance',0),
	38:('Park Place',0),
	39:('Luxury Tax',0),
	40:('Boardwalk',0),
	}

	def is_jail(space):
		return space == 'Go To Jail'
	

	#Create cur_pos with pos 0 to represent Go
	cur_pos = 0
	#Roll the dice n times
	for i in range(1000):
		#Roll the dices, store positions
		#Mod the position to stay within 40 squares
		dice1, dice2 = roll_dice()
		cur_pos += (dice1 + dice2)
		cur_pos %= 40
		if (cur_pos == 0):
			cur_pos = 40
		print(cur_pos)
		#Increase counter
		curr_landings = board[cur_pos][1]+1
		#Replace tuple with new increased counter
		board[cur_pos] = (board[cur_pos][0], curr_landings)
		print(board[cur_pos])
		if is_jail(board[cur_pos][0]):
			cur_pos = 10
			curr_landings = board[cur_pos][1]+1
			board[cur_pos] = (board[cur_pos][0], curr_landings)
			continue

		#Roll again if doubles
		#NOTE: 3 consecutive will NOT yield jail
		while (dice1 == dice2):
			dice1, dice2 = roll_dice()
			cur_pos += (dice1 + dice2)
			cur_pos %= 40
			if (cur_pos == 0):
				cur_pos = 40
			print(cur_pos)
			curr_landings = board[cur_pos][1]+1
			board[cur_pos] = (board[cur_pos][0], curr_landings)
			print(board[cur_pos])
			if is_jail(board[cur_pos][0]):
				cur_pos = 10
				curr_landings = board[cur_pos][1]+1
				board[cur_pos] = (board[cur_pos][0], curr_landings)
				break
		
	#return the final board with all the tallies
	return board

result = play_monopoly()
print(result)
