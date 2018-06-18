import random
from random import randint

deck = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

def roll_dice():
	dice_1 = randint(1,6)
	dice_2 = randint(1,6)
	return (dice_1,dice_2)

def shuffle_chance():
	random.shuffle(deck)


def play_monopoly():
	turn = 1
	global player_1
	global player_2
	player_1 = 500
	player_2 = 500
	print(player_1)
	print(player_2)
	shuffle_chance()
	#Create each monopoly square and hold it
	#Board change order is now, Name, Landings, Owner, Cost, Rent
	#Owner of -1 represents not ownable
	#0 = Unowned, 1 or 2 owned by player 1 or 2 respectively
	#Railroads, and Companies have fixed rent of 25
	#DOES NOT account for multiple colors owned
	board = {
	1: ('Go',0,-1,0,0),
	2: ('Mediterranean', 0,0,60,2),
	3: ('Community Chest',0,-1,0,0),
	4: ('Baltic',0,0,60,4),
	5: ('Income Tax',0,-1,200,200),
	6: ('Reading Railroad',0,0,200,25),
	7: ('Oriental Avenue',0,0,100,6),
	8: ('Chance',0,-1,0,0),
	9: ('Vermont',0,0,100,6),
	10: ('Connecticut',0,0,120,8),
	11:('Jail',0,-1,0,0),
	12:('St. Charles',0,0,140,10),
	13:('Electric Company',0,0,150,25),
	14:('States Avenue',0,0,140,10),
	15:('Virginia Avenue',0,0,160,12),
	16:('Pennsylvania Railroad',0,0,200,25),
	17:('St. James',0,0,180,14),
	18:('Commnity Chest',0,-1,0,0),
	19:('Teneesee',0,0,180,14),
	20:('New York',0,0,200,16),
	21:('Free Parking',0,-1,0,0),
	22:('Kentucky',0,0,220,18),
	23:('Chance',0,-1,0,0),
	24:('Indiana Avenue',0,0,220,19),
	25:('Illinois Avenue',0,0,240,20),
	26:('B.A.O Railroad',0,0,200,25),
	27:('Atlantic',0,0,260,22),
	28:('Venthos',0,0,260,22),
	29:('Water Works',0,0,150,25),
	30:('Maine',0,0,280,24),
	31:('Go To Jail',0,-1,0,0),
	32:('Pacific',0,0,300,26),
	33:('North Carolina',0,0,300,26),
	34:('Community Chest',0,-1,0,0),
	35:('Pennsylvania',0,0,320,28),
	36:('Short Line',0,0,200,25),
	37:('Chance',0,-1,0,0),
	38:('Park Place',0,0,350,35),
	39:('Luxury Tax',0,-1,75,75),
	40:('Boardwalk',0,0,400,50),
	}

	def get_chance_card(cur_pos,player):
		#Define chance cards here, and draw from them.
		#After drawing the card is placed at the back of
		#'Deck' again.
		card = deck[0]
		#print(deck)
		
		for i in range(len(deck)-1):
			deck[i] = deck[i+1]
		deck[15] = card	
		#print(deck)

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

		position = handle_chance(card, cur_pos,player)

		return position


	#Will handle the chance card according to its rule
	#will call get chance card and process accordingly
	#Takes current position to move backward forward if necessary
	#NOTE: Get out of jail is IGNORED. 
	def handle_chance(card,pos,player):
		global player_1
		global player_2
		#Go
		if card == 1:
			give_go(player)
			return 1
		#Illinois
		elif card == 2:
			land_on_property(25,player)
			return 25
		#St Charles
		elif card == 3:
			land_on_property(12,player)
			return 12
		#Nearest Utility
		elif card == 4:
			electric = 13 - pos
			water = 29 - pos
			utilities = [electric, water]
			minimum =  min(utilities)
			if minimum == electric:
				land_on_property(13,player)
				return 13
			else:
				land_on_property(29,player)
				return 29
		#Nearest Railroad
		elif card == 5:
			reading_pos = 6 - pos
			penn_pos = 16 - pos
			bao_pos = 26 - pos
			sho_pos = 36 - pos
			trains = [reading_pos, penn_pos, bao_pos, sho_pos]
			minimum = min(trains)
			if minimum == reading_pos:
				land_on_property(6,player)
				return 6
			elif minimum == penn_pos:
				land_on_property(16,player)
				return 16
			elif minimum == bao_pos:
				land_on_property(26,player)
				return 26
			elif minimum == sho_pos:
				land_on_property(36,player)
				return 36
		#Get 50
		elif card == 6:
			if player == 1:
				player_1 += 50
			else:
				player_2 += 50
			return 0
		#Get out of Jail Free
		elif card == 7:
			#NOT IMPLEMENTED
			return 0
		#Go Back 3
		elif card == 8:
			temp_pos = pos-3
			temp_mod = temp_pos%40
			if temp_mod == 0:
				land_on_property(40,player)
				return 40
			else:
				land_on_property(temp_mod,player)
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
			if player == 1:
				player_1 -= 15
			else:
				player_2 -= 15
			return 0
		#Reading Railroad
		elif card == 12:
			land_on_property(12,player)
			return 6
		#Boardwalk
		elif card == 13:
			land_on_property(40,player)
			return 40
		#Pay each player 50
		elif card == 14:
			if player == 1:
				player_1 -= 50
				player_2 += 50
			else:
				player_2 -= 50
				player_1 += 50
			return 0
		#Collect 150
		elif card == 15:
			if player == 1:
				player_1 += 150
			else:
				player_2 += 150
			return 0
		#Collect 100
		elif card == 16:
			if player == 1:
				player_1 += 100
			else:
				player_2 += 100
			return 0

		return 0

	def is_jail(space):
		return space == 'Go To Jail'

	def give_go(player):
		global player_1
		global player_2
		if player == 1:
			player_1 += 200
			print("Player 1 receives 200 for passing Go")
			print("Player 1 money is now: " + str(player_1))
		else:
			player_2 += 200
			print("Player 2 receives 200 for passing Go")
			print("Player 2 money is now: " + str(player_2))
	def pay_rent(space,player_to_pay):
		global player_1
		global player_2
		rent = board[space][4]
		if player_to_pay == 1:
			player_1 -= rent
			player_2 += rent
			print("Player 1 pays Player 2, " + str(rent) + "for landing on " + board[space][0])
			print("Player 1 money is now: " + str(player_1))
		else:
			player_2 -= rent
			player_1 += rent
			print("Player 2 pays Player 1, " + str(rent) + "for landing on " + board[space][0])
			print("Player 2 money is now: " + str(player_2))

	def check_tax(space,player_to_pay):
		global player_1
		global player_2
		#income Tax
		if space == 5:
			if player_to_pay == 1:
				player_1 -= board[space][4]
				print("Player 1 pays Income Tax of 200")
			else:
				player_2 -= board[space][4]
				print("Player 2 pays Income Tax of 200")
		#Luxury Tax
		elif space == 39:
			if player_to_pay == 1:
				player_1 -= board[space][4]
				print("Player 1 pays Luxury Tax of 75")
				print("Player 1 money is now: " + str(player_1))
			else:
				player_2 -= board[space][4]
				print("Player 2 pays Income Tax of 75")
				print("Player 2 money is now: " + str(player_2))

	def land_on_property(space, player):
		global player_1
		global player_2
		if board[space][2] == -1:
			check_tax(space, player)

		#Handle rent payment
		if board[space][2] > 0 and board[space][2] != player:
				pay_rent(space,player)
				return

		#Add an extra rich flag
		#In Which a player will always buy if money is over 400
		rich = False
		if player == 1:
			if  player_1 > 400:
				rich = True
		elif player == 2:
			if player_2 > 400:
				rich = True
		#Handle to Buy
		#Will randombly decide to buy or not to buy
		if board[space][2] != -1:
			to_buy = randint(1,2)
			if to_buy == 1 or rich:
				if board[space][2] == 0:
					if player == 1:
						if player_1 >= board[space][3]:
							player_1 -= board[space][3]
							board[space] = (board[space][0],board[space][1],player,board[space][3],board[space][4])
							print("Player 1 buys property " + board[space][0])
							print("Player 1 money is now: " + str(player_1))
					else:
						if player_2 >= board[space][3]:
							player_2 -= board[space][3]
							board[space] = (board[space][0],board[space][1],player,board[space][3],board[space][4])
							print("Player 2 buys property " + board[space][0])
							print("Player 2 money is now: " + str(player_2))
			elif to_buy == 2:
				print("Player " + str(player) + " decides not to buy property " + board[space][0])

	
	def check_bankrupt():
		if player_1 < 0:
			return 2
		elif player_2 <0:
			return 1
		else:
			return 0

	def get_winner():
		if player_1 > player_2:
			print("Player 1 wins with $" + str(player_1) + " over $" + str(player_2) + " of player 2.")
		else:
			print("Player 2 wins with $" + str(player_2) + " over $" + str(player_1) + " of player 1.")


	#Create cur_pos with pos 0 to represent Go
	cur_pos = [0,1,1]
	#Roll the dice n times
	for i in range(200):
		#Roll the dices, store positions
		#Mod the position to stay within 40 squares
		dice1, dice2 = roll_dice()
		cur_pos[turn] += (dice1 + dice2)
		print("Player " + str(turn) + " rolls " + str(dice1+dice2))
		if cur_pos[turn] > 40:
			give_go(turn)
		cur_pos[turn] %= 40
		if (cur_pos[turn] == 0):
			cur_pos[turn] = 40
		print("Player " + str(turn) + " lands on " + board[cur_pos[turn]][0])
		land_on_property(cur_pos[turn],turn)
		#print(cur_pos[turn])
		#Increase counter
		curr_landings = board[cur_pos[turn]][1]+1
		#Replace tuple with new increased counter
		board[cur_pos[turn]] = (board[cur_pos[turn]][0], curr_landings,board[cur_pos[turn]][2],board[cur_pos[turn]][3],board[cur_pos[turn]][4])
		#print(board[cur_pos[turn]])
		#Check if jail and increase accordingly
		if is_jail(board[cur_pos[turn]][0]):
			cur_pos[turn] = 10
			curr_landings = board[cur_pos[turn]][1]+1
			board[cur_pos[turn]] = (board[cur_pos[turn]][0], curr_landings,board[cur_pos[turn]][2],board[cur_pos[turn]][3],board[cur_pos[turn]][4])
			continue
		#check if chance and increase counters with new position
		#of chance card, if any
		if cur_pos[turn] == 8 or cur_pos[turn] == 23 or cur_pos[turn] == 37:
			position = get_chance_card(cur_pos[turn],turn)
			if position != 0:
				cur_pos[turn] = position
				curr_landings = board[cur_pos[turn]][1]+1
				board[cur_pos[turn]] = (board[cur_pos[turn]][0], curr_landings,board[cur_pos[turn]][2],board[cur_pos[turn]][3],board[cur_pos[turn]][4])
		#Roll again if doubles
		#NOTE: 3 consecutive will NOT yield jail
		while (dice1 == dice2):
			dice1, dice2 = roll_dice()
			print("Player " + str(turn) + " rolls again" + str(dice1+dice2))
			cur_pos[turn] += (dice1 + dice2)
			cur_pos[turn] %= 40
			if (cur_pos[turn] == 0):
				cur_pos[turn] = 40
			print("Player " + str(turn) + " lands on " + board[cur_pos[turn]][0])
			land_on_property(cur_pos[turn],turn)
			#print(cur_pos[turn])
			curr_landings = board[cur_pos[turn]][1]+1
			board[cur_pos[turn]] = (board[cur_pos[turn]][0], curr_landings,board[cur_pos[turn]][2],board[cur_pos[turn]][3],board[cur_pos[turn]][4])
			#print(board[cur_pos[turn]])
			if is_jail(board[cur_pos[turn]][0]):
				cur_pos[turn] = 10
				curr_landings = board[cur_pos[turn]][1]+1
				board[cur_pos[turn]] = (board[cur_pos[turn]][0], curr_landings,board[cur_pos[turn]][2],board[cur_pos[turn]][3],board[cur_pos[turn]][4])
				break
			#check if chance and increase counters with new position
			#of chance card, if any
			if cur_pos[turn] == 8 or cur_pos[turn] == 23 or cur_pos[turn] == 37:
				position = get_chance_card(cur_pos[turn],turn)
				if position != 0:
					cur_pos[turn] = position
					curr_landings = board[cur_pos[turn]][1]+1
					board[cur_pos[turn]] = (board[cur_pos[turn]][0], curr_landings,board[cur_pos[turn]][2],board[cur_pos[turn]][3],board[cur_pos[turn]][4])
		if check_bankrupt == 1:
			print("Player 1 wins the game")
			break
		elif check_bankrupt == 2:
			print("Player 2 wins the game")
			break
		if turn == 1:
			turn = 2
		else:
			turn = 1
		
	#return the final board with all the tallies
	get_winner()
	return board

result = play_monopoly()

