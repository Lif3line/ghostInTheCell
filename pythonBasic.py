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

    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 \
            = input().split()

        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    print("WAIT")
