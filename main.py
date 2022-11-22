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
import Dealer
import time
import concurrent.futures
import multiprocessing as mp
from multiprocessing import Queue
import threading
import random
import sys
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import sys
from PIL import Image, ImageFont, ImageDraw
import os
import time


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
OPTIMAL_PLAYER = None
VICTOR_RESULTS_LIST = []


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

def visualize_strategy_tables(player):
    path = "./Strategy Table Images/Generation " + str(player.generation) + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    player_designation = str(player.player_number) + "_"

    info_text = "Generation: " + str(player.generation) + "\nPlayer: "+ str(player.player_number) +"\nRemaining Funds: $"+ str(player.POOL)
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
    file_name = path + "PLAYER " + str(player.player_number) + " RESULTS.png"
    all_tables.save(file_name)
    os.remove(path+player_designation+"hard_hand.png")
    os.remove(path+player_designation+"soft_hand.png")
    os.remove(path+player_designation+"pair.png")
    os.remove(path+player_designation+"info.png")


#Returns rank of random card (blackjack doesnt care about suits) from the populated deck
def get_random_card():
    if(len(DECK) > 52):
        #print("Error: populate deck prior to drawing card")
        return None
    card = DECK[random.randint(0, len(DECK)-1)]
    card = card.split(" of ")
    return card[0]


#Returns an array of the player's cards and the dealers visible card and not visible card in the form [[Player Card 1, Player Card 2], [Dealer Visible Card, Dealer not Visible Card]]. Example: [[]"7 of hearts", "King of Spades"], []"Jack of Diamonds", "3 of Clubs"]]
def deal(player, dealer):
    player_card_1 = get_random_card()
    player_card_2 = get_random_card()
    if player_card_1 == player_card_2:
        player.can_split = True
    get_card_value(player, player_card_1)
    get_card_value(player, player_card_2)

    dealer_card_1 = get_random_card()
    if dealer_card_1 == 'Ace':
        dealer.hole_card = 'Ace'
    elif dealer_card_1 == 'Jack' or dealer_card_1 == 'Queen' or dealer_card_1 == 'King':
        dealer.hole_card = 10
    else:
        dealer.hole_card = int(dealer_card_1)
    get_card_value(dealer, get_random_card())
    get_card_value(dealer, get_random_card())
    return 

#Checks for the condition wherein a player is drawn an Ace and a 10 card (10 or any face card), resulting in an immediate Blackjack. Different conditions exist for player and dealers having a natural, returns None if not applicable, return a string describing who won is applicable. 
def check_naturals(player, dealer):
    # when playing final version (not when training AI) we want to update the pool accordingly 
    if player.total == 21 and dealer.total != 21:
        # the player normally earns 3/2 odds -> on a $2 bet, +$3 is earned instead of the normal +$2
        player.POOL += (1.5 * player.BET_AMOUNT)
        player.hands_won += 1
        return "Player Blackjack: Player Win"
    if player.total != 21 and dealer.total == 21:
        # the player looses normally
        player.POOL -= player.BET_AMOUNT
        player.hands_lost += 1
        return "Dealer BlackJack: Player Lose"
    if player.total == 21 and dealer.total == 21:
        # the bet is a "push", no money exchanged
        player.hands_tied += 1
        return "Player and Dealer Blackjack: Push"
    else:
        return None



#Takes a card in the form "Value of Suit" and returns an integer of the value unless Ace. Example: "7 of Hearts" -> 7, "King of Spades" -> 10, "Ace of Clubs" -> "Ace"
def get_card_value(player, value):
    if value == "Ace":
        # player can only have 1 Ace without busting     i.e., hand [Ace, Ace] == [Ace, 1]
        # player can only have an Ace if total is < 11   i.e., hand [8, 8, Ace] == [8, 8, 1]
        if player.hand[0] != 11 and player.total < 11:
            player.hand[0] = 11
            player.total += 11
        else:
            player.hand[1] += 1
            player.total += 1
    elif value == "King" or value == "Queen" or value == "Jack":
        player.hand[1] += 10
        player.total += 10
    else:
        value = int(value)
        player.hand[1] += value
        player.total += value
    if player.total > 21 and player.hand[0] == 11:
        player.total -= 10
        player.hand[0] = 0
        player.hand[1] += 1


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
    card = get_random_card()
    get_card_value(player, card)



#ACTION: Double Down. Player hits one more time and bets a doubled amount. After hitting one more, procedure is the same as stand (see above)
def double_down(player):
    if not player.first_action:
        #print("Error: can only double down with 2 cards")
        # if the AIs table says double and you have 3 cards, Hit instead
        hit(player)
        return None
    player.BET_AMOUNT = 2 * player.BET_AMOUNT
    #print("Doubling Down with bet: $" + str(player.BET_AMOUNT))
    hit(player)
    player.done_with_hand = True


