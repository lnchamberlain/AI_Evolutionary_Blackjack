
#################################################################################
# 
# Evolutionary Blackjack
# Semester Project for CSCE A405 AI
# Austin Edwards, Tuva Granoien, and Logan Chamberlain
# Fall 2022
#
#
################################################################################

import time 
import random



#NOTE: The dealer has an infinite deck for the purposes of our algorithm


PROVEN_STRATEGY_TABLE = {} #This is the end goal
STRATEGY_TABLE = {}
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



#Takes a card in the form "Value of Suit" and returns an integer of the value. Example: "7 of Hearts" -> 7, "King of Spades" -> 10, "Ace of Clubs" -> 11
def get_card_value(card):
    card = card.split("of")
    value = card[0]
    if(value == "Ace"):
        #Some games have an Ace be value 1
        return 11
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


#Checks if player has exceeded 21, returns "BUST" if so and returns the total value of their cards if not
def check_player_hand(player_hand):
    total = 0
    for card in player_hand:
        total += get_card_value(card)
    if(total > 21):
        return "BUST"
    else:
        return total


def main():
    populate_deck()



if __name__ == "__main__":
    main()