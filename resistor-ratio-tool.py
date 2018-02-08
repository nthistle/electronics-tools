## Neil Thistlethwaite, 2017
from bisect import bisect_left

## Resistor Sets
E6 = [100, 150, 220, 330, 470, 680]
E12 = [100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820]
E24 = [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330,
        360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910]
E48 = [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178,
        187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332,
        348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619,
        649, 681, 715, 750, 787, 825, 866, 909, 953]
E96 = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133,
        137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182,
        187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249,
        255, 261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332, 340,
        348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464,
        475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634,
        649, 665, 681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866,
        887, 909, 931, 953, 976]

def findresistors(ratio, resset=E96):
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
