# human.py -- human liar's dice player

import logging

def get_play(players, current_card, current_tokens, id):
    me = players[id]
    ''' play against the computer '''
    logging.info('You are player "%s" | Current Card: %i | Current Tokens: %i \
                |  Your Cards: %i | Your Tokens: %i' % (me.name, current_card,
                current_tokens, me.cards, me.tokens))
    logging.info('"Pass" or "Take":')
    s = raw_input()
    x = (s == 'Pass')
    logging.info('*' * 50)
    return x
