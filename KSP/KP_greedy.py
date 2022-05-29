# There is a bag with items, every item has a value and a weight.
# The goal is to find the maximum value that fits in the bag given a capacity.

from collections import namedtuple


def ksp_greedy(items, capacity, taken):
    res=0
    for item in items:
        if (capacity-item.weight>=0):
            res+=item.value
            taken[item.index]=1
            capacity-=item.weight
    return res, taken

Item = namedtuple("Item", ['index', 'value', 'weight'])

first_line = input().split() # N items, Capacity
item_count = int(first_line[0])
capacity = int(first_line[1])


items = []
for i in range(1, item_count+1):
    parts = input().split() # CSV
    items.append(Item(i-1, int(parts[0]), int(parts[1])))

taken = [0]*len(items)

max_value, taken = ksp_greedy(items, capacity, taken)

print(max_value, taken)

