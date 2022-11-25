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
import main


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
      
    players_per_generation = 5
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


#IGNORE THE BELOW, USED IT TO GENERATE THE CROSS OVER DEMO IMAGES
'''
if __name__ == "__main__":
    victors = []
    for i in range(4):
        p = Player.player()
        p.generation = 1
        p.player_number = i + 1
        victors.append(p)
    print(victors)
    player = victors[0]
    player.POOL = 320
    for row in player.STRATEGY_TABLE_HARD_HAND:
            for elem in player.STRATEGY_TABLE_HARD_HAND[row]:
                player.STRATEGY_TABLE_HARD_HAND[row][elem] = 'P'
    player = victors[1]
    player.POOL = 27
    for row in player.STRATEGY_TABLE_HARD_HAND:
            for elem in player.STRATEGY_TABLE_HARD_HAND[row]:
                player.STRATEGY_TABLE_HARD_HAND[row][elem] = 'D'
    player = victors[2]
    player.POOL = 27
    for row in player.STRATEGY_TABLE_HARD_HAND:
            for elem in player.STRATEGY_TABLE_HARD_HAND[row]:
                player.STRATEGY_TABLE_HARD_HAND[row][elem] = 'H'
    player = victors[3]
    player.POOL = 27
    for row in player.STRATEGY_TABLE_HARD_HAND:
            for elem in player.STRATEGY_TABLE_HARD_HAND[row]:
                player.STRATEGY_TABLE_HARD_HAND[row][elem] = 'S'
    
    for v in victors: 
        main.visualize_strategy_tables(v)
    new_gen = CrossOver(victors)
    for g in new_gen:
        main.visualize_strategy_tables(g)

 '''