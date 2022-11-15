
#!/usr/bin/env python
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
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import sys
from PIL import Image, ImageFont, ImageDraw
import os



#NOTE: The dealer has an infinite deck for the purposes of our algorithm

#Proven strategy tables data sourced from: https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c
#MOVES ARE INDEX by TABLE[PLAYER SUM][DEALER CARD]
PROVEN_STRATEGY_TABLE_HARD_HAND = {20:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"}, 
                              19:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                              18:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                              17:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"S", 8:"S", 9:"S", 10:"S", "Ace":"S"},
                              16:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              15:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              14:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              13:{2:"S", 3:"S", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              12:{2:"H", 3:"H", 4:"S", 5:"S", 6:"S", 7:"H", 8:"H", 9:"H", 10:"H", "Ace":"H"},
                              11:{2:"D", 3:"D", 4:"D", 5:"D", 6:"D", 7:"D", 8:"D", 9:"D", 10:"D", "Ace":"D"},
                              10:{2:"D", 3:"D", 4:"D", 5:"D", 6:"D", 7:"D", 8:"D", 9:"D", 10:"H", "Ace":"H"},
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
                                   

BET_AMOUNT = 2 #Bet $2 per hand
DECK = []
LIMIT = 1000 #Each player plays until their Pool is 0 or Limit is reached
OPTIMAL_PLAYER = None


def _color_table(val):
    color = ''
    if(val == 'S'):
        color = 'red'
    elif(val == 'H'):
        color = 'green'
    elif(val == 'D'):
        color = 'yellow'
    elif(val == 'P'):
        color = 'purple'
    else:
        color = 'white'
    return 'background-color: %s' % color

def visualize_strategy_tables(player, player_number, generation):
    path = "./Strategy Table Images/Generation " + str(generation) + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    player_designation = str(player_number) + "_"

    info_text = "Generation: " + str(generation) + "\nPlayer: "+ str(player_number) +"\nRemaining Funds: $"+ str(player.POOL)
    font = ImageFont.truetype("arial.ttf", size=20)
    info_img = Image.new('RGB', (300, 100), color=(255,255,255))
    imgDraw = ImageDraw.Draw(info_img)
    imgDraw.text((10,10), info_text, font=font, fill=(0,0,0))
    info_img.save(path+player_designation+"info.png")

    df_hard_hand = pd.DataFrame(player.STRATEGY_TABLE_HARD_HAND).T
    df_hard_hand.style.set_table_attributes("style='display:inline'").set_caption('Hard Hand')
    df_styled_hard_hand = df_hard_hand.style.applymap(_color_table)
    dfi.export(df_styled_hard_hand,path+player_designation+"hard_hand.png")
    
    df_soft_hand = pd.DataFrame(player.STRATEGY_TABLE_SOFT_HAND).T
    df_styled_soft_hand = df_soft_hand.style.applymap(_color_table)
    dfi.export(df_styled_soft_hand,path+player_designation+"soft_hand.png")

    df_pair = pd.DataFrame(player.STRATEGY_TABLE_PAIR).T
    df_styled_pair = df_pair.style.applymap(_color_table)
    dfi.export(df_styled_pair,path+player_designation+"pair.png")

    images = [Image.open(x) for x in [path+player_designation+"hard_hand.png", path+player_designation+"soft_hand.png", path+player_designation+"pair.png"]]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    all_tables = Image.new('RGB', (total_width, max_height), color = (255, 255, 255))
    info_img = Image.open(path+player_designation+"info.png")
    x_offset = 0
    PASTED_INFO = False
    for im in images:
        all_tables.paste(im, (x_offset,0))
        if(x_offset != 0 and not PASTED_INFO):
            all_tables.paste(info_img, (x_offset + 300, 400))
            PASTED_INFO = True
        x_offset += im.size[0]
    file_name = path + "PLAYER " + str(player_number) + " RESULTS.png"
    all_tables.save(file_name)
    os.remove(path+player_designation+"hard_hand.png")
    os.remove(path+player_designation+"soft_hand.png")
    os.remove(path+player_designation+"pair.png")
    os.remove(path+player_designation+"info.png")


#Returns a random card from the populated deck
def get_random_card():
    if(len(DECK) > 52):
        print("Error: populate deck prior to drawing card")
        return None
    return DECK[random.randint(0, len(DECK)-1)]


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
    dealer_val_one = get_card_value(dealer_hand[0])
    dealer_val_two = get_card_value(dealer_hand[1])
    dealer_sum = dealer_val_one + dealer_val_two
    # when playing final version (not when training AI) we want to update the pool accordingly 
    if(player_sum == 21 and dealer_sum != 21):
        # the player normally earns 3/2 odds -> on a $2 bet, $3 is earned (+$1) instead of the normal $4 (+$2)
        # player.POOL += (0.5 * player.BET_AMOUNT)
        return "Player Blackjack: Player Win"
    if(player_sum != 21 and dealer_sum == 21):
        # the player looses normally
        # player.POOL -= player.BET_AMOUNT
        return "Dealer BlackJack: Player Lose"
    if(player_sum == 21 and dealer_sum == 21):
        # the bet is a "push", no money exchanged
        return "Player and Dealer Blackjack: Push"
    else:
        return None



#Takes a card in the form "Value of Suit" and returns an integer of the value unless Ace. Example: "7 of Hearts" -> 7, "King of Spades" -> 10, "Ace of Clubs" -> "Ace"
def get_card_value(card):
    card = card.split(" of ")
    value = card[0]
    if(value == "Ace"):
        #Function only used in check_naturals(), ace should default to 11 to make blackjack
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


#ACTION: Finished drawing, check player hand against dealer's. Returns a bool of if game was won or not
def stand(player):
    player.done_with_hand = True


#ACTION: player asks for a new card to be added to their hand
def hit(player):
    player.hand.append(get_random_card())


#ACTION: Double Down. Player hits one more time and bets a doubled amount. After hitting one more, procedure is the same as stand (see above)
def double_down(player):
    if len(player.hand) != 2:
        print("Error: can only double down with 2 cards")
        # if the AIs table says double and you have 3 cards, Hit instead
        Hit(player)
        return None
    player.BET_AMOUNT = 2 * player.BET_AMOUNT
    print("Doubling Down with bet: $" + str(player.BET_AMOUNT))
    hit(player)
    player.done_with_hand = True


#ACTION: Checks if there is a pair and player has not split.  Stores pair value so it can evaluate the hands individually
def split(player, dealer_hand):
    # many of these tests can be removed when we decide if the AIs hand is a hard hand, soft hand, or pair
    if len(player.hand) != 2:
        print("Error: Can only split with 2 cards")
        return None
    card_1 = player.hand[0].split(" of ")
    card_2 = player.hand[1].split(" of ")
    if card_1[0] != card_2[0]:
        print("Error: Cannot split with no pair")
        return None
    if player.has_split is True:
        print("Error: Cannor split twice")
        return None
    # store some split information: Bool, split card value, and bet amount
    player.has_split = True
    player.split_card = player.hand[1]
    player.BET_AMOUNT = 1
    player.hand.pop(1)
    player.hand.append(get_random_card())
    # play hand #1
    play_hand(player, dealer_hand)    
    # reset bet_amount and create second hand
    player.BET_AMOUNT = 1
    player.done_with_hand = False
    player.hand.clear()
    player.hand.append(player.split_card)
    player.hand.append(get_random_card())
    # play hand #2
    # plays second hand when it exits into play_hand() function
    


#Checks if player has exceeded 21, returns "BUST" if so and returns the total value of their cards if not
def check_player_hand(player_hand):
    total = 0
    for card in player_hand:
        card = card.split(" of ")
        value = card[0]
        if value != "Ace":
            if(value == "King" or value == "Queen" or value == "Jack"):
                total += 10
            else:
                total += int(value)
        else:
            # If Ace, use 11 unless that makes the player go over, then use 1
            total += 1
    # After evaluated total with aces = 1, check to see if they can be 11 without busting
    for card in player_hand:
        card = card.split(" of ")
        value = card[0]
        if value == "Ace":
            total -= 1 # This temporarily deletes the ace from the total for readability
            if(total + 11 > 21):
                total += 1
            else:
                total += 11
    if(total > 21):
        return "BUST"
    else:
        return total


 #As per the game rules, the dealer hits automatically if the total is under 17 and stands automatically if over 17 but under 21. Bust if 21 or over
def get_dealer_hand(dealer_hand):
    total = check_player_hand(dealer_hand)
    # this is assuming the dealer is playing by Soft-17 rules (dealer must stand on a soft 17 e.g., [Ace, 6], [2, 4, Ace])
    # Solf-17 gives the dealer a slight advantage
    while (total != "BUST") and (total < 17):
        dealer_hand.append(get_random_card())
        total = check_player_hand(dealer_hand)
    return total, dealer_hand


 #Checks action the AI will take until "done with hand"
def play_hand(player, dealer_hand):
    while not player.done_with_hand:
        # choose action from randomized table
        # Hit, stand, double down, or split based on soft-hand, hard-hand, or pair
        # Need to put some logic in place in some of the following situations:
        # default to HIT if double cannot be done, implemented in double function
        # 6-Ace is soft as well as a 6-3-Ace (9-Ace), but 10-Ace is 21 by default -> player.done_with_hand, 11-Ace, 12-Ace, 13-Ace... and up is a hard-12, hard-13, hard-14...
        # A-A is a pair, not a soft or hard hand
        print("Player Hand: {}".format(player.hand) + " Total: " + str(check_player_hand(player.hand)))
        action = input("Enter your action (H,S,D,P): ")
        if action == 'H':
            hit(player)
        elif action == 'S':
            stand(player)
        elif action == 'D':
            double_down(player)
        elif action == 'P':
            split(player, dealer_hand)

        if check_player_hand(player.hand) == "BUST" or check_player_hand(player.hand) == 21:
            player.done_with_hand = True
    
    #need to evaluate inside this function since split has 2 calls to play_hand
    evaluate_hands(player, dealer_hand)
    print("Balance: " + str(player.POOL))


 #Evaluates Hands after play is complete, prints winner, and returns True or False for a Win
def evaluate_hands(player, dealer_hand):
    player_total = check_player_hand(player.hand)
    dealer_total, dealer_hand = get_dealer_hand(dealer_hand)
    if(player_total == "BUST"):
        print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(dealer_hand, dealer_total, player.hand, player_total))
        print("Player Lose, Bust")
        player.POOL -= player.BET_AMOUNT
        return False
    if(dealer_total == "BUST"):
        print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(dealer_hand, dealer_total, player.hand, player_total))
        print("Player wins, dealer bust")
        player.POOL += player.BET_AMOUNT
        return True
    player_diff = 21 - player_total 
    dealer_diff = 21 - dealer_total 
    if(player_diff < dealer_diff):
        print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(dealer_hand, dealer_total, player.hand, player_total))
        print("Player Wins")
        player.POOL += player.BET_AMOUNT
        return True
    else:
        print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(dealer_hand, dealer_total, player.hand, player_total))
        print("Player Lose")
        player.POOL -= player.BET_AMOUNT
        return False


 #Resets values of player.  i.e. if you double down, the next hand is reset to a bet of $2
