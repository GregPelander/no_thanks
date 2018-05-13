# human.py -- allows a human to play

import logging

def get_play(players, current_card, current_tokens, me):
    #sort Cards
    me.cards.sort()

    logging.info('You are player "%s" | Current Card: [%i] | ' \
                'Current Tokens: %i | Your Cards: %s | Your Tokens: %i' \
                % (me.name, current_card, current_tokens, ' ' \
                .join(('[%s]' % str(x)) for x in me.cards), me.tokens))
    logging.info('"Pass" or "Take":')
    s = input()
    x = (s.lower() == 'take')
    logging.info('*' * 50)
    return x
