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

# ----------------------
# diplomacy_find_start
# ----------------------


def diplomacy_find_start(l, d):
    """
    returns a updated dictionary of starting city for an army
    l is a list of strings : ["A", "Barcelona", "Move", "Madrid"]
    """
    return d.update({l[0]:l[1]})


# -------------
# diplomacy_eval
# -------------


def diplomacy_eval(supporters, attackers, start, armies):
    """
    returns a list of outcomes
    supporters is a dictionary {army : # of support}
    attackers is a dictionary {army : city attacking} 
    l is a list
    """
    outcome = {}
    for army in supporters:
        if army[0] in attackers
        """
        if army[2] == "Move":
            support_attacker = supporters.get(army[0])
            support_defender = supporters.get(army[3])
            if support_attacker > support_defender:
                outcome.update({army[0]: army[3])
                outcome.update({army[3]: "[dead]")
            elif support_attacker < support_defender:
                outcome.update({army[0]: "[dead]")
            else:
                outcome.update({army[0]: "[dead]")
                outcome.update({army[3]: "[dead]")
        """
# -------------
# diplomacy_solve
# -------------


def diplomacy_solve(r, w):
    """
    r a reader
    w a writer
    """
    supporters = {}
    attackers = {}
    armies = []
    start = {}
    # finds initial moves 
    for s in r:
        l = diplomacy_read(s)
        supporters = diplomacy_find_support(l, supporters)
        attackers.update({l[0]:l[3]) # army name : city attacking
        start = diplomacy_find_start(l, start)
        armies.append(l)
    # finds solution after move    
    solution = diplomacy_eval(supporters, attackers, start, armies)
        
        
        #diplomacy_print(w, i, j)
    