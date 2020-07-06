#!/usr/bin/env python3

# -------------
# diplomacy_read
# -------------

def diplomacy_read(s):
    """
    reads 3 strings
    s a string
    return a list of 3 string, army name, city name, and action 
    """
    a = s.split()
    try:
        b = [(a[0]), (a[1]), a([2])]
        if len(a) == 4:
            b += (a[3])
        return b
    except:
        sys.exit()
        
# -------------
# diplomacy_print
# -------------


def diplomacy_print(w, i, j):
    """
    print two strings
    w a writer
    i is army name
    j is army's location or [dead]
    """
    w.write(str(i) + " " + str(j) + "\n")

# -------------
# diplomacy_eval
# -------------


def diplomacy_eval(l):
    """
    returns one strings, army name and army's location or [dead]
    l is a list
    """
    pass
    

# -------------
# diplomacy_solve
# -------------


def diplomacy_solve(r, w):
    """
    r a reader
    w a writer
    """
    for s in r:
        l = diplomacy_read(s)
        i, j = diplomacy_eval(l)
        diplomacy_print(w, i, j)