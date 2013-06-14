"""Prisoner's dilemma game, with evolution and selection
If executed without modification, instantiates 20 players who mostly defect, but the population can
be invaded by the other strategies over the 1000 'generations' iterated in the function 'evolve2'
prints out initial strategies and strategies of the 15 survivors at the end
"""

import random
import itertools
import logging
from strategies import *
from collections import defaultdict

class Player(object):
    def __init__(self, name, strat, num_rounds, points=0, plays=None, allplays=None):
        '''points: stores points accrued in a single generation or set of games
        strat = strategy, defined above
        plays = dictionary of lists storing plays made against each opponent
        allplays = list of all plays made: this might be unnecessary'''
        self.name = name
        self.strat = strat
        self.points = points
        self.plays = defaultdict(list)
        if plays is not None:
            self.plays.update(plays)
        if allplays is None:
            self.allplays = []
        else:
            self.allplays = allplays
    def addpoints(self, points):
        self.points += points
    def play(self, opp):
        move = self.strat(self, opp)
        self.allplays.append(move)
        self.plays[opp].append(move)
        return move
    def __lt__(self, other):
        return self.points < other.points
    def endgen(self):
        '''when a generation or full round is over, restore points to 0'''
        self.points = 0
    def __str__(self):
        return self.name

## game functions

## a single encounter consists of 1 game, described below
def play(player1, player2):
    if player1 is player2: raise Exception("Logic error: game against self")

    ## prisoner's dilemma parameters
    defect_payoff_if_opp_cooperates = 7
    both_cooperate_payoff = 5
    both_defect_payoff = 1 # n for Nash Equilibrium

    logging.info('player '+str(player1.__str__())+' vs '+str(player2.__str__()))
    logging.info('player1 points before playing %s', player1.points)
    logging.info('player2 points before playing %s', player2.points)
    if len(player1.plays[player2]) >= 1:
        logging.info('last matchup between the players: %s %s', player1.plays[player2][-1], player2.plays[player1][-1])
    logging.debug('player %s all plays: %s', player1, player1.allplays)
    logging.debug('player %s plays: %s', player1, player1.plays)
    logging.debug('player %s plays against opp: %s', player1, player1.plays[player2])
    logging.debug('player %s all plays: %s', player2, player2.allplays)
    logging.debug('player %s plays: %s', player2, player2.plays)
    logging.debug('player %s plays against opp: %s', player2, player2.plays[player1])

    player1play = player1.play(player2)
    player2play = player2.play(player1)

    ## assign points based on prisoner's dilemma
    if player1play == player2play == 'defect':
        player1.addpoints(both_defect_payoff)
        player2.addpoints(both_defect_payoff)
    elif player1play == 'defect' and player2play == 'cooperate':
        player1.addpoints(defect_payoff_if_opp_cooperates)
    elif player2play == 'defect' and player1play == 'cooperate':
        player2.addpoints(defect_payoff_if_opp_cooperates)
    elif player2play == player1play == 'cooperate':
        player1.addpoints(both_cooperate_payoff)
        player2.addpoints(both_cooperate_payoff)
    else:
        raise Exception("bad play strings: %s %s", player1play, player2play)

    logging.info('player1 points after playing %d', player1.points)
    logging.info('player2 points after playing %d', player2.points)
    logging.info('############# next match ##########')

def play_multiple_rounds(players, numrounds):
    for t in range(numrounds):
        player_order = players[:]
        random.shuffle(player_order)
        for p1, p2 in itertools.combinations(players, 2):
            play(p1, p2)

def generation_survivors(players, rounds, num_die):
    for player in players:
        player.endgen()
    play_multiple_rounds(players, rounds)
    players.sort()
    players = players[num_die:]
    return players

def evolve1(players, numgens, numyears_pergen, num_players, num_die):
    '''numgens = int, number of iterations
    numyears_pergen = int, number of times each team will 'play' before the selection happens'''
    for generation in range(numgens):
        players = generation_survivors(players, numyears_pergen, num_die)
        players += [Player(generation, random.choice(strat_list), num_players) for _ in range(num_die)]
    return generation_survivors(players, numyears_pergen, num_die)

## incredibly variable results!!
def evolve2(players, numgens, numyears_pergen, num_players, num_die):
    '''boots out the losing players, replicates the winning players instead of random ones,
    and mutates each player with a fixed probability'''
    mutation_parameter = .2
    for generation in range(numgens):
        assert len(players) / 2 >= num_die # because otherwise this strategy doesn't work
        for player in players:
            if random.random() < mutation_parameter:
                player.strat = random.choice(strat_list)
                logging.info('mutation!! new strategy= %s', player.strat)
        players = generation_survivors(players, numyears_pergen, num_die)
        players += [Player(generation, winner.strat, num_players) for winner in players[-1:-(1+num_die):-1]]
    return generation_survivors(players, numyears_pergen, num_die)

## list with strategies to be used in simulation (modify to include more or fewer strategies)
strat_list = [mostly_tit_for_tat,
        mostly_cooperate,
        tit_for_tat_opp,
        tit_for_tat_2,
        always_defect,
        mostly_random_play,
        clever,
        mostly_defect,
        tit_for_two_tat,
        tit_for_tat_forgiving]

## define some players for a simple simulation
def get_simple_simulation_players():
    players = [Player(1, tit_for_tat_2),
               Player('titfortat2', tit_for_tat_2),
               Player('defect', mostly_defect),
               Player('clever', clever),
               Player('mostly random', mostlyrandomplay),
               Player('titfortat opp', tit_for_tat_opp),
               Player('mostly cooperate', mostly_cooperate),
               Player('mostly titfortat', mostly_tit_for_tat)]
    return players

def get_similar_players(numplayers, initial_strat):
    """num_players players all using initial_strat"""
    #For the evolution scenario some strategies impossible to invade, surprisingly, like tit for tat opposite.
    players = [Player(i, initial_strat, numplayers) for i in range(numplayers)]
    return players

## these results are kinda crazy. different each time. next step: run many versions of evolve2 and collect
## results in a histogram, find out distribution of results/ strategies that do well more often, etc.

if __name__ == '__main__':
    ## decide which program to run
    simple_simulation = False
    evolution = True

    if simple_simulation:
        do_simple_simulation()
    if evolution:
        players = get_similar_players(20, mostly_defect)
        ## modify the initial strategy to see which strategies are prone to invasion, or make it random
        print '####### INITIAL PLAYERS ##########'
        for player in players:
            print player.strat
        players = evolve2(players, 100, 10, 20, 3)
        print '#### FINAL SURVIVORS ########'
        for player in players:
            print player.strat
