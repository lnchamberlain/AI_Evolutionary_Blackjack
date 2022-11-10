
#################################################################################
# 
# Evolutionary Blackjack
# Semester Project for CSCE A405 AI
# Austin Edwards, Tuva Granoien, and Logan Chamberlain
# Fall 2022
#
#
################################################################################

import Player
import random
import sys



#NOTE: The dealer has an infinite deck for the purposes of our algorithm

#Proven strategy tables data sourced from: https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c
#MOVES ARE INDEX by TABLE[PLAYER SUM][DEALER CARD]
PROVEN_STRATEGY_TABLE_HARD_HAND = {20:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"}, 
                              19:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                              18:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                              17:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                              16:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              15:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              14:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"S", 9:"H", 10:"H", "Ace":"H"},
                              13:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              12:{2:"H", 3:"H", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              11:{2:"D", 3:"D", 4:"D", 5:"D", 6:"D", 7:"D", 8:"D", 9:"D", 10:"D", "Ace":"D"},
                              10:{2:"D", 3:"D", 4:"D", 5:"D", 6:"D", 7:"D", 8:"D", 9:"D", 10:"S", "Ace":"S"},
                              9:{2:"H", 3:"D", 4:"D", 5:"D", 6:"D", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"}, 
                              8:{2:"H", 3:"H", 4:"H", 5:"H", 6:"H", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              7:{2:"H", 3:"H", 4:"H", 5:"H", 6:"H", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              6:{2:"H", 3:"H", 4:"H", 5:"H", 6:"H", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              5:{2:"H", 3:"H", 4:"H", 5:"H", 6:"H", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"}}
                             
PROVEN_STRATEGY_TABLE_SOFT_HAND = {"A-9":{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"}, 
                                   "A-8":{2:"S", 3:"S", 4:"S", 5:"S", 6:"D", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                                   "A-7":{2:"D", 3:"D", 4:"D", 5:"D", 6:"D", 7:"S", 8:"S", 9:"H", 10:"H", "Ace":"H"},
                                   "A-6":{2:"H", 3:"D", 4:"D", 5:"D", 6:"D", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "A-5":{2:"H", 3:"H", 4:"D", 5:"D", 6:"D", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "A-4":{2:"H", 3:"H", 4:"D", 5:"D", 6:"D", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "A-3":{2:"H", 3:"H", 4:"H", 5:"D", 6:"D", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "A-2":{2:"H", 3:"H", 4:"H", 5:"D", 6:"D", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"}}

PROVEN_STRATEGY_TABLE_PAIR = {"A-A":{2:"P", 3:"P", 4:"P", 5:"P", 6:"P", 7:"P", 8:"P", 9:"P", 10:"P", "Ace":"P"}, 
                                   "T-T":{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                                   "9-9":{2:"P", 3:"P", 4:"P", 5:"P", 6:"P", 7:"S", 8:"P", 9:"P", 10:"S", "Ace":"S"},
                                   "8-8":{2:"P", 3:"P", 4:"P", 5:"P", 6:"P", 7:"P", 8:"P", 9:"P", 10:"P","Ace":"P"},
                                   "7-7":{2:"P", 3:"P", 4:"P", 5:"P", 6:"P", 7:"P", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "6-6":{2:"P", 3:"P", 4:"P", 5:"P", 6:"P", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "5-5":{2:"D", 3:"D", 4:"D", 5:"D", 6:"D", 7:"D", 8:"D", 9:"D", 10:"H", "Ace":"H"},
                                   "4-4":{2:"H", 3:"H", 4:"H", 5:"P", 6:"P", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "3-3":{2:"P", 3:"P", 4:"P", 5:"P", 6:"P", 7:"P", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                                   "2-2":{2:"P", 3:"P", 4:"P", 5:"P", 6:"P", 7:"P", 8:"H", 9:"H", 10:"H", "Ace":"H"}}
                                   
STRATEGY_TABLE_PAIR = [] 
STRATEGY_TABLE_SOFT_HAND = []
STRATEGY_TABLE_HARD_HAND = []
POOL = 500 #Amount of money player starts with
BET_AMOUNT = 2 #Bet $2 per hand
DECK = []
LIMIT = 1000 #Each generation plays until their Pool is 0 or Limit is reached


#Returns a random card from the populated deck
def get_random_card():
    if(len(DECK) > 52):
        print("Error: populate deck prior to drawing card")
        return None
    return DECK[random.randint(0, len(DECK))]


#Returns an array of the player's cards and the dealers visible card and not visible card in the form [[Player Card 1, Player Card 2], [Dealer Visible Card, Dealer not Visible Card]]. Example: [[]"7 of hearts", "King of Spades"], []"Jack of Diamonds", "3 of Clubs"]]
def deal():
    player_hand = [get_random_card(), get_random_card()]
    dealer_card = [get_random_card(), get_random_card()]
    return [player_hand, dealer_card]
 

#Checks for the condition wherein a player is drawn an Ace and a 10 card (10 or any face card), resulting in an immediate Blackjack. Different conditions exist for player and dealers having a natural, returns None if not applicable, return a string describing who won is applicable. 
def check_naturals(deal):
    player_hand = deal[0]
    dealer_hand = deal[1]
    player_val_one = get_card_value(player_hand[0])
    player_val_two = get_card_value(player_hand[1])
    player_sum = player_val_one + player_val_two
    dealer_val_one = get_card_value(player_hand[0])
    dealer_val_two = get_card_value(player_hand[1])
    dealer_sum = dealer_val_one + dealer_val_two
    if(player_sum == 21 and dealer_sum != 21):
        return "Player"
    if(player_sum != 21 and dealer_sum == 21):
        return "Dealer"
    if(player_sum == 21 and dealer_sum == 21):
        return "Tie"
    else:
        return None



#Takes a card in the form "Value of Suit" and returns an integer of the value unless Ace. Example: "7 of Hearts" -> 7, "King of Spades" -> 10, "Ace of Clubs" -> "Ace"
def get_card_value(card):
    card = card.split("of")
    value = card[0]
    if(value == "Ace"):
        #Some games have an Ace be value 1 or 11
        return "Ace"
    if(value == "King" or value == "Queen" or value == "Jack"):
        return 10
    else:
        return int(value)

#Fills in the global deck variable with 52 strings of the form "value of suit"
def populate_deck():
    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ROYALTY_AND_ACE = ["Ace", "King", "Queen", "Jack"]
    for i in range(2,11):
        for SUIT in SUITS: 
            DECK.append(str(i) + " of " + SUIT)
    for FACE in ROYALTY_AND_ACE:
        for SUIT in SUITS:
            DECK.append(FACE + " of " + SUIT)

#ACTION: Do nothing? Not sure if I read the rules right 
def stand():
    return None

#ACTION: player asks for a new card to be added to their hand
def hit(player_hand):
    player_hand.append(get_random_card())
    return player_hand

#ACTION: 
def double_down():
    print("STUB")

def split():
    print("STUB")

#Checks if player has exceeded 21, returns "BUST" if so and returns the total value of their cards if not
def check_player_hand(player_hand):
    total = 0
    for card in player_hand:
        if card != "Ace":
            total += get_card_value(card)
        else:
            #If Ace, use 11 unless that makes the player go over, then use 1
            if(total + 11 > 21):
                total += 1
            else:
                total += 11
    if(total > 21):
        return "BUST"
    else:
        return total


#Returns a random move depending on the mode (hard hard, soft hand, and pair)
def generate_random_move(mode):
    if(mode == "Hard Hand" or mode == "Soft Hand"):
        move = random.choice(["S", "H", "D"]) 
    if(mode == "Pair"):
        move = random.choice(["P", "S", "H", "D"])
    return move

#Creates an array of Player objects with randomly filled strategy tables. Takes in an integer denoting how many players to create
def generate_inital_population(num_players):
    initial_population = []
    for i in range(num_players):
        initial_population.append(Player.player())

    for player in initial_population:
        #Fill Hard hand table
        for row in player.STRATEGY_TABLE_HARD_HAND:        
            for elem in player.STRATEGY_TABLE_HARD_HAND[row]:
                player.STRATEGY_TABLE_HARD_HAND[row][elem] = generate_random_move("Hard Hand")
        #Fill in Soft hand table
        for row in player.STRATEGY_TABLE_SOFT_HAND:        
            for elem in player.STRATEGY_TABLE_SOFT_HAND[row]:
                player.STRATEGY_TABLE_SOFT_HAND[row][elem] = generate_random_move("Soft Hand")
        #Fill in pairs tables
        for row in player.STRATEGY_TABLE_PAIR:        
            for elem in player.STRATEGY_TABLE_PAIR[row]:
                player.STRATEGY_TABLE_PAIR[row][elem] = generate_random_move("Pair")

    return initial_population

def main():
    populate_deck()
    generate_inital_population(20)
    



if __name__ == "__main__":
    main()