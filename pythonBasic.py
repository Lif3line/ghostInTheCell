# Code for codingame Ghost in the Cell competition
# Adam Hartwell 2017

# Turn off irrelevant warning about constants vs variables
# pylint: disable=C0103

import sys
from numpy import full


def getFactoryValue(distance, production):
    """Return a heuristic valuation of a target"""
    return production / distance


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


factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories

distances = full([factory_count, factory_count], 99, dtype=int)

for i in range(link_count):
    factory_1, factory_2, curDistance = [int(j) for j in input().split()]
    distances[factory_1, factory_2] = curDistance

# Mirror matrix since symetric along diagonal
for i in range(factory_count):
    for j in range(factory_count):
        distances[j, i] = distances[i, j]

# print(link_count, file=sys.stderr)
# print(distances.shape, file=sys.stderr)
# print(distances, file=sys.stderr)

# Game loop
while True:
    factories, troops, bombs, numFactories, numTroops, numBombs = getEntities()

    curTargetID = -1
    curTargetProd = -1
    curTargetCyborgs = -1
    curTargetValue = -1
    curTargetOwner = -2
    curSourceID = -1
    curSourceCyborgs = -1

    curSecTargetID = -1
    curSecTargetProd = -1
    curSecTargetDistance = 9999
    curSecSourceID = -1
    curSecSourceCyborgs = -1
    secAttackSize = 1

    # Compute our sources
    for i in range(numFactories):
        # Use our factory with the largest number of cyborgs as a source
        if factories[1][i] == 1 and curSourceCyborgs < factories[2][i]:
            curSecSourceID = curSourceID
            curSecSourceCyborgs = curSourceCyborgs

            curSourceID = factories[0][i]
            curSourceCyborgs = factories[2][i]

    # Compute main target
    # Target the factory with highest production not already owned by us
    # Subselect by distance
    for i in range(numFactories):
        curValue = getFactoryValue(distances[curSourceID, factories[0][i]],
                                   factories[3][i])
        if (factories[1][i] != 1 and
                factories[0][i] != curSourceID and  # Prevents bug when backcap
                curValue > curTargetValue):
            curTargetID = factories[0][i]
            curTargetProd = factories[3][i]
            curTargetCyborgs = factories[2][i]
            curTargetValue = curValue
            curTargetOwner = factories[1][i]

    # Compute number of our cyborgs already heading for target
    cyborgsAttacking = 0
    cyborgsMovingToDefend = 0
    incomingCyborgs = 0
    for i in range(numTroops):
        # Our cyborgs that are already attacking the target
        if troops[1][i] == 1 and troops[3][i] == curTargetID:
            cyborgsAttacking = cyborgsAttacking + troops[4][i]

        # Their cyborgs moving to defend
        if troops[1][i] == -1 and troops[3][i] == curTargetID:
            cyborgsMovingToDefend = cyborgsMovingToDefend + troops[4][i]

        # Cyborgs looking to attack our source
        if troops[1][i] == -1 and troops[3][i] == curSourceID:
            incomingCyborgs = incomingCyborgs + troops[4][i]

    cyborgsDefending = cyborgsMovingToDefend + curTargetCyborgs

    # Conquer size for enemy
    minConquerSize = cyborgsDefending - cyborgsAttacking + 1
    if curTargetOwner == -1:
        prodDuringTravel = ((distances[curSourceID, curTargetID] + 1) *
                            curTargetProd)
        minConquerSize += prodDuringTravel

    attackSize = min(minConquerSize, curSourceCyborgs - incomingCyborgs)

    print(curSourceCyborgs - incomingCyborgs, file=sys.stderr)

    # Compute collateral target
    # Target the closest neutral factory with prod > 0
    for i in range(numFactories):
        if (factories[1][i] == 0 and
                distances[curSecSourceID, factories[0][i]] <
                curSecTargetDistance):
            curSecTargetID = factories[0][i]
            curSecTargetDistance = distances[curSecSourceID, factories[0][i]]

    mainAttackString = ""
    secAttackString = ""
    # Choose actions or print("Debug messages...", file=sys.stderr)
    if curSourceID != -1 and curTargetID != -1 and attackSize >= 0:
        mainAttackString = "MOVE {} {} {}".format(curSourceID,
                                                  curTargetID,
                                                  attackSize)
        if (curSecSourceID != -1 and
                curSecTargetID != -1 and
                secAttackSize >= 0):
            secAttackString = ";MOVE {} {} {}".format(curSecSourceID,
                                                      curSecTargetID,
                                                      secAttackSize)
        print(mainAttackString + secAttackString)
    else:
        print("WAIT")
        print("WAIT")
        print("No valid action found", file=sys.stderr)
        print("""No valid action found
                 curSourceID: {}
                 curTargetID: {}
                 attackSize: {}
                 curSecSourceID: {}
                 curSecTargetID: {}
                 secAttackSize: {}
                 """.format(curSourceID,
                            curTargetID,
                            attackSize,
                            curSecSourceID,
                            curSecTargetID,
                            secAttackSize),
              file=sys.stderr)