def reset_player(player):
    player.BET_AMOUNT = 2
    player.hand = []
    player.has_split = False
    player.split_card = None
    player.done_with_hand = False


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
    global OPTIMAL_PLAYER
    OPTIMAL_PLAYER = Player.player()
    OPTIMAL_PLAYER.STRATEGY_TABLE_HARD_HAND = PROVEN_STRATEGY_TABLE_HARD_HAND
    OPTIMAL_PLAYER.STRATEGY_TABLE_SOFT_HAND = PROVEN_STRATEGY_TABLE_SOFT_HAND
    OPTIMAL_PLAYER.STRATEGY_TABLE_PAIR = PROVEN_STRATEGY_TABLE_PAIR
    visualize_strategy_tables(OPTIMAL_PLAYER, "OPTIMAL", "OPTIMAL")
    init_pop = generate_inital_population(1)
    for i in range(len(init_pop)):
        visualize_strategy_tables(init_pop[i], i+1, 1)


    # testing play
    keep_playing = 'y'
    test_player = Player.player()
    while keep_playing == 'y':
        dealers_hand = []
        result = None
        [test_player.hand, dealer_hand] = deal()
        print("Dealer Hand: {}".format(dealer_hand[0]))
        result = check_naturals([test_player.hand, dealer_hand])
        if not result:
            play_hand(test_player, dealer_hand)
        else:
            print(result)
            print("Balance: " + str(test_player.POOL))

        keep_playing = input("Keep Playing? (y/n): ")
        reset_player(test_player)

if __name__ == "__main__":
    main()