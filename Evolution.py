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
POP_SIZE = 50
# number of payers chosen for each tournament
tourneyNum = 4
# number of parents to make a child 
numParents = 4
def Evolve(Generation):
    NextGeneration = []
    # do whatever selection we want
    TourneySelection(Generation, NextGeneration)
    return NextGeneration
def TourneySelection(Generation, NextGeneration):
    Selected = []
    # Create groups of players of size tourneyNum until the generation is empty
    while len(Generation) > 0:
        Tourney = []
        # choose, without replacement, random players from the generation 
        i = 0
        while i < tourneyNum:
            randomChoice = random.randint(0, len(Generation)-1)
            Tourney.append(Generation.pop(randomChoice))
            if len(Generation) == 0:
               i = tourneyNum
            i += 1
        # sort the players in the tournament
        Tourney.sort(key=lambda x: x.POOL, reverse=True)
        # append the best to the Selected
        Selected.append(Tourney[0])
    # THIS FILLS THE REST OF THE GENERATION
    # make 2 copies of the selected generation
    SelectedTemp = Selected.copy()
    # while the generation isn't full
    while len(NextGeneration) < POP_SIZE:
        # the remaining victors is less that how many parents/child
        if len(SelectedTemp) < numParents:
            # recopy the victors
            SelectedTemp = Selected.copy()
        parents = []
        # copy random parents into list "parents" without replacement
        for i in range(numParents):
            randomChoice = random.randint(0, len(SelectedTemp)-1)
            parents.append(SelectedTemp.pop(randomChoice))
        
        NextGeneration.append(CrossOverTourney(parents))




#Takes in an array of the 4 victor players of the previous generation. Returns a array of the next generation
def CrossOverTourney(Parents):
    sum = 0
    weights = []

    #Weights are calcuated as the % of the total winnings. Progressively summed to get 4 values that sum to 100, i.e 0 to w1 = Player 1 Pool / sum, w1 to w2 = Player 2 Pool / sum
    for player in Parents:
        sum += player.POOL

    for player in Parents:
        weights.append(player.POOL/sum)
      
    child = Player.player()
    #Fill in Hard hand table
    for row in child.STRATEGY_TABLE_HARD_HAND:        
        for elem in child.STRATEGY_TABLE_HARD_HAND[row]:
            child.STRATEGY_TABLE_HARD_HAND[row][elem] = random.choices([player.STRATEGY_TABLE_HARD_HAND[row][elem] for player in Parents], weights)[0]
    #Fill in Soft hand table
    for row in child.STRATEGY_TABLE_SOFT_HAND:        
        for elem in child.STRATEGY_TABLE_SOFT_HAND[row]:
            child.STRATEGY_TABLE_SOFT_HAND[row][elem] = random.choices([player.STRATEGY_TABLE_SOFT_HAND[row][elem] for player in Parents], weights)[0]
    #Fill in pairs tables
    for row in child.STRATEGY_TABLE_PAIR:        
        for elem in child.STRATEGY_TABLE_PAIR[row]:
            child.STRATEGY_TABLE_PAIR[row][elem] = random.choices([player.STRATEGY_TABLE_PAIR[row][elem] for player in Parents], weights)[0]
    
    return child
                 

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