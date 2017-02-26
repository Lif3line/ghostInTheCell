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

distances = full([factory_count, factory_count], 99, dtype=int)

# Get distances between pairs of factories
for i in range(link_count):
    factory_1, factory_2, curDistance = [int(j) for j in input().split()]
    distances[factory_1, factory_2] = curDistance

# Mirror matrix since symetric along diagonal
for i in range(factory_count):
    for j in range(factory_count):
        distances[j, i] = distances[i, j]

# print(link_count, file=sys.stderr)
# print(distances.shape, file=sys.stderr)
print(distances, file=sys.stderr)

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

    curSourceID = -1
    curSourceCyborgs = -1

    attackSize = -1  # Number of cyborgs to send to target

    # Compute our source
    for i in range(entityCount):
        # Use our factory with the largest number of cyborgs as a source
        if entityType[i] == "FACTORY":
            if arg1[i] == 1 and curSourceCyborgs < arg2[i]:
                curSourceID = entityID[i]
                curSourceCyborgs = arg2[i]

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
                print(curValue, file=sys.stderr)
                print("Selected", file=sys.stderr)

    # Compute number of our cyborgs already heading for target
    cyborgsAttacking = 0
    for i in range(entityCount):
        if entityType[i] == "TROOP":
            if arg1[i] == 1 and arg3[i] == curTargetID:
                cyborgsAttacking = cyborgsAttacking + arg4[i]

    attackSize = min(curTargetCyborgs + 1, round(curSourceCyborgs / 2))

    # Choose actions or print("Debug messages...", file=sys.stderr)
    if curSourceID != -1 and curTargetID != -1 and attackSize >= 0:
        print("MOVE {} {} {}".format(curSourceID, curTargetID, attackSize))
        # print(";")
        # print("MSG Rusb B!")
    else:
        print("WAIT")
        print("No valid action found", file=sys.stderr)
