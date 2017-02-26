# Code for codingame Ghost in the Cell competition
# Adam Hartwell 2017

# Turn off irrelevant warning about constants vs variables
# pylint: disable=C0103
import sys
import math

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]

# Game loop
while True:
    entity_count = int(input())  # Number of entities (factories and troops)

    curTargetID = -1
    curTargetProd = -1
    curTargetCyborgs = -1

    curSourceID = -1
    curSourceCyborgs = -1

    attackSize = 5  # Number of cyborgs to send to target

    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 \
            = input().split()

        # 'FACTORY' or 'TROOP'
        entity_id = int(entity_id)
        arg_1 = int(arg_1)  # Owner (1 ally, -1 enemy, 0 neutral)
        arg_2 = int(arg_2)  # F: # cyborgs, T: id of last factory visited
        arg_3 = int(arg_3)  # F: production val, T: id of target factory
        arg_4 = int(arg_4)  # F: N/A, T: # cyborgs in troop
        arg_5 = int(arg_5)  # F: N/A, T: # turns until destination

        # Target the factory with highest production not already owned by us
        if entity_type == "FACTORY":
            if curTargetProd < arg_3 and arg_1 != 1:
                curTargetID = entity_id
                curTargetProd = arg_3
                curTargetCyborgs = arg_2

        # Use our factory with the largest number of cyborgs as a source
        if entity_type == "FACTORY":
            if curSourceCyborgs < arg_2 and arg_1 == 1:
                curSourceID = entity_id
                curSourceCyborgs = arg_2

    # Choose actions - print("MOVE source destination cyborgCount")
    # or print("WAIT") or print("Debug messages...", file=sys.stderr)
    print("MOVE {} {} {}".format(curSourceID, curTargetID, attackSize))
