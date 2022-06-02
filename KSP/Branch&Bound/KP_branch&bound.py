# Solving Knapsack´s Problem Using B&B techniques

from node import *


def solve_branch_bound_DFS(items, capacity):
    best_val=0
    taken=[0]*len(items)
    alive=[]
    order_visiting = []

    root_node=Node(0,[],best_val,capacity)
    best_node=root_node
    alive.append(root_node)

    while alive:
        node=alive.pop()
        estimate=node.estimate(items)
        if estimate<=best_val:
            continue
        if node.value>best_val:
            best_val=node.value
            best_node = node
        if node.index >= len(items):
            continue

        rightPath= node.path.copy()
        nodeRight=Node(node.index+1,rightPath,node.value,node.room)
        alive.append(nodeRight) # If limited discrepancy technique was used -> insert(0)
        enough_room=node.room - items[node.index].weight

        if enough_room <= 0 :
            continue

        leftPath= node.path.copy()
        leftPath.append(node.index)
        nodeLeft=Node(node.index+1,leftPath,node.value+items[node.index].value,enough_room)
        alive.append(nodeLeft)

    for i in best_node.path:
        taken[items[i].index]=1
    return best_val, taken

first_line = input().split() # N items, Capacity
item_count = int(first_line[0])
capacity = int(first_line[1])

items = []
for i in range(1, item_count+1):
    parts = input().split() # CSV
    items.append(Item(i-1, int(parts[0]), int(parts[1])))


print(capacity)

value, taken= solve_branch_bound_DFS(items, capacity)

print(value, taken)