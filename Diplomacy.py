#!/usr/bin/env python3
from io import StringIO

# -------------
# diplomacy_read
# -------------

def diplomacy_read(s):
    """
    reads 3 strings
    s is a string
    return a list of 3 strings: army name, city name, and action 
    """
    a = s.split()
    
    b = [a[0], a[1], a[2]]
    if len(a) == 4:
        b.append(a[3])
    return b

        
# -------------
# diplomacy_print
# -------------


def diplomacy_print(w, i, j):
    """
    print two strings
    w is a writer
    i is an army name
    j is the army's location or [dead]
    """
    w.write(str(i) + " " + str(j) + "\n")
        

# ------------------------
# diplomacy_find_supported
# ------------------------


def diplomacy_find_supported(l, d):
    """
    returns a dictionary of the number of supports for each army {army : number of supporters}
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
    returns a dictionary of all armies and their supporters {army : army they are supporting} 
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
    returns a dictionary of starting city for an army {army:starting city}
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
    attackers is a dictionary {attacking army : city it is attacking}
    current is a dictionary {army : current location}
    returns a dictionary {army : [list of armies that want to attack it]}
    """

    attacked = {}

    for attacker in attackers:
        for army in current:   
            if attackers.get(attacker) == current.get(army): 
                if (army in attacked) == False:
                    att = []
                    
                if attacked == {}:
                    att = [attacker]
                    attacked = {army: att}
                else:
                    if attacked.get(army) == None:
                        att = [attacker]
                    else:
                        a = attacked.get(army)
                        att = a + [attacker]
                    attacked.update({army: sorted(att)})

    return attacked

# ------------------
# diplomacy_compare
# ------------------
def diplomacy_compare(attacked, attackers, army, opp_army, supported, supporters, current):
    """
    returns supported, supporters, current after comparing supporting armies
    """

    if army in supporters:
        supported[supporters.get(army)] -= 1
        supporters.pop(army)

    opp_supp = supported.get(opp_army)
    army_supp = supported.get(army)

    if opp_supp > army_supp:
        current.update({opp_army: current.get(army)})
        current.update({army: '[dead]'})

            
    elif army_supp > opp_supp:
        current.update({army: current.get(army)})
        current.update({opp_army: '[dead]'})

            
    else:
        """
        if (army in attacked) and (army in attackers):
            current.update({army: '[dead]'})
            current.update({opp_army:attackers.get(opp_army)})
        
        else:
        """
        current.update({opp_army: '[dead]'})
        current.update({army: '[dead]'})

    return supported, supporters, current


# -------------
# diplomacy_eval
# -------------


def diplomacy_eval(supported, supporters, attacked, attackers, current):

    """
    supported is a dictionary {army : # of support}
    supporters is a dictionary {army : army they support}
    attacked is a dictionary {army : [list of armies attacking them]}
    attackers is a dictionary {army : city it is attacking}
    current is a dictionary {army : current location}
    returns a dictionary with {army : final location}
    """            
    invalid_attacked = []
    new_attacked = {}
    for army in attacked:
        if army in supporters:
            for opp_army in attacked.get(army):
                supported, supporters, current = diplomacy_compare(attacked,attackers,army, opp_army, supported, supporters, current)
        elif army in attackers:
            for opp_army in current: 
                if attackers.get(army) == current.get(opp_army):
                    if opp_army not in attackers:
                        supported, supporters, current = diplomacy_compare(attacked,attackers,opp_army, army, supported, supporters, current)
                        if len(attacked.get(army)) > 1:
                            new_attacked.update({attacked.get(army)[0]: attacked.get(army)[1:]})
                        else:
                            uncontested_army = attacked.get(army)[0]
                            invalid_attacked.append(army)
                            current.update({uncontested_army: attackers.get(uncontested_army)})
    
    for i in invalid_attacked:
        attacked.pop(i)
    attacked.update(new_attacked)    
        
    for army in attacked:
        if current.get(army) == '[dead]':
            for opp_army in attacked.get(army):
                if current.get(opp_army) != '[dead]':
                    current.update({opp_army:attackers.get(opp_army)})   
        else:
            for opp_army in attacked.get(army):
                supported, supporters, current = diplomacy_compare(attacked, attackers,army, opp_army, supported, supporters, current)               
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
    
    # checks for armies attacking unoccupied cities
    held_cities = current.values()
    for army in attackers: 
        if attackers.get(army) not in held_cities:
            current.update({army: attackers.get(army)})
            if army in attacked:
                if len(attacked.get(army)) > 1:
                    attacked.update({attacked.get(army)[0]:attacked.get(army)[1:]})
                attacked.pop(army)


    # finds solution after move    
    solutions = diplomacy_eval(supported, supporters, attacked, attackers, current)
    sorted_solutions = sorted(solutions.items())
    
    for solution in sorted_solutions:
        armyName = solution[0]
        location = solution[1]
        diplomacy_print(w, armyName, location)



