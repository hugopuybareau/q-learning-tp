# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
    * Please read learningAgents.py before reading this.*

    A ValueIterationAgent takes a Markov decision process
    (see mdp.py) on initialization and runs value iteration
    for a given number of iterations using the supplied
    discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.

        Some useful mdp methods you will use:
            mdp.getStates()
            mdp.getPossibleActions(state)
            mdp.getTransitionStatesAndProbs(state, action)
            mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        if self.iterations == -1:
            self.runValueIterationCv()
            print(f"{self.iterations} iterations to converge")
        else:
            self.runValueIteration(self.iterations)

    def runValueIteration(self, iter):
        """
        Run the indicated number of iterations
        """
        for _ in range(iter):
            new_values = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    new_values[state] = 0
                else:
                    max_q_value = float("-inf")
                    actions = self.mdp.getPossibleActions(state)
                    for action in actions:
                        q_value = self.getQValue(state, action)
                        if q_value > max_q_value:
                            max_q_value = q_value
                    new_values[state] = max_q_value
            self.values = new_values

    def runValueIterationCv(self):
        """
        Run until convergence
        """
        threshold = 1e-6
        self.iterations = 0
        while True:
            self.iterations += 1
            diff = 0
            new_values = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    new_values[state] = 0
                else:
                    max_q_value = float("-inf")
                    actions = self.mdp.getPossibleActions(state)
                    for action in actions:
                        q_value = self.getQValue(state, action)
                        if q_value > max_q_value:
                            max_q_value = q_value

                    new_values[state] = max_q_value
                    diff = max(diff, abs(new_values[state] - self.values[state]))
            self.values = new_values
            if diff < threshold:
                break

    def getValue(self, state):
        """
        Return the value of the state
        """
        return self.values[state]

    def getQValue(self, state, action):
        """
        The q-value of the state action pair
        (after the indicated number of value iteration
        passes).
        """
        q_value = 0
        transition_and_probs = self.mdp.getTransitionStatesAndProbs(state, action)

        for next, prob in transition_and_probs:
            q_value += prob * (
                self.mdp.getReward(state, action, next)
                + self.discount * self.values[next]
            )
        return q_value

    def getPolicy(self, state):
        """
        The policy is the best action in the given state
        according to the values computed by value iteration.
        You may break ties any way you see fit.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        if not actions:  # terminal state
            return None

        best_action = None
        best_q_value = float("-inf")

        for action in actions:
            q_value = self.getQValue(state, action)
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = action

        return best_action

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
