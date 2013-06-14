"""Prisoner's dilemma game, with evolution and selection
If executed without modification, instantiates 20 players who mostly defect, but the population can
be invaded by the other strategies over the 1000 'generations' iterated in the function 'evolve2'
prints out initial strategies and strategies of the 15 survivors at the end
"""

import random
import itertools
from strategies import *
from collections import defaultdict

class Player(object):
    playerlist = []
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
        ## playerlist gets modified when a player is instantiated
        self.playerlist.append(self)
        self.nextplay = None
    def addpoints(self, points):
        self.points += points

    def decideplay(self, opp):
        play = self.strat(self, opp)
        self.nextplay = play
        return play
    def makeplay(self, opp):
        play = self.nextplay
        self.allplays.append(play)
        self.plays[opp].append(play)
        return play
    def __lt__(self, other):
        return self.points < other.points
    def endgen(self):
        '''when a generation or full round is over, restore points to 0'''
        self.points = 0
    def __str__(self):
        return self.name

## game functions

## a single encounter consists of 1 game, described below
def play(player1, player2, toPrint1=False, toPrint2=False):

    ## prisoner's dilemma parameters
    defect_payoff_if_opp_cooperates = 7
    both_cooperate_payoff = 5
    both_defect_payoff = 1 # n for Nash Equilibrium

    ## debugging
    if toPrint2:
        print 'player '+str(player1.__str__())+' vs '+str(player2.__str__())
        print 'player1 points before playing ', player1.points
        print 'player2 points before playing ', player2.points
        if len(player1.allplays) >= len(Player.playerlist) - 1:
            print 'last matchup between the players', player1.plays[player2][-1], player2.plays[player1][-1]

    if player1 is player2:
        return None

    if toPrint1:

        print 'player '+player1.__str__()+'all plays=', player1.allplays
        print 'player '+player1.__str__()+'plays', player1.plays
        print 'player '+player1.__str__()+'plays against opp', player1.plays[player2]
        print 'player '+player2.__str__()+'all plays=', player2.allplays
        print 'player '+player2.__str__()+'plays', player2.plays
        print 'player '+player2.__str__()+'plays against opp', player2.plays[player1]
    ## play below
    player1.decideplay(player2)
    player2.decideplay(player1)
    player1play = player1.makeplay(player2)
    player2play = player2.makeplay(player1)
    ## assign points based on prisoner's dilemma
    if player1play == player2play == 'defect':
        player1.addpoints(both_defect_payoff)
        player2.addpoints(both_defect_payoff)
        #print 'both defect'
    elif player1play == 'defect' and player2play == 'cooperate':
        player1.addpoints(defect_payoff_if_opp_cooperates)
        #print 'first player defects, second cooperateerates'
    elif player2play == 'defect' and player1play == 'cooperate':
        player2.addpoints(defect_payoff_if_opp_cooperates)
        #print 'first player cooperateerates, second defects'
    else:
        #print 'both cooperateerate'
        player1.addpoints(both_cooperate_payoff)
        player2.addpoints(both_cooperate_payoff)
    if toPrint2:
        print 'player1 points after playing ', player1.points
        print 'player2 points after playing ', player2.points
        print '############# next match ##########'


def play_multiple_rounds(numrounds):
    for t in range(numrounds):
        players = Player.playerlist[:]
        random.shuffle(players)
        for p1, p2 in itertools.combinations(players, 2):
            play(p1, p2)

def order_players(players=Player.playerlist):
    players.sort()

## one more parameter to decide how many players 'die' after each full round (or 'generation')

def evolve1(numgens, numyears_pergen, num_players, num_die):
    '''numgens = int, number of iterations
    numyears_pergen = int, number of times each team will 'play' before the selection happens'''
    ## new team gets new name
    playernum = num_players + 1
    for i in range(numgens):
        play_multiple_rounds(numyears_pergen)
        order_players()
        for j in range(num_die):
            ## kill off the losers
            Player.playerlist.pop(0)
            ## insert randoms
            newstrat = random.choice(strat_list)
            Player(i, newstrat, num_players)
            # print 'new strategy ', newstrat
        for player in Player.playerlist:
            player.endgen()
    ## play one more generation without replacing
    play_multiple_rounds(numyears_pergen)
    order_players()
    for j in range(num_die):
        Player.playerlist.pop(0)
    for player in Player.playerlist:
        print player.strat

## incredibly variable results!!
def evolve2(numgens, numyears_pergen, num_players, num_die):
    '''boots out the losing players, replicates the winning players instead of random ones,
     and mutates each player with a fixed probability
     uncomment print statements to see it in action'''
    playernum = num_players + 1
    for i in range(numgens):
        for t in range(len(Player.playerlist)):
            if random.random() < mutation_parameter:
                Player.playerlist[t].strat = random.choice(strat_list)
                # print 'mutation!!!!'
                # print 'new strategy= ', Player.playerlist[t].strat
        play_multiple_rounds(numyears_pergen)
        order_players()
        for j in range(num_die):
            Player.playerlist.pop(0)
            newstrat = Player.playerlist[-j].strat
            Player(i, newstrat, num_players)
            # print 'new strategy = winning strategy =  ', newstrat
        for player in Player.playerlist:
            player.endgen()
    ## play one more generation without replacing
    play_multiple_rounds(numyears_pergen)
    order_players()
    for j in range(num_die):
        Player.playerlist.pop(0)
    print '#### FINAL SURVIVORS ########'
    for player in Player.playerlist:
        print player.strat

## decide which program to run
simple_simulation = False
evolution = True


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

def do_simple_simulation():
    player1 = Player(1, tit_for_tat_2)
    player2 = Player('titfortat2', tit_for_tat_2)
    player3 = Player('defect', mostly_defect)
    player4 = Player('clever', clever)
    player5 = Player('mostly random', mostlyrandomplay)
    player6 = Player('titfortat opp', tit_for_tat_opp)
    player7 = Player('mostly cooperate', mostly_cooperate)
    player8 = Player('mostly titfortat', mostly_tit_for_tat)

## for the evolution scenario
## some strategies impossible to invade, surprisingly, like tit for tat opposite
def do_evolution(numplayers):
    ## modify the initial strategy to see which strategies are prone to invasion, or make it random
    initial_strat = mostly_defect
    for i in range(numplayers):
        Player(i, initial_strat, numplayers)
    ## comment out below for long simulations
    print '####### INITIAL PLAYERS ##########'
    for player in Player.playerlist:
        print player.strat

# def evolve3(numgens, numyears_pergen):



## these results are kinda crazy. different each time. next step: run many versions of evolve2 and collect
## results in a histogram, find out distribution of results/ strategies that do well more often, etc.

if simple_simulation:
    do_simple_simulation()
if evolution:
    do_evolution(20)

evolve2(1000, 10, 20, 3)








# if __name__ == '__main__':
#
#     play_multiple_rounds(10)
#     for i in range(len(Player.playerlist)):
#         print str(Player.playerlist[i].__str__()) + '\'s'+'points=' + str(Player.playerlist[i].points) + '   ', str(Player.playerlist[i].strat)
#     order_players()
#
#
#
#
#
#

    # print str(Player.playerlist)
    #     for player in Player.playerlist:
    #     play(player2, player4)
    #     play(player2, player4)
    #     play(player4, player5)
    #     print 'player 4 plays', player4.plays
    #     print 'player 2 plays', player2.plays
    #     print 'player 5 plays', player5.plays
    #
    #
    #     print 'player2 points', player2.points
    #     print 'player 4 points', player4.points
    #     print 'player 5 points', player5.points




