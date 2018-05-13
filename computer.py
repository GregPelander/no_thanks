# computer.py -- sample bot

import logging
import random

def get_play(players, current_card, current_tokens, me):
    # check if the card is sequential to one of ours
    for card in me.cards:
        if(abs(card - current_card) == 1):
            return True
    # 

    # otherwise we take if it has tokens and is below a threshold
    return(current_tokens > 1 and current_card - current_tokens < 11)
