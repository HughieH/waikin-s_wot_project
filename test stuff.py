A = {'a':5, 't':4, 'd':2}
B = {'s':11, 'a':4, 'd': 0}

C = {x: A[x] - B[x] for x in A if x in B}

print(C)