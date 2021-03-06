from random import choice
import numpy
import specmine

class QFunctionPolicy(object):
    def __init__(self, domain, q_values):
        self._domain = domain
        self._q_values = q_values

    def __getitem__(self, state):
        return \
            max(
                self._domain.actions_in(state),
                key = lambda a: self._q_values[(state, a)],
                )

class LinearValueFunction:
    def __init__(self, features, weights = None):
        self.features = features
        self.weights = weights

    def __getitem__(self, state):
        # TODO add interpolation to unseen states
        phi = self.features[state] # returns a vector of feature values

        if self.weights is None:
            self.weights = numpy.zeros_like(phi)

        return numpy.dot(phi, self.weights)

class StateValueFunctionPolicy:
    def __init__(self, domain, value_function, epsilon = 0.0):
        self.domain = domain
        self.values = value_function 
        self.epsilon = epsilon

    def __getitem__(self,state):
        if numpy.random.random() < self.epsilon:
            best_moves = list(self.domain.actions_in(state))
        else:
            max_value = None
            for action in self.domain.actions_in(state):
                after_state = self.domain.outcome_of(state,action)
                value = self.values[after_state]

                if value > max_value:
                    best_moves = [action]
                    max_value = value
                elif value == max_value:
                    best_moves.append(action) 

        # choose randomly among the moves of highest value
        return choice(best_moves)

class RandomPolicy:
    def __init__(self, domain):
        self.domain = domain

    def __getitem__(self,state):
        return choice(list(self.domain.actions_in(state)))

class ExpertGoPolicy:
    def __init__(self,sgf_file,player):
        self.gen = specmine.go.sgf_game_reader(sgf_file) 
        self.player = player
        if self.player == -1:
            self.gen.next()

    def __getitem__(self,state):
        move = (None,None)
        try:
            move = self.gen.next()
            self.gen.next() # skip opponents move (inefficient?)
            return move

        except StopIteration:
            return move
        
