
def tripoly(poly):
    return [(poly[0],b,c) for b,c in zip(poly[1:],poly[2:])]

polygon=[1, 2, 3, 4 ,5]

print(tripoly(polygon)) # [('A', 'B', 'C'), ('A', 'C', 'D'), ('A', 'D', 'E')]

