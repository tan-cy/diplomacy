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
        b = [a[0], a[1], a[2]]
        if len(a) == 4:
            b.append(a[3])
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

# ----------------------
# diplomacy_find_support
# ----------------------


def diplomacy_find_support(l, d):
    """
    returns a dictionary of number of supports for each city 
    l is a list of strings : ["A", "Barcelona", "Move", "Madrid"]
    """

    if l[2] == "Support":
        if l[3] in d:
           d.update({l[3]: d.get(l[3]) + 1})
        else:
           d.update({l[3]: 1})
    return d

# -------------
# diplomacy_solve
# -------------


def diplomacy_solve(r, w):
    """
    r a reader
    w a writer
    """
    supporters = {}
    for s in r:
        l = diplomacy_read(s)
        supporters = diplomacy_find_support(l, supporters)
        i, j = diplomacy_eval(l)
        diplomacy_print(w, i, j)