# Cycle Crossover Method
def cycle_cross_def(p1,p2):
    elementsChecked = 1
    cycleNum = 1
    cycles = [0] * len(p1)
    cycles[0] = cycleNum
    child = [0]*len(p1)
    i = 0
    j = 0
    while elementsChecked < len(p1):
        if p1[i] == p2[j]:
            cycles[j]=cycleNum
            i = j
            j = 0
            elementsChecked += 1
        j += 1
        if j == len(p1) and elementsChecked < len(p1):
            j=0
            for k in range(len(p1)):
                if cycles[k] == 0:
                    i=k
                    cycleNum+=1
                    cycles[k]=cycleNum
                    elementsChecked += 1
                    break

    for k in range(len(cycles)):
        if cycles[k] % 2==0: # Even cycle picks mother genes
            child[k]=p2[k]
        else: # Odd cycle picks mother genes
            child[k]=p1[k]
    return child,cycles

p1=['h','k','c','e','f','d','b','l','a','i','g','j']
p2=['a','b','c','d','e','f','g','h','i','j','k','l']

child,cycle= cycle_cross_def(p1,p2)
print(child)
