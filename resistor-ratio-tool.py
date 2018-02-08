## Neil Thistlethwaite, 2017
import sys
from bisect import bisect_left
import json

resistor_sets_filename = "resistor-sets.json"
## Resistor Sets
print("Loading resistor sets...")
resistor_sets = None
try:
    with open(resistor_sets_filename, "r") as f:
        resistor_sets = json.loads(f.read())
except:
    print("Error loading JSON file `%s`" % resistor_sets_filename)
    sys.exit(1)

def findresistors(ratio, resset=resistor_sets["E96"]):
    resset = [x for x in resset]
    checkset = [x for x in resset]
    if ratio<1:
        ratio = 1/ratio
    maxideal = resset[-1]*ratio
    ctmp = [x for x in resset]
    while maxideal >= checkset[-2]:
        ctmp = [10*x for x in ctmp]
        checkset.extend([x for x in ctmp])
    print(len(checkset))
    bestpair = (1,checkset[0],checkset[0])
    for res in resset:
        ideal = ratio*res
        cinx = bisect_left(checkset, ideal)
        rr1 = checkset[cinx-1]/res
        rr2 = checkset[cinx]/res
        if(abs(bestpair[0]-ratio) > abs(rr1-ratio)):
            bestpair = (rr1, checkset[cinx-1], res)
        if(abs(bestpair[0]-ratio) > abs(rr2-ratio)):
            bestpair = (rr2, checkset[cinx], res)
    return bestpair
