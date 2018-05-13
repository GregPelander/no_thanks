HELP = '''\
usage:

    To play a game against the computer:

        $ python main.py play human computer

    To play 10 games between get_play() in my_robot.py, get_play in
    his_robot.py, and dummy() in robots.py:

        $ python main.py tournament 10 my_robot.get_play his_robot.get_play robots.dummy
'''

import sys
import logging
import random
import time

import nothanks
import zipimport

# ignore SIG_PIPE
from signal import (signal,
                    SIGPIPE,
                    SIG_DFL)

signal(SIGPIPE, SIG_DFL)

class Player:
    def __init__(self, id, name, file):
        self.id = id
        self.name = name
        self.file = file
        self.score = 0

def make_player(s, catch_exceptions):
    filename = s
    attr = 'get_play'

    if -1 != s.find('.'):
        filename, attr = s.split('.')
    try:
        m = __import__(filename)
    except:
        if not catch_exceptions:
            raise
        logging.warn('caught exception "%s" importing %s' % (sys.exc_info()[1],filename))

        return None

    f = getattr(m, attr)
    return f

def play_games(n,seed,player_names,catch_exceptions) :
    random.seed(seed)
    logging.debug('SEED\t%s' % seed)
    players = {}
    for name in player_names:
        id = chr(ord('A') + len(players))
        logging.info('making player %s (%s) ...' % (id, name))
        file = make_player(name, catch_exceptions)
        players[id] = Player(id, name, file)

    game_num = 0
    for r in range(n):
        game_num += 1
        logging.debug('playing game %d ...' % (game_num))
        winner = nothanks.play_game(game_num, players, catch_exceptions)
        players[winner].score += 1
        logging.debug('RESULT\tgame:%d\twinner:%s' % (game_num, winner))
        for id in players:
            logging.info('SCORE\tgame %d of %d\t%s\t%s\t%d' % (game_num, n, id,
                players[id].name, players[id].score))
        logging.info('SCORE')
    return players

def main(argv) :
    if 1 == len(argv) :
        print(HELP)
        sys.exit()

    c = argv[1]

    if 0 :
        pass

    elif 'help' == c :
        print(HELP)
        sys.exit()

    elif 'play' == c :
        logging.basicConfig(level=logging.INFO,format='%(message)s',stream=sys.stdout)
        n = 1
        player_names = sys.argv[2:]
        seed = int(time.time() * 1000)
        play_games(n,seed,player_names,False)

    elif 'tournament' == c :
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)-7s %(message)s',stream=sys.stdout)
        n = int(sys.argv[2])
        player_names = sys.argv[3:]
        seed = ''.join(sys.argv)
        play_games(n,seed,player_names,True)

    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        print(HELP)
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)
