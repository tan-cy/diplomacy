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
    returns a dictionary of number of supports for each city 
    l is a list of strings : ["A", "Barcelona", "Move", "Madrid"]
    """

    if l[2] == "Support":
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

    if l[2] == "Support":
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
        

# -------------
# diplomacy_eval
# -------------


def diplomacy_eval(supported, supporters, attacked, current):

    """
    returns a list of outcomes
    supported is a dictionary {army : # of support}
    supporters is a dictionary {army : army they support}
    attacked is a dictionary {army : [list of armies attacking them]} 
    l is a list
    """
    for army in attacked:
        for att_army in attacked.get(army):

            if (army not in supported) and (att_army not in supported):
                current.update({army : '[dead]'})
                current.update({att_army : '[dead]'})

                if army in supporters:
                    supporters.pop(army)
                    supported[supporters.get(army)] -= 1

                elif att_army in supporters:
                    #supporters.pop(att_army)
                    supported[supporters.get(att_army)] -= 1

            elif (army not in supported) and (att_army in supported):
                current.update({att_army : current.get(army)})
                current.update({army : '[dead]'})

                if army in supporters:
                    #supporters.pop(army)
                    supported[supporters.get(army)] -= 1

            elif (army in supported) and (att_army not in supported):
                current.update({army : current.get(att_army)})
                current.update({att_army : '[dead]'})

                if att_army in supporters:
                    #supporters.pop(att_army)
                    supported[supporters.get(att_army)] -= 1

            else:
                pass

            

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
    outcome = {}

    for s in r:
        l = diplomacy_read(s)
        supported = diplomacy_find_supported(l, supported)
        supporters = diplomacy_find_supporters(l, supporters)
        current = diplomacy_find_start(l, current)

        if (len(l) > 3) and (l[2] == "Move"):
            attackers.update({l[0]:l[3]}) # army name : city attacking

        if outcome == {}:
            outcome = {l[0]:""}
        else:
            outcome.update({l[0]:""})

    attacked = diplomacy_attacked(attackers, current)


    
    # finds solution after move    
    solution = diplomacy_eval(supported, supporters, attacked, current)

