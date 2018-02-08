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

def find_resistors_for_ratio(ratio, resistor_set=resistor_sets["E96"]):
    check_set = [r for r in resistor_set]
    flipped_ratio = ratio < 1.0
    if flipped_ratio:
        ratio = 1.0/ratio
    max_ideal = resistor_set[-1]*ratio
    ctmp = [x for x in resistor_set]
    while max_ideal >= check_set[-2]:
        ctmp = [10*x for x in ctmp]
        check_set.extend([x for x in ctmp])
    best_pair = (1.0,check_set[0],check_set[0])
    for resistor in resistor_set:
        ideal = ratio * resistor
        target_index = bisect_left(check_set, ideal)
        poss_ratio_1 = check_set[target_index-1] / resistor
        poss_ratio_2 = check_set[target_index] / resistor
        if(abs(best_pair[0]-ratio) > abs(poss_ratio_1-ratio)):
            best_pair = (poss_ratio_1, check_set[target_index-1], resistor)
        if(abs(best_pair[0]-ratio) > abs(poss_ratio_2-ratio)):
            best_pair = (poss_ratio_2, check_set[target_index], resistor)
    return best_pair if not flipped_ratio else (1.0/best_pair[0], best_pair[2], best_pair[1])