#ACTION: Checks if there is a pair and player has not split.  Stores pair value so it can evaluate the hands individually
def split(player, dealer):
    # store some split information: Bool, split card value, and create first hand
    player.can_split = False
    if player.hand[0] == 11:
        player.hand[1] = 0
        player.split_card = 11
        player.hand[0] = 11
        player.done_with_hand = True
    else:
        player.split_card = int(player.total/2)
        player.hand[1] = player.split_card
    player.total = player.split_card
    hit(player)
    # play hand #1
    play_hand(player, dealer)    
    # Create second hand
    player.done_with_hand = False
    if player.split_card == 11:
        player.hand[0] = 11
        player.hand[1] = 0
        player.done_with_hand = True
    else:
        player.hand[0] = 0
        player.hand[1] = player.split_card
    player.total = player.split_card
    hit(player)
    # play hand #2
    # plays second hand when it exits into play_hand() function
    
'''
#Get a single cards value 
def get_single_card_val(card):
    #print(card)
    l = card.split(" of ")
    value = l[0]
    if value != "Ace":
            if(value == "King" or value == "Queen" or value == "Jack"):
                total = 10
            else:
                total = int(value)
    else:
            #If Ace, use 11 unless that makes the player go over, then use 1
            total = "Ace"
    return total


#Checks if player has exceeded 21, returns "BUST" if so and returns the total value of their cards if not
def check_player_hand(hand):
    total = 0
    for card in hand:
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
    for card in hand:
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
'''

 #As per the game rules, the dealer hits automatically if the total is under 17 and stands automatically if over 17 but under 21. Bust if 21 or over
def get_dealer_hand(dealer):
    # this is assuming the dealer is playing by Soft-17 rules (dealer must stand on a soft 17 e.g., [Ace, 6], [2, 4, Ace])
    # Solf-17 gives the dealer a slight advantage
        while dealer.total < 17:
            card = get_random_card()
            get_card_value(dealer, card)
        return

 #Checks action the AI will take until "done with hand"
def play_hand(player, dealer):
    if player.total == 21:
        player.done_with_hand = True
    while not player.done_with_hand:
        # choose action from randomized table
        # Hit, stand, double down, or split based on soft-hand, hard-hand, or pair
        # Need to put some logic in place in some of the following situations:
        # default to HIT if double cannot be done (more than 2 cards), implemented in double function
        # 6-Ace is soft as well as a 6-3-Ace (9-Ace), but 10-Ace is 21 by default -> player.done_with_hand, 11-Ace, 12-Ace, 13-Ace... and up is a hard-12, hard-13, hard-14...
        # A-A is a pair, not a soft or hard hand
        # need to deal with already_split to appropriate soft or hard hand within this function: e.g., draw 7,7     -> split -> first hand = 7,   draw 7   -> this is a hard 14 
        # After splitting aces, limit to 1 hit per hand
        #print("Player Hand: {}".format(player.hand) + " Total: " + str(check_player_hand(player.hand)))
        #TODO, do we check for an ace and a face card or automatic win before we reach this point?
        #Soft hand condtion

        action = ''

        #Pair condition: check this first so we dont need to check for 2 aces in soft-hand    
        if player.can_split:
            if player.hand[0] == 11:
                action = player.STRATEGY_TABLE_PAIR["A-A"][dealer.hole_card]
            else:
                value = str(int(player.total/2))
                action = player.STRATEGY_TABLE_PAIR[value + "-" + value][dealer.hole_card]

        elif player.hand[0] == 11:
            #Get the value of the card that is not an ace
            if player.hand[1] == 1:
                action = player.STRATEGY_TABLE_SOFT_HAND["A-A"][dealer.hole_card]
            else:
                action = player.STRATEGY_TABLE_SOFT_HAND["A-" + str(player.hand[1])][dealer.hole_card]

        #Hard hand condtion
        else:
            action = player.STRATEGY_TABLE_HARD_HAND[player.hand[1]][dealer.hole_card]

           
        #action = input("Enter your action (H,S,D,P): ")

        if action == 'H':
            hit(player)
        elif action == 'S':
            stand(player)
        elif action == 'D':
            double_down(player)
        elif action == 'P':
            player.first_action = False
            split(player, dealer)
        player.first_action = False

        
        if player.total > 20:
            player.done_with_hand = True
    
    #need to evaluate inside this function since split has 2 calls to play_hand
    evaluate_hands(player, dealer)
    #print("Balance: " + str(player.POOL))


 #Evaluates Hands after play is complete, prints winner, and returns True or False for a Win
