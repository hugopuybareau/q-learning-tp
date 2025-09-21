# featureExtractors.py
# --------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"Feature extractors for Pacman game states"

from game import Actions
import util


class FeatureExtractor:
    def getFeatures(self, state, action):
        """
        Returns a dict from features to counts
        Usually, the count will just be 1.0 for
        indicator functions.
        """
        util.raiseNotDefined()


class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state, action)] = 1.0
        return feats


def closestFood(pos, food, walls):
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist + 1))
    # no food found
    return None


class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum(
            (next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts
        )

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features


class ExpertExtractor(FeatureExtractor):
    """
    Returns expert features considering capsules.
    """

    def getFeatures(self, state, action):
        features = util.Counter()
        features["bias"] = 1.0 # 1

        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # action eats food?
        features["ghosts-1-step-away"] = sum( # 2
            (next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts
        )

        # eat food if no ghost 1 step away
        if not features["ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1 # 3

        # distance to closest food
        distance = closestFood((next_x, next_y), food, walls)
        if distance is not None:
            features["closest-food"] = float(distance) / (walls.width * walls.height) # 4

        # closest capsule
        capsules = state.getCapsules()
        if capsules:
            capsuleDists = [util.manhattanDistance((next_x, next_y), cap) for cap in capsules] # pacman moves manhattan distance to capsules
            features["closest-capsule"] = min(capsuleDists) / (walls.width * walls.height) # 5
        else:
            features["closest-capsule"] = 0

        if (next_x, next_y) in capsules:
            features["eats-capsule"] = 1 # 6

        # feat : ghosts management
        ghostStates = state.getGhostStates()
        scaredGhosts = [g for g in ghostStates if g.scaredTimer > 0]
        normalGhosts = [g for g in ghostStates if g.scaredTimer == 0]

        # print(normalGhosts)
        # print(scaredGhosts)

        if scaredGhosts:
            scaredPositions = [g.getPosition() for g in scaredGhosts]
            scaredDists = [util.manhattanDistance((next_x, next_y), pos) for pos in scaredPositions]
            features["closest-scared-ghost"] = min(scaredDists) / (walls.width * walls.height) # 7

            # eat the ghost if possible
            for pos in scaredPositions:
                if (next_x, next_y) == pos:
                    features["eats-scared-ghost"] = 1 # 8

        if normalGhosts:
            normalPositions = [g.getPosition() for g in normalGhosts]
            normalDists = [util.manhattanDistance((next_x, next_y), pos) for pos in normalPositions]
            closestNormalDist = min(normalDists) if normalDists else 10
            
            # malus if too close to normal ghost
            if closestNormalDist <= 1:
                features["danger-normal-ghost"] = 1 # 9
            elif closestNormalDist <= 2:
                features["danger-normal-ghost"] = 0.5

        # features.divideAll(len(features) - 1) # faut normaliser sinon les features avec des grosses valeurs dominent
        return features
