# Node Class to build tree DS and implement B&B algorithms

from pprint import pformat
from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])


class Node:
    def __init__(self, index, path, value, room):
        self.index = index
        self.path = path
        self.value = value
        self.room = room

    def __repr__(self):
        return pformat(vars(self))

    def estimate(self, items):
        return self.value + sum(item.value for item in items[self.index:])


def from_data_to_items(input_data):
    lines = input_data.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    items = []
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    return items, capacity


def check_solution(capacity, items, taken):
    weight = 0
    value = 0
    for item in items:
        if taken[item.index] == 1:
            weight += item.weight
            value += item.value
    if weight > capacity:
        print("Solución incorrecta, se supera la capacidad de la mochila (capacity, weight):", capacity, weight)
        return 0
    return value
