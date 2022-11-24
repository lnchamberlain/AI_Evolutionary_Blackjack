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


import random
import Player


def Selection(Generation):
    print("STUB")


#Takes in an array of the 4 victor players of the previous generation. Returns a array of the next generation
def CrossOver(victors):
    sum = 0
    n = 0
    #Weights are calcuated as the % of the total winnings. Progressively summed to get 4 values that sum to 100, i.e 0 to w1 = Player 1 Pool / sum, w1 to w2 = Player 2 Pool / sum
    for player in victors:
        sum += player.POOL
    w1 = (victors[0].POOL / sum) * 100  
    w2 = ((victors[1].POOL / sum) + w1 / 100) * 100
    w3 = ((victors[2].POOL / sum) + w2 / 100) * 100 
      
    players_per_generation = 400
    new_generation = []
    prev_gen_number = victors[0].generation
    new_gen_number = prev_gen_number + 1
    for i in range(players_per_generation):
        new_player = Player.player()
        new_player.player_number = i + 1
        new_player.generation = new_gen_number
        new_generation.append(new_player)

    for player in new_generation:

        for row in player.STRATEGY_TABLE_HARD_HAND:
            for elem in player.STRATEGY_TABLE_HARD_HAND[row]:
                n = random.randint(0, 100)
                if(n < w1):
                    player.STRATEGY_TABLE_HARD_HAND[row][elem] = victors[0].STRATEGY_TABLE_HARD_HAND[row][elem]
                elif(n >= w1 and n < w2):
                    player.STRATEGY_TABLE_HARD_HAND[row][elem] = victors[1].STRATEGY_TABLE_HARD_HAND[row][elem]
                elif(n >= w2 and n < w3):
                    player.STRATEGY_TABLE_HARD_HAND[row][elem] = victors[2].STRATEGY_TABLE_HARD_HAND[row][elem]
                elif(n >= w3):
                    player.STRATEGY_TABLE_HARD_HAND[row][elem] = victors[3].STRATEGY_TABLE_HARD_HAND[row][elem]

        for row in player.STRATEGY_TABLE_SOFT_HAND:
            for elem in player.STRATEGY_TABLE_SOFT_HAND[row]:
                n = random.randint(0, 100)
                if(n < w1):
                    player.STRATEGY_TABLE_SOFT_HAND[row][elem] = victors[0].STRATEGY_TABLE_SOFT_HAND[row][elem]
                elif(n >= w1 and n < w2):
                    player.STRATEGY_TABLE_SOFT_HAND[row][elem] = victors[1].STRATEGY_TABLE_SOFT_HAND[row][elem]
                elif(n >= w2 and n < w3):
                    player.STRATEGY_TABLE_SOFT_HAND[row][elem] = victors[2].STRATEGY_TABLE_SOFT_HAND[row][elem]
                elif(n >= w3):
                    player.STRATEGY_TABLE_SOFT_HAND[row][elem] = victors[3].STRATEGY_TABLE_SOFT_HAND[row][elem]

        for row in player.STRATEGY_TABLE_PAIR:
            for elem in player.STRATEGY_TABLE_PAIR[row]:
                n = random.randint(0, 100)
                if(n < w1):
                    player.STRATEGY_TABLE_PAIR[row][elem] = victors[0].STRATEGY_TABLE_PAIR[row][elem] 
                elif(n >= w1 and n < w2):
                    player.STRATEGY_TABLE_PAIR[row][elem] = victors[1].STRATEGY_TABLE_PAIR[row][elem]
                elif(n >= w2 and n < w3):
                    player.STRATEGY_TABLE_PAIR[row][elem] = victors[2].STRATEGY_TABLE_PAIR[row][elem] 
                elif(n >= w3):
                    player.STRATEGY_TABLE_PAIR[row][elem] = victors[3].STRATEGY_TABLE_PAIR[row][elem]
                 
    return new_generation






def Mutation(child):
    print("STUB")

