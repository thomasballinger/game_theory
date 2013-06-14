import random

## variables to be used in stochastic strategies
percentagecooperate = 0.7
percentagedefect = 0.9
percentage_tit_for_tat = 0.9
tit_for_tat_param = 0.1
mutation_parameter = 0.02

## strategies
def mostly_random_play(player1,player2):
    ## check if last three plays by the opponent against you were defect
    if player2.plays[player1.index][-3:] == ['defect','defect','defect']:
        return 'defect'
    else:
        l = ['cooperate','defect']
        return random.choice(l)

def always_cooperate(player1,player2):
    return 'cooperate'

def clever(player1,player2):
    ## check if last two plays were cooperate. if so, take advantage!
    if player2.plays[player1.index][-2:] == ['cooperate','cooperate']:
        return 'defect'
    ## if opponent appears to be a defector, don't cooperate
    elif player2.plays[player1.index][-2:] == ['defect','defect']:
        return 'defect'
    else:
        return 'cooperate'

def always_defect(player1,player2):
    return 'defect'

def mostly_defect(player1,player2):
    if random.random() < percentagedefect:
        return 'defect'
    else:
        return 'cooperate'


def tit_for_tat_1(player1,player2):
    '''smart tit for tat, can see player's last move against any opponent'''
    ## not using this strategy in simulation below
    if len(player2.allplays) == 0:
        return 'cooperate'
    elif player2.allplays[-1] == 'cooperate':
        return 'cooperate'
    elif player2.allplays[-1] == 'defect':
        return 'defect'
    else:
        raise 'second player index error, t for t 1'

def tit_for_tat_2(player1,player2):
    '''traditional tit for tat, plays whatever opponent last played against you'''
    if player2.plays[player1.index] == []:
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'cooperate':
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'defect':
        return 'defect'


def tit_for_tat_opp(player1,player2):
    '''opposite of tit for tat, with exceptions'''
    ## initial play
    if player2.plays[player1.index] == []:
        l = ['cooperate','defect']
        play = random.choice(l)
        return play
    ## if opponent is a serial defector, don't cooperate
    elif player2.plays[player1.index][-2:] == ['defect','defect']:
        return 'defect'
    ## otherwise, do the opposite of tit for tat
    elif player2.plays[player1.index][-1] == 'cooperate':
        return 'defect'
    elif player2.plays[player1.index][-1] == 'defect':
        return 'cooperate'


def mostly_cooperate(player1,player2):
    ## check for serial defector
    if player2.plays[player1.index][-3:] == ['defect','defect','defect']:
        return 'defect'
    ## otherwise, cooperate stochastically
    elif random.random() <  percentagecooperate:
        return 'cooperate'
    else:
        return 'defect'

def mostly_tit_for_tat(player1,player2):
    if random.random() < percentage_tit_for_tat:
        return tit_for_tat_2(player1,player2)
    else:
        return 'defect'

def tit_for_two_tat(player1,player2):
    '''more forgiving'''
    if len(player2.plays[player1.index]) <= 1:
        return 'cooperate'
    elif player2.plays[player1.index][-2:] == ['defect','defect']:
        return 'defect'
    else:
        return 'cooperate'

def tit_for_tat_forgiving(player1,player2):
    if player2.plays[player1.index] == []:
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'cooperate':
        return 'cooperate'
    elif player2.plays[player1.index][-1] == 'defect':
        if random.random() < tit_for_tat_param:
            return 'cooperate'
        else:
            return 'defect'

