A = []
A.append([False, False, True,  True,  True,  False, False, False, False, False])
A.append([False, False, False, False, True,  True,  True,  False, False, False])
A.append([False, True,  True,  True,  False, False, False, False, False, False])

r =      [False, True,  True,  True,  True,  True,   True, False, False, False]
L = len(A[0])
W = []

start = True
w = set()
for i in range(L):
    if start: # beginning of window
        for a in A:  
            if a[i] is True:  # found the start of the window
                w.add(i)      # mark it
                start = False # start looking for the end of the window
                break
    else:
        end = True # until proven otherwise
        for a in A:
            if a[i] is True:  # nope, not the end, keep looking
                end = False   # proof
                break
        if end is True:  # all false, this is the end
            w.add(i-1)   # mark it
            W.append(w)  # save it
            w = set()    # start over
            start = True
    
print (W) 