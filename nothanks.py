# nothanks.py -- main game engine
import logging
import random
import sys

##  ONFIGURATION
#
LOWEST_CARD     = 3
HIGHEST_CARD    = 35
NUM_REMOVED     = 9
TOKENS          = 11

class Player:
    def __init__(self, id, name, file, tokens):
        self.key = id
        self.name = name
        self.cards = []
        self.tokens = tokens
        self.name = name
        self.file = file
        self.score = 0

# Get User
def get_play(game_id, players, current_card,
            current_tokens, current_player, catch_exceptions):
    play = 0
    try :
        play = bool(current_player.file(players, current_card,
                                current_tokens, current_player))
    except KeyboardInterrupt :
        raise
    except :
        if not catch_exceptions :
            raise
        logging.warn('caught exception "%s" calling %s (%s) \'s get_play() function' % (sys.exc_info()[1],who,player_name))
    return play

def play_game(game_id, players_in, catch_exceptions):

    ## SETUP

    # Get the players and give each 11 tokens
    players = []
    for key in players_in:
        players.append(Player(players_in[key].id, players_in[key].name,
                              players_in[key].file, TOKENS))
    logging.info('=' * 50)
    logging.info('Starting a new game between %s' % ', '.join(x.name for x in players))

    # Pick a player to start
    random.shuffle(players)
    player_index = 0
    current_player = players[player_index]
    logging.info('*** %s will start ***' % current_player.name)

    # Get a deck of (suitless) cards numbered 3 to 35
    deck = list(range(LOWEST_CARD, HIGHEST_CARD))

    # Remove 9 cards from the deck at random
    random.shuffle(deck)
    for _ in range(NUM_REMOVED):
        deck.pop()

    # Flip over a new card
    current_card = deck.pop()
    current_tokens = 0
    logging.info('%s flips over the [%i]' \
        % (current_player.name, current_card))



    ## GAMEPLAY

    # The game ends when there are no cards left in the deck
    while len(deck):

        # The current player may either take the face up card
        # or pass (if they have tokens)
        if(current_player.tokens == 0):
            take_card = True
        else:
            take_card = get_play(game_id, players, current_card,
                                 current_tokens, current_player, catch_exceptions)

        if(take_card):
            # They collect any tokens on the card
            current_player.tokens += current_tokens
            if(current_tokens == 1):
                logging.info('%s takes the [%i] and 1 token' \
                    % (current_player.name, current_card))
            else:
                logging.info('%s takes the [%i] and %i tokens' \
                    % (current_player.name, current_card, current_tokens))
            current_tokens = 0

            # They put the card face up in front of them
            current_player.cards.append(current_card)

            # They flip over the next card in the deck and start a new turn
            current_card = deck.pop()
            logging.info('%s flips over the [%i]' \
                % (current_player.name, current_card))
            logging.info("*** It is still %s's turn ***" % current_player.name)
            continue

        else:
            # They put a token on the card and it is the next player's turn
            current_tokens += 1
            current_player.tokens -= 1
            if(current_tokens == 1):
                logging.info('%s passes and adds a token. '\
                    'There is now 1 token on the card'
                    % current_player.name)
            else:
                logging.info('%s passes and adds a token. ' \
                    'There are now %i tokens on the card'
                    % (current_player.name, current_tokens))
            player_index += 1
            current_player = players[player_index % len(players)]
            logging.info("\n*** It is now %s's turn ***" % current_player.name)
            continue

    ## SCORING

    winner = None
    for player in players:
        # Tokens are worth -1 point each
        player.score -= player.tokens

        # Single cards are worth their value
        # A sequence of cards is worth the value of the lowest card in the sequence
        player.cards.sort()
        last_card = None
        for card in player.cards:
            if(last_card is None or card - last_card > 1):
                player.score += card
            last_card = card

        logging.info("%s finishes with %i" % (player.name, player.score))

        if(winner is None or player.score < winner.score):
            winner = player

    return winner.key
