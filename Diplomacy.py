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
    b = []

    if a == []:
        pass
    
    elif len(a) == 4:
        b = [a[0], a[1], a[2], a[3]]

    else:
        b = [a[0], a[1], a[2]]

        
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

        current.update({opp_army: '[dead]'})
        current.update({army: '[dead]'})

    return supported, supporters, current


# -------------
# diplomacy_eval
# -------------

def find_winner(d, current, attackers, supporters, supported):
    """
    d is a dictionary {army : number of support}
    """
    supp_lst = []

    for army in d:
        supp_lst.append(supported[army])

    maximum = max(supp_lst)
    count = 0

    for army in d:
        
        if supported.get(army) == maximum:
           count += 1

        if count > 1:
            for army in d:
                current.update({army : '[dead]'})
            
            return current

    for army in d:
    
        if supported.get(army) == maximum:
        
            if army in attackers:
                current.update({army : attackers.get(army)})
            else:
                pass
        else:
    
            current.update({army : '[dead]'})


    return current
        

def diplomacy_eval(moved, supported, supporters, attacked, attackers, current):

    """
    supported is a dictionary {army : # of support}
    supporters is a dictionary {army : army they support}
    attacked is a dictionary {army : [list of armies attacking them]}
    attackers is a dictionary {army : city it is attacking}
    current is a dictionary {army : current location}
    returns a dictionary with {army : final location}
    """
    d = {}

    for army in attacked:
        
        if army in supporters:
            
            for opp_army in attacked.get(army):
                supported, supporters, current = diplomacy_compare(attacked, attackers, army, opp_army, supported, supporters, current)

    for city in moved:
        lst_armies = moved.get(city)
            
        current = find_winner(lst_armies, current, attackers, supporters, supported)
    
    return current

    

# -------------
# diplomacy_solve
# -------------

def m(l, moved, armies):
    """
    l is a list of strings ['A', 'Madrid', 'Hold']
    moved is a dictionary { city : [list of armies that are in this location] }
    returns moved
    """

    if l[2] == 'Move':
        
        if moved == {}:
            armies = [l[0]]
            moved = {l[3] : armies}

        elif l[3] in moved:
            armies = moved.get(l[3]) + [l[0]]
            moved.update({l[3] : armies})

        else:
            armies = [l[0]]
            moved.update({l[3] : armies})


    elif l[2] == 'Hold' or l[2] == 'Support':
        
        if moved == {}:
            armies = [l[0]]
            moved = {l[1] : armies}

        elif l[1] in moved:
            armies = moved.get(l[1]) + [l[0]]
            moved.update({l[1] : armies})

        else:
            armies = [l[0]]
            moved.update({l[1] : armies})
            
    return moved, armies
        


def diplomacy_solve(r, w):
    """
    r a reader
    w a writer
    """
    supported = {}
    supporters = {}
    attackers = {}
    current = {}
    moved = {}
    armies = []

    for s in r:
        l = diplomacy_read(s)

        if l == []:
            break
        current = diplomacy_find_start(l, current)
        moved, armies = m(l,moved, armies)
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
    solutions = diplomacy_eval(moved, supported, supporters, attacked, attackers, current)
    #print('answer',solutions)
    
    sorted_solutions = sorted(solutions.items())
    
    for solution in sorted_solutions:
        armyName = solution[0]
        location = solution[1]
        diplomacy_print(w, armyName, location)
"""
def main():
    r = StringIO('A Madrid Hold\nB Paris Move London\nC London Move Madrid\n' \
                 'D Barcelona Support B\nE HongKong Hold\nF Venice Move Lyon\n' \
                 'G Lyon Move HongKong\nH Yemin Support E\nI Austin Hold\n' \
                 'J Houston Move Dallas\nK Dallas Move Austin \nL Pasadena Support K\n' \
                 'M HongKong Move Perdu\n')
    w = StringIO()
    diplomacy_solve(r,w)

main()
"""   
 
