#!/usr/bin/env python3
from io import StringIO

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
        

# ------------------------
# diplomacy_find_supported
# ------------------------


def diplomacy_find_supported(l, d):
    """
    returns a dictionary of number of supports for each army 
    l is a list of strings : ["A", "Barcelona", "Support", C"]
    """

    if l[3] in d:
       d.update({l[3]: d.get(l[3]) + 1})
    else:
       d.update({l[3]: 1})
    return d


# -------------------------
# diplomacy_find_supporters
# -------------------------


def diplomacy_find_supporters(l, d):
    """
    returns a dictionary of army : army they are supporting 
    l is a list of strings : ["A", "Barcelona", "Support", "B"]
    """
    if d == {}:
        d = {l[0]: l[3]}
    else:
        d.update({l[0]: l[3]})
    return d
    
    
# ----------------------
# diplomacy_find_start
# ----------------------


def diplomacy_find_start(l, d):
    """
    returns a updated dictionary of starting city for an army
    l is a list of strings : ["A", "Barcelona", "Support", "B"]
    """
    if d == {}:
        d = {l[0]: l[1]}

    else:
        d.update({l[0]:l[1]})

    return d

# -------------------
# diplomacy_attacked
# -------------------
def diplomacy_attacked(attackers, current):
    """
    attackers is a dictionary attacking army : city it is attacking
    current is a dictionary army : current location
    returns a dictionary army : [list of armies that want to attack it]
    """

    attacked = {}

    for attacker in attackers:
        for city in current:   
            if attackers.get(attacker) == current.get(city):
                if current.get(attacker) == attackers.get(city): 
                    pass
                if attacked == {}:
                    att = [attacker]
                    attacked = {city: att}
                    
                else:

                    if attacked.get(city) == None:
                        att = [attacker]
                    else:
                        attacked.get(city).append(attacker)
                    attacked.update({city: att})
                

    return attacked

# ------------------
# diplomacy_compare
# ------------------
def diplomacy_compare(army, opp_army, supported, supporters, current):
    """
    returns supported, supporters, current after comparing supporting armies
    """
    opp_supp = supported.get(opp_army)
    army_supp = supported.get(army)
    if opp_supp > army_supp:
        current.update({opp_army: current.get(army)})
        current.update({army: '[dead]'})
        if army in supporters:
            supported[supporters.get(army)] -= 1
            supporters.pop(army)
    elif army_supp > opp_supp:
        current.update({opp_army: '[dead]'})
    else:
        current.update({opp_army: '[dead]'})
        current.update({army: '[dead]'})
    return supported, supporters, current


# -------------
# diplomacy_eval
# -------------


def diplomacy_eval(supported, supporters, attacked, current):

    """
    supported is a dictionary {army : # of support}
    supporters is a dictionary {army : army they support}
    attacked is a dictionary {army : [list of armies attacking them]}
    current is a dictionary {army : current location}
    returns a dictionary with {army : final location}
    """
    for army in attacked:
        if army in supporters:
            for opp_army in attacked.get(army):
                supported, supporters, current = diplomacy_compare(army, opp_army, supported, supporters, current) 
    for army in attacked:
        if current.get(army) == '[dead]':
            pass
        else:
            for opp_army in attacked.get(army):
                supported, supporters, current = diplomacy_compare(army, opp_army, supported, supporters, current)               
    return current


# -------------
# diplomacy_solve
# -------------


def diplomacy_solve(r, w):
    """
    r a reader
    w a writer
    """
    supported = {}
    supporters = {}
    attackers = {}
    current = {}

    for s in r:
        l = diplomacy_read(s)
        current = diplomacy_find_start(l, current)
        if (len(l) > 3) and (l[2] == "Move"):
            attackers.update({l[0]:l[3]}) # army name : city attacking
        elif (len(l) > 3) and (l[2] == "Support"):
            supported = diplomacy_find_supported(l, supported)
            supporters = diplomacy_find_supporters(l, supporters)
        
    # updates supported for armies with 0 supporters     
    for army in current:
        if army not in supported:
            supported.update({army:0})
            
    attacked = diplomacy_attacked(attackers, current)

    # finds solution after move    
    solutions = diplomacy_eval(supported, supporters, attacked, current)

    for solution in solutions:
        armyName = solution
        location = solutions.get(solution)
        diplomacy_print(w, armyName, location)


def main():
    r = StringIO("A Berlin Hold\nB London Move Berlin\nC Austin Move Berlin\nD Barcelona Move Berlin\nE NewYork Support A\n")
    w = StringIO()
    diplomacy_solve(r, w)
    
        