def evaluate_hands(player, dealer):
    get_dealer_hand(dealer)
    if(player.total > 21):
        #print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(player.dealer_hand, player.dealer_total, player.hand, player.total))
        #print("Player Lose, Bust")
        player.POOL -= player.BET_AMOUNT
        player.hands_lost += 1
        return False
    elif(dealer.total > 21):
        #print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(player.dealer_hand, player.dealer_total, player.hand, player.total))
        #print("Player wins, dealer bust")
        player.POOL += player.BET_AMOUNT
        player.hands_won += 1
        return True
    elif(player.total > dealer.total):
        #print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(player.dealer_hand, player.dealer_total, player.hand, player.total))
        #print("Player Wins")
        player.POOL += player.BET_AMOUNT
        player.hands_won += 1
        return True
    elif(player.total == dealer.total):
        #print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(player.dealer_hand, player.dealer_total, player.hand, player.total))
        #print("Push")
        player.hands_tied += 1
        return True
    else:
        #print("Dealer Hand: {}  Total: {}\nPlayer Hand: {}  Total: {}".format(player.dealer_hand, player.dealer_total, player.hand, player.total))
        #print("Player Lose")
        player.POOL -= player.BET_AMOUNT
        player.hands_lost += 1
        return False


    #Plays a game with a player until 1000 hands or player pool is 0
def play_game(player,RESULTS):
    populate_deck()
    dealer = Dealer.dealer()
    while player.hands_played < player.LIMIT:
        deal(player, dealer)
        #print("Dealer Hand: {}".format(player.dealer_hand[0]))
        result = check_naturals(player, dealer)
        if not result:
            play_hand(player, dealer)
        #else:
            #print(result + " had naturals")
            #print("Balance: " + str(player.POOL))
        reset(player, dealer)
        player.hands_played += 1
    #Build array of result information to determine victors
    RESULTS.put([player.player_number, player.generation, player.POOL, player.hands_played, player.hands_won, player.hands_lost, player.hands_tied])
    #RESULTS.append([player.player_number, player.generation, player.POOL, player.hands_played, player.hands_won, player.hands_lost, player.hands_tied])
    return 


 #Resets values of player.  i.e. if you double down, the next hand is reset to a bet of $2
def reset(player, dealer):
    player.done_with_hand = False
    player.BET_AMOUNT = 2
    player.hand = [0, 0]
    player.total = 0
    player.dealer_hand = []
    player.dealer_total = 0
    player.can_split = False
    player.split_card = None
    player.first_action = True

    dealer.hand = [0, 0]
    dealer.hole_card
    dealer.total = 0



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


POP_SIZE = 400
num_processes = os.cpu_count()
Threads = [None]*num_processes


if __name__ == "__main__":
    OPTIMAL_PLAYER = Player.player()
    OPTIMAL_PLAYER.STRATEGY_TABLE_HARD_HAND = PROVEN_STRATEGY_TABLE_HARD_HAND
    OPTIMAL_PLAYER.STRATEGY_TABLE_SOFT_HAND = PROVEN_STRATEGY_TABLE_SOFT_HAND
    OPTIMAL_PLAYER.STRATEGY_TABLE_PAIR = PROVEN_STRATEGY_TABLE_PAIR
    visualize_strategy_tables(OPTIMAL_PLAYER)
    population = generate_inital_population(POP_SIZE)
    print(population)
    #Fill in generation info and player numbers 
    for i in range(POP_SIZE):
        population[i].generation = 0
        population[i].player_number = i + 1
    
    # Running with Miltiprocessing
    ##################################################################################################
    RESULTS = mp.Queue()
    Generation1 = []
    i = 0
    Start = time.time()
    # loops through population
    while i < len(population):
        # thread index is population % desired number of threads
        threadIndex = i % num_processes
        # play game through each thread and write result into RESULTS
        Threads[threadIndex] = mp.Process(target=play_game, args=(population[i],RESULTS,))
        Threads[threadIndex].start()
        # if you reach the max number of threads, wait for all threads to finish
        if threadIndex == num_processes-1:
            for j in range(num_processes):
                Threads[j].join()
                Generation1.append(RESULTS.get())
                print("Process: " + str(i))
        i += 1
    # after looping through population, wait for remaining threads
    for j in range(num_processes):
        Threads[j].join()
    End = time.time()
    for results in Generation1:
        print(results)
    
    print("Time: " + str(End-Start))
    # Running without Treads
    ##################################################################################################
    '''
    RESULTS = []
    i = 0
    Start = time.time()
    populate_deck()
    for player in population:
        play_game(player, RESULTS)
        print(RESULTS.pop())
    End = time.time()
    for results in RESULTS:
        print(results)
    print("Time: " + str(End-Start))
    '''