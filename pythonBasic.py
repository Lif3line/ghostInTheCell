# Code for codingame Ghost in the Cell competition
# Adam Hartwell 2017

# Turn off irrelevant warning about constants vs variables
# pylint: disable=C0103

# For convenience IDs == indices

import sys
from numpy import full

# Multipliers for target valuation
VICTORY_MOD = 0
DIST_CUTOFF = 7


def getFactoryValue(sources, sourceStrs, target):
    """Return a heuristic valuation of a target"""
    minDistance = 99
    for ss in sources:
        if distances[ss][target] < minDistance:
            minDistance = distances[ss][target]

    # Cyborgs heading there from other attacks this turn
    cyborgsAttacking = cyborgAttackVectors[target]

    cyborgsMovingToDefend = 0
    for ii in range(numTroops):
        # Our cyborgs that are already attacking the target
        if troops[1][ii] == 1 and troops[3][ii] == target:
            cyborgsAttacking += troops[4][ii]

        # Their cyborgs moving to defend
        if troops[1][ii] == -1 and troops[3][ii] == target:
            cyborgsMovingToDefend += troops[4][ii]

    minConquerSize = (cyborgsMovingToDefend + factories[2][target] -
                      cyborgsAttacking + 1 + VICTORY_MOD)

    if factories[1][target] == -1:
        prodDuringTravel = ((minDistance + 1) * factories[3][target])
        minConquerSize += prodDuringTravel

    if sum(sourceStrs) > minConquerSize:
        return -1

    valuation = 0
    for ii, _ in enumerate(sources):
        if distances[ii][target] < DIST_CUTOFF:
            valuation += ((min(sourceStrs[ii] - factories[2][target], 1) *
                           factories[3][target]) /
                          distances[sources[ii]][target])

    return valuation


def getEntities():
    """Get all entities on the field"""
    entityCount = int(input())  # Number of entities (factories and troops)
    factoryInfo = [[] for i in range(5)]
    troopInfo = [[] for i in range(6)]
    bombInfo = [[] for i in range(5)]

    factoryCount = 0
    troopCount = 0
    bombCount = 0

    for _ in range(entityCount):
        ID, entitityType, arg1, arg2, arg3, arg4, arg5 = input().split()

        if entitityType == "FACTORY":
            factoryInfo[0].append(int(ID))  # ID
            factoryInfo[1].append(int(arg1))  # Owner
            factoryInfo[2].append(int(arg2))  # # Cyborgs
            factoryInfo[3].append(int(arg3))  # Production
            factoryInfo[4].append(int(arg4))  # Turns until production
            factoryCount += 1

        elif entitityType == "TROOP":
            troopInfo[0].append(int(ID))  # ID
            troopInfo[1].append(int(arg1))  # Owner
            troopInfo[2].append(int(arg2))  # Source factory ID
            troopInfo[3].append(int(arg3))  # Target factory ID
            troopInfo[4].append(int(arg4))  # Number of cyborgs
            troopInfo[5].append(int(arg5))  # Time until arrival
            troopCount += 1

        elif entitityType == "BOMB":
            bombInfo[0].append(int(ID))  # ID
            bombInfo[1].append(int(arg1))  # Owner
            bombInfo[2].append(int(arg2))  # Source factory ID
            bombInfo[3].append(int(arg3))  # Target factory ID
            bombInfo[4].append(int(arg4))  # Number of cyborgs
            bombCount += 1

    return (factoryInfo, troopInfo, bombInfo,
            factoryCount, troopCount, bombCount)


def computeBestTarget(sourceID):
    """Compute the current optimal target from one of our factories"""
    targetValue = -1
    curTargetIndex = -1

    for ii in range(numFactories):
        if factories[1][ii] != 1:
            curValue = \
                getFactoryValue(distances[sourceID, factories[0][ii]],
                                factories[3][ii],
                                factories[2][ii])

            if curValue > targetValue:
                targetValue = curValue
                curTargetIndex = ii

    return curTargetIndex


def computeSpareCyborgs(factoryID):
    """Compute the number of cyborgs we have to spare on a factory"""
    # TODO: add compensation for time until attack
    incomingCyborgs = 0
    incomingDefense = 0
    for ii in range(numTroops):
        if troops[1][ii] == -1 and troops[3][ii] == factoryID:
            incomingCyborgs += troops[4][ii]

        # Friendlies moving to defense
        if troops[1][ii] == 1 and troops[3][ii] == factoryID:
            incomingDefense += troops[4][ii]

    return (factories[2][factoryID] - incomingCyborgs +
            incomingDefense - cyborgsInUse[factoryID])


def computeCyborgsToCap(sourceID, targetID):
    """Compute the number of cyborgs needed to take a factory"""

    # Cyborgs heading there from other attacks this turn
    cyborgsAttacking = cyborgAttackVectors[targetID]

    cyborgsMovingToDefend = 0
    for ii in range(numTroops):
        # Our cyborgs that are already attacking the target
        if troops[1][ii] == 1 and troops[3][ii] == targetID:
            cyborgsAttacking += troops[4][ii]

        # Their cyborgs moving to defend
        if troops[1][ii] == -1 and troops[3][ii] == targetID:
            cyborgsMovingToDefend += troops[4][ii]

    defenceTotal = cyborgsMovingToDefend + factories[2][targetID]
    conquerSize = defenceTotal - cyborgsAttacking + 1

    # Account for production on enemy factories
    if factories[1][targetID] == -1:
        prodDuringTravel = ((distances[sourceID, targetID] + 1) *
                            factories[3][targetID])
        conquerSize += prodDuringTravel

    return conquerSize


bombsRemaining = 2
turn = 0
neutralsTaken = False  # Flag for if useful neutrals are all taken

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories

distances = full([factory_count, factory_count], 99, dtype=int)

maxDist = 0
for i in range(link_count):
    factory_1, factory_2, curDistance = [int(j) for j in input().split()]
    distances[factory_1, factory_2] = curDistance
    if curDistance > maxDist:
        maxDist = curDistance

# Mirror matrix since symetric along diagonal
for i in range(factory_count):
    for j in range(factory_count):
        distances[j, i] = distances[i, j]

print(distances, file=sys.stderr)

# Game loop
while True:
    # Get details of all entities, must be here since taking input
    factories, troops, bombs, numFactories, numTroops, numBombs = getEntities()
    commandString = ""

    # Check to see if all neutrals are taken (mid game)
    if not neutralsTaken:
        neutralsTaken = True  # Assume is true: prove false
        for i in range(numFactories):
            if factories[1][i] == 0 and factories[3][i] > 0:
                neutralsTaken = False

    # Track cyborgs actions generated by previous commands this turn
    cyborgsInUse = full([factory_count], 0, dtype=int)
    cyborgAttackVectors = full([factory_count], 0, dtype=int)

    # Compute which factories can source or need defending
    possibleSources = []
    factoriesThreatened = []
    for i in range(numFactories):
        strength = computeSpareCyborgs(i)
        if factories[1][i] == 1 and strength > 0:
            possibleSources.append(i)
        elif factories[1][i] == 1 and strength < 0:
            factoriesThreatened.append(i)

    # Move to defend first
    for threatened in factoriesThreatened:
        closeSources = sorted(possibleSources,
                              key=lambda ss, i=threatened: (distances[i, ss]))
        defecit = -computeSpareCyborgs(threatened)
        for source in closeSources:
            sourceSpares = computeSpareCyborgs(source)

            cyborgsToSend = min(sourceSpares, defecit)

            defecit -= cyborgsToSend

            cyborgsInUse[source] += cyborgsToSend
            commandString += "MOVE {} {} {};".format(source,
                                                     threatened,
                                                     cyborgsToSend)
            # print("Sending defense from {} to {}, {} cyborgs".format(source, threatened, cyborgsToSend), file=sys.stderr)
            if defecit < 0:
                break

    # Early spreading
    if not neutralsTaken:
        for i in range(numFactories):  # Sources i
            if factories[1][i] == 1:
                for j in range(numFactories):  # targets j
                    if (factories[1][j] != 1 and
                        factories[3][j] > 0 and
                            distances[i][j] < maxDist / 2):
                        attSize = computeCyborgsToCap(i, j)
                        spareCyborgs = computeSpareCyborgs(i)

                        if attSize > 0 and attSize <= spareCyborgs:
                            commandString += "MOVE {} {} {};".format(i,
                                                                     j,
                                                                     attSize)
                            cyborgsInUse[i] += attSize
                            cyborgAttackVectors[j] += attSize

    # Mid-late game sniping
    else:
        # Re-calculate sources
        possibleSources = []
        sourceStr = []
        tpList = []
        for i in range(numFactories):
            strength = computeSpareCyborgs(i)
            if factories[1][i] == 1 and strength > 0:
                possibleSources.append(i)
                sourceStr.append(strength)
                tpList.append((i, strength))

        bestTarget = (-1, 0)  # ID, value
        for i in range(numFactories):
            if factories[1][i] != 1:
                value = getFactoryValue(possibleSources, sourceStr, i)
                if value > bestTarget[1]:
                    bestTarget = (i, value)

        # Do attack:D
        if bestTarget[0] != -1:
            biggestSources = sorted(tpList, key=lambda s: (s[1]))

            for source in biggestSources:
                if distances[source[0], bestTarget[0]] < DIST_CUTOFF:
                    numLeftToCap = computeCyborgsToCap(source[0], bestTarget[0]) + VICTORY_MOD
                    sourceSpares = computeSpareCyborgs(source[0])

                    cyborgsToSend = min(sourceSpares, numLeftToCap)

                    numLeftToCap -= cyborgsToSend

                    # cyborgsInUse[source[0]] += cyborgsToSend
                    # cyborgAttackVectors[bestTarget[0]] += cyborgsToSend
                    # commandString += "MOVE {} {} {};".format(source[0],
                    #                                          bestTarget[0],
                    #                                          cyborgsToSend)
                    # print("Sending attack from {} to {}, {} cyborgs".format(source[0], bestTarget[0], cyborgsToSend), file=sys.stderr)
                    if numLeftToCap < 0:
                        break

        # Bombing logic
        if bombsRemaining > 0:
            if bestTarget[0] != -1:
                alreadyAttacking = False
                for i in range(numBombs):
                    if bombs[3][i] == bestTarget[0]:
                        alreadyAttacking = True

                if not alreadyAttacking:
                    shortestDist = 99
                    bomberID = -1
                    for i in range(numFactories):  # Send from closest factory
                        if (factories[1][i] == 1 and
                                distances[i][bestTarget[0]] < shortestDist):
                            shortestDist = distances[i][bestTarget[0]]
                            bomberID = i

                    commandString += "BOMB {} {};".format(bomberID, bestTarget[0])
                    bombsRemaining -= 1

    # Upgrading logic (more than x spare)
    for i in range(numFactories):
        if (factories[1][i] == 1 and
            factories[3][i] < 3 and
                computeSpareCyborgs(i) >= 10):
            commandString += "INC {};".format(i)
            cyborgsInUse[i] += 10

    # Print out command(s) as appropriate
    if commandString:
        if turn < 8:
            commandString += "MSG Rush B;"
        print(commandString[:-1])  # Remove trailing ;
    else:
        if turn < 8:
            print("MSG Rush B;WAIT")
        else:
            print("WAIT")

    turn += 1
