import random
from random import randint

deck = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

def roll_dice():
	dice_1 = randint(1,6)
	dice_2 = randint(1,6)
	return (dice_1,dice_2)

def shuffle_chance():
	random.shuffle(deck)

def get_chance_card(cur_pos):
	#Define chance cards here, and draw from them.
	#After drawing the card is placed at the back of
	#'Deck' again.
	card = deck[0]
	print(deck)
	
	for i in range(len(deck)-1):
		deck[i] = deck[i+1]
	deck[15] = card	
	print(deck)

	cards = {
	1:  ('Advance to Go', 0),
	2:  ('Advance to Illinois Ave', 0),
	3:  ('Advance to St. Charles Place', 0),
	4:  ('Advance to Nearest Utility', 0),
	5:  ('Advance to nearest Railroad', 0),
	6:  ('Bank Pays You 50', 0),
	7:  ('Get out of Jail Free', 0),
	8:  ('Go Back 3 Spaces', 0),
	9:  ('Go to Jail', 0),
	10: ('Pay Repairs', 0),
	11: ('Pay tax of 15', 0),
	12: ('Go to Reading Railroad', 0),
	13: ('Go to Boardwalk', 0),
	14: ('Pay each player 50', 0),
	15: ('Collect 150', 0),
	16: ('Collect 100', 0),
	}

	cards[card] = (cards[card][0], cards[card][1]+1)

	position = handle_chance(card, cur_pos)

	return position


#Will handle the chance card according to its rule
#will call get chance card and process accordingly
#Takes current position to move backward forward if necessary
#NOTE: Get out of jail is IGNORED. 
def handle_chance(card,pos):
	#Go
	if card == 1:
		return 40
	#Illinois
	elif card == 2:
		return 25
	#St Charles
	elif card == 3:
		return 12
	#Nearest Utility
	elif card == 4:
		electric = 13 - pos
		water = 29 - pos
		utilities = [electric, water]
		return min(utilities)
	#Nearest Railroad
	elif card == 5:
		reading_pos = 6 - pos
		penn_pos = 16 - pos
		bao_pos = 26 - pos
		sho_pos = 26 - pos
		trains = [reading_pos, penn_pos, bao_pos, sho_pos]
		return min(trains)
	#Get 50
	elif card == 6:
		#NOT IMPLEMENTED
		return 0
	#Get out of Jail Free
	elif card == 7:
		#NOT IMPLEMENTED
		return 0
	#Go Back 3
	elif card == 8:
		temp_pos = position-3
		temp_mod = temp_pos%40
		if temp_mod == 0:
			return 40
		else:
			return temp_mod
	#Go to Jail
	elif card == 9:
		return 11
	#Pay Repairs
	elif card == 10:
		#NOT IMPLEMENTED
		return 0
	#Pay 15
	elif card == 11:
		#NOT IMPLEMENTED
		return 0
	#Reading Railroad
	elif card == 12:
		return 6
	#Boardwalk
	elif card == 13:
		return 40
	#Pay each player 50
	elif card == 14:
		#NOT IMPLEMENTED
		return 0
	#Collect 150
	elif card == 15:
		#NOT IMPLEMENTED
		return 0
	#Collect 100
	elif card == 16:
		#NOT IMPLEMENTED
		return 0

	return 0


def play_monopoly():
	print(deck)
	shuffle_chance()
	print(deck)
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
	for i in range(10):
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
		#Check if jail and increase accordingly
		if is_jail(board[cur_pos][0]):
			cur_pos = 10
			curr_landings = board[cur_pos][1]+1
			board[cur_pos] = (board[cur_pos][0], curr_landings)
			continue
		#check if chance and increase counters with new position
		#of chance card, if any
		if cur_pos == 8 or cur_pos == 23 or cur_pos == 37:
			position = get_chance_card(cur_pos)
			if position != 0:
				cur_pos = position
				curr_landings = board[cur_pos][1]+1
				board[cur_pos] = (board[cur_pos][0], curr_landings)
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
