# Sort bag by value using merge sort (divide&conquer)

from collections import namedtuple


def ksp_sort_by_val(items):
    if len(items)==1:
        return items
    left=ksp_sort_by_val(items[:len(items)//2])
    right=ksp_sort_by_val(items[len(items)//2:])
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


Item = namedtuple("Item", ['index', 'value', 'weight'])

first_line = input().split() # N items, Capacity
item_count = int(first_line[0])


items = []
vals=[]
for i in range(1, item_count+1):
    parts = input().split() # CSV
    items.append(Item(i-1, int(parts[0]), int(parts[1])))
    vals.append(int(parts[0]))


sortedValues = ksp_sort_by_val(vals)


print(sortedValues)

