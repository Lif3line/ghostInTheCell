# Code for codingame Ghost in the Cell competition
# Adam Hartwell 2017

# Turn off irrelevant warning about constants vs variables
# pylint: disable=C0103

import sys
from numpy import full


def getFactoryValue(distance, production):
    return production / distance


factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
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
    entityCount = int(input())  # Number of entities (factories and troops)
    entityID = []
    entityType = []
    arg1 = []
    arg2 = []
    arg3 = []
    arg4 = []
    arg5 = []
    for i in range(entityCount):
        out1, out2, out3, out4, out5, out6, out7 = input().split()
        entityID.append(int(out1))
        entityType.append(out2)  # 'FACTORY' or 'TROOP'
        arg1.append(int(out3))  # Owner (1 ally, -1 enemy, 0 neutral)
        arg2.append(int(out4))  # F: # cyborgs, T: id of last factory visited
        arg3.append(int(out5))  # F: production val, T: id of target factory
        arg4.append(int(out6))  # F: # turns till prod., T: # cyborgs in troop
        arg5.append(int(out7))  # F: N/A, T: # turns until destination

    curTargetID = -1
    curTargetProd = -1
    curTargetCyborgs = -1
    curTargetValue = -1
    curTargetOwner = -2
    curSecTargetID = -1
    curSecTargetProd = -1
    curSecTargetDistance = 9999

    curSourceID = -1
    curSourceCyborgs = -1
    curSecSourceID = -1
    curSecSourceCyborgs = -1

    attackSize = -1  # Number of cyborgs to send to target
    secAttackSize = 1

    # Compute our source
    for i in range(entityCount):
        # Use our factory with the largest number of cyborgs as a source
        if entityType[i] == "FACTORY":
            if arg1[i] == 1 and curSourceCyborgs < arg2[i]:
                curSourceID = entityID[i]
                curSourceCyborgs = arg2[i]
    # Compute our sources
    for i in range(entityCount):
        # Use our factory with the largest number of cyborgs as a source
        if entityType[i] == "FACTORY":
            if arg1[i] == 1 and curSourceCyborgs < arg2[i]:
                curSecSourceID = curSourceID
                curSecSourceCyborgs = curSourceCyborgs
                

    # Compute target
    # Target the factory with highest production not already owned by us
    # Subselect by distance
    for i in range(entityCount):
        if entityType[i] == "FACTORY":
            curValue = getFactoryValue(distances[curSourceID, entityID[i]],
                                       arg3[i])
            if (arg1[i] != 1 and
                    entityID[i] != curSourceID and  # Prevents bug when backcap
                    curValue > curTargetValue):
                curTargetID = entityID[i]
                curTargetProd = arg3[i]
                curTargetCyborgs = arg2[i]
                curTargetValue = curValue
                curTargetOwner = arg1[i]

    # Compute number of our cyborgs already heading for target
    cyborgsAttacking = 0
    cyborgsMovingToDefend = 0
    incomingCyborgs = 0
    for i in range(entityCount):
        if entityType[i] == "TROOP":
            # Our cyborgs that are already attacking the target
            if arg1[i] == 1 and arg3[i] == curTargetID:
                cyborgsAttacking = cyborgsAttacking + arg4[i]

            # Their cyborgs moving to defend
            if arg1[i] == -1 and arg3[i] == curTargetID:
                cyborgsMovingToDefend = cyborgsMovingToDefend + arg4[i]

            # Cyborgs looking to attack our source
            if arg1[i] == -1 and arg3[i] == curSourceID:
                incomingCyborgs = incomingCyborgs + arg4[i]

    cyborgsDefending = cyborgsMovingToDefend + curTargetCyborgs

    # Conquer size for enemy
    minConquerSize = cyborgsDefending - cyborgsAttacking + 1
    if curTargetOwner == -1:
        prodDuringTravel = ((distances[curSourceID, curTargetID] + 1) *
                            curTargetProd)
        minConquerSize += prodDuringTravel

    attackSize = min(minConquerSize, curSourceCyborgs - incomingCyborgs)

    print(curSourceCyborgs - incomingCyborgs, file=sys.stderr)
    #compute collateral target
    # Target the closest neutral factory with prod > 0
    for i in range(entityCount):
        if entityType[i] == "FACTORY":
            if (arg1[i] == 0 and distances[curSecSourceID, entityID[i]] < curSecTargetDistance):
                curSecTargetID = entityID[i]
                curSecTargetDistance = distances[curSecSourceID, entityID[i]]
    
    mainAttackString = ""
    secAttackString = ""
    # Choose actions or print("Debug messages...", file=sys.stderr)
    if curSourceID != -1 and curTargetID != -1 and mainAttackSize >= 0:
        mainAttackString = "MOVE {} {} {}".format(curSourceID, curTargetID, mainAttackSize)
        if curSecSourceID != -1 and curSecTargetID != -1 and secAttackSize >= 0:
            secAttackString = ";MOVE {} {} {}".format(curSecSourceID, curSecTargetID, secAttackSize)
        # print("MSG Rusb B!")
        print(mainAttackString + secAttackString)
    if curSourceID != -1 and curTargetID != -1 and attackSize >= 0:
        print("MOVE {} {} {}".format(curSourceID, curTargetID, attackSize))
        # print(";")
        # print("MSG Rusb B!")
    else:
        print("WAIT")
        print("""No valid action found
                 curSourceID: {}
                 curTargetID: {}
                 mainAttackSize: {}
                 curSecSourceID: {}
                 curSecTargetID: {}
                 secAttackSize: {}
                 """.format(curSourceID, curTargetID, mainAttackSize,curSecSourceID, curSecTargetID, secAttackSize), file=sys.stderr)
