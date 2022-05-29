# Sort the items, in this case, by density attribute,  and return index

from collections import namedtuple


def ksp_sort_by_density(items):
    if len(items)==1:
        return items
    left=ksp_sort_by_density(items[:len(items)//2])
    right=ksp_sort_by_density(items[len(items)//2:])
    return merge(left,right)

def merge(left,right):
    res=[]
    i=j=0
    while i<len(left) and j<len(right):
        if left[i]>right[j]:
            res.append(left[i])
            i+=1
        else:
            res.append(right[j])
            j+=1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def get_taken(densities, sorted_densities):
    taken=[]
    for i in range(0,len(densities)):
        for j in range(0, len(densities)):
            if sorted_densities[i] == densities[j]:
                taken.append(j)
    return taken


Item = namedtuple("Item", ['index', 'value', 'weight'])
first_line = input().split() # N items, Capacity
item_count = int(first_line[0])
capacity = int(first_line[1])

items = []
densities=[]
for i in range(1, item_count+1):
    parts = input().split() # CSV
    items.append(Item(i-1, int(parts[0]), int(parts[1])))
    densities.append(int(parts[0])/int(parts[1]))


sorted_items = ksp_sort_by_density(densities)
taken_items= get_taken(densities,sorted_items)
print(taken_items)