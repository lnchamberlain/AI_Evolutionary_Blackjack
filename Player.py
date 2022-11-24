#!/usr/bin/env python
# Evolutionary Blackjack
# Semester Project for CSCE A405 AI
# Austin Edwards, Tuva Granoien, and Logan Chamberlain
# Fall 2022
#
#
################################################################################





class player():
    def __init__(self):
        #Strategy tables are empty at initalization
        self.STRATEGY_TABLE_HARD_HAND = {20:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""}, 
                              19:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              18:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              17:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              16:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              15:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              14:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              13:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              12:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              11:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              10:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              9:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""}, 
                              8:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              7:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              6:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              5:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                              4:{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""}}
                               # might need to add a 4 for the condition if it has split 2,2 and draws a 2                     

        self.STRATEGY_TABLE_SOFT_HAND = {"A-9":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""}, 
                                   "A-8":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "A-7":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "A-6":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "A-5":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "A-4":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "A-3":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "A-2":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "A-A":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""}}

        self.STRATEGY_TABLE_PAIR = {"A-A":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""}, 
                                   "10-10":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "9-9":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "8-8":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "7-7":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "6-6":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "5-5":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "4-4":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "3-3":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""},
                                   "2-2":{2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", "Ace":""}}
        
        self.COUNT_TABLE_HARD_HAND = {20:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0}, 
                              19:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              18:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              17:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              16:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              15:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              14:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              13:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              12:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              11:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              10:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              9:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0}, 
                              8:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              7:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              6:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              5:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                              4:{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0}}
                               # might need to add a 4 for the condition if it has split 2,2 and draws a 2                     

        self.COUNT_TABLE_SOFT_HAND = {"A-9":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0}, 
                                   "A-8":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "A-7":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "A-6":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "A-5":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "A-4":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "A-3":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "A-2":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "A-2":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0}}

        self.COUNT_TABLE_PAIR = {"A-A":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0}, 
                                   "10-10":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "9-9":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "8-8":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "7-7":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "6-6":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "5-5":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "4-4":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "3-3":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0},
                                   "2-2":{2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, "Ace":0}}


        # running counts and unchanging variables
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_tied = 0
        self.POOL = 100_000
        self.LIMIT = 10_000
        self.generation = 0
        self.player_number = 0
        # reset after every hand
        self.hand = [0, 0]
        self.total = 0
        self.BET_AMOUNT = 2
        self.first_action = True
        self.done_with_hand = False
        self.can_split = False
        self.split_card = None
