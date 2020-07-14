#!/usr/bin/env python3

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase


from Diplomacy import diplomacy_read, diplomacy_print, diplomacy_solve, \
    diplomacy_eval, diplomacy_find_supported, diplomacy_find_supporters, \
    diplomacy_compare, diplomacy_find_start, diplomacy_attacked, find_winner, \
    moved_armies

# --------------
# TestDiplomacy
# --------------

class TestDiplomacy(TestCase):
    
    # ----
    # read
    # ----
    
    def test_read_1(self):
        s = "A Berlin Hold"
        i = diplomacy_read(s)
        self.assertEqual(i, ["A","Berlin","Hold"])

    def test_read_2(self):
        s = "A Berlin Move NewYork"
        i = diplomacy_read(s)
        self.assertEqual(i,  ["A", "Berlin","Move", "NewYork"])

    def test_read_3(self):
        s = "Z London Support A"
        i = diplomacy_read(s)
        self.assertEqual(i, ["Z", "London", "Support", "A"])

    # -----
    # print
    # ----- 
    
    def test_print_1(self):
        w = StringIO()
        diplomacy_print(w, "A", "Berlin")
        self.assertEqual(w.getvalue(), "A Berlin\n")

    def test_print_2(self):
        w = StringIO()
        diplomacy_print(w, "B", "[dead]")
        self.assertEqual(w.getvalue(), "B [dead]\n")

    def test_print_3(self):
        w = StringIO()
        diplomacy_print(w, "Z", "NewYork")
        self.assertEqual(w.getvalue(), "Z NewYork\n")

    # ------------------------
    # diplomacy_find_supported
    # ------------------------
    
    def test_supported_1(self):
        l = ["A", "Barcelona", "Support", "C"]
        d = {}
        z = diplomacy_find_supported(l,d)
        self.assertEqual(z, {"C":1})
        
    def test_supported_2(self):
        l = ["A", "Barcelona", "Support", "C"]
        d = {"C": 3}
        z = diplomacy_find_supported(l,d)
        self.assertEqual(z, {"C":4})
    
    def test_supported_3(self):
        l = ["A", "Barcelona", "Support", "C"]
        d = {"D": 3}
        z = diplomacy_find_supported(l,d)
        self.assertEqual(z, {"D": 3, "C": 1})
        
        
    # -------------------------
    # diplomacy_find_supporters
    # -------------------------
    
    def test_supporter_1(self):
        l = ["A", "Barcelona", "Support", "C"]
        d = {}
        z = diplomacy_find_supporters(l,d)
        self.assertEqual(z, {"A": "C"})
        
    def test_supporter_2(self):
        l = ["A", "Barcelona", "Support", "C"]
        d = {"B": "D"}
        z = diplomacy_find_supporters(l,d)
        self.assertEqual(z, {"B": "D", "A": "C"})


    # --------------------
    # diplomacy_find_start
    # --------------------

    def test_find_start_1(self):
        l = ["A", "Austin" ,"Support", "B"]
        d = {}
        answer = diplomacy_find_start(l, d)
        self.assertEqual(answer, {'A':'Austin'})

    # ------------------
    # diplomacy_attacked
    # ------------------

    def test_attacked_1(self):
        attackers = {'A':'Madrid', 'C':'Madrid', 'E':'Houston'}
        current = {'A':'Austin', 'B':'Madrid', 'C':'Houston', 'D':'NewYork', 'E':'Detroit'}
        answer = diplomacy_attacked(attackers, current)
        self.assertEqual(answer, {'B':['A','C'], 'C':['E']})

    def test_attacked_2(self):
        attackers = {'A': 'Madrid', 'C':'Madrid', 'D':'Madrid', 'E':'Houston', 'G':'Houston', 'H':'NewYork'}
        current = {'A':'Austin', 'B':'Madrid', 'C':'Cairo', 'D':'Houston', 'E':'Tomball', 'F':'NewYork','G':'LaPaz','H':'Tarija'}
        answer = diplomacy_attacked(attackers, current)
        self.assertEqual(answer, {'B':['A','C','D'], 'D':['E','G'], 'F':['H']})

    def test_attacked_3(self):
        attackers = {}
        current = {'A':'Austin','B':'Madrid', 'C':'Cairo'}
        answer = diplomacy_attacked(attackers, current)
        self.assertEqual(answer, {})
    
    def test_attacked_4(self):
        attackers = {'B':'Madrid', 'D':'London'}
        current = {'A':'Madrid','B':'London', 'C':'Berlin', 'D':'Detroid'}
        answer = diplomacy_attacked(attackers, current)
        self.assertEqual(answer, {'A':['B'], 'B':['D']})
    
    
    # ----------------
    # dipomacy_compare
    # ----------------
    def test_compare_1(self):
        attacked = {'A':['B']}
        attackers = {'B':'Austin'}
        army = 'A'
        opp_army = 'B'
        supported = {'A':0, 'B':0}
        supporters = {}
        current = {'A':'Austin', 'B':'Berlin'}
        answer = diplomacy_compare(attacked, attackers, army, opp_army, supported, supporters, current)
        self.assertEqual(answer, ({'A':0, 'B':0}, {}, {'A':'[dead]', 'B':'[dead]'}))

    def test_compare_2(self):
        attacked = {'A':['B']}
        attackers = {'B':'Austin'}
        army = 'A'
        opp_army = 'B'
        supported = {'A':2, 'B':1}
        supporters = {'C':'A', 'D':'A', 'E':'B'}
        current = {'A':'Austin', 'B':'Berlin', 'C':'Cairo', 'D':'Detroit', 'E':'NewYork'}
        answer = diplomacy_compare(attacked, attackers, army, opp_army, supported, supporters, current)
        self.assertEqual(answer, ({'A':2, 'B':1}, {'C':'A', 'D':'A', 'E':'B'}, {'A':'Austin', 'B':'[dead]', 'C':'Cairo', 'D':'Detroit', 'E':'NewYork'}))

    def test_compare_3(self):
        attacked = {'A':['D']}
        attackers = {'D':'Austin'}
        army = 'A'
        opp_army = 'D'
        supported = {'A':0, 'D':1}
        supporters = {'A':'D'}
        current = {'A':'Austin', 'B':'Berlin', 'C':'Cairo', 'D':'Detroit'}
        answer = diplomacy_compare(attacked, attackers, army, opp_army, supported, supporters, current)
        self.assertEqual(answer, ({'A':0, 'D':0}, {}, {'A':'[dead]', 'B':'Berlin', 'C':'Cairo', 'D':'[dead]'}))
    
    # -----------
    # find_winner
    # -----------
    def test_find_winner_1(self):
        d = ['A', 'B', 'C']
        current = {'A':'Austin', 'B':'Berlin', 'C':'Cairo'}
        attackers = {'B':'Austin', 'C':'Austin'}
        supported = {'A':0, 'B':0, 'C':0}
        supporters = {}
        answer = find_winner(d, current, attackers, supporters, supported)
        self.assertEqual(answer, {'A':'[dead]', 'B':'[dead]', 'C':'[dead]'})

    def test_find_winner_2(self):
        d = ['A']
        current = {'A':'Austin'}
        attackers = {}
        supported = {'A':0}
        supporters = {}
        answer = find_winner(d, current, attackers, supporters, supported)
        self.assertEqual(answer, {'A':'Austin'})
    

    
    # ---------------
    # diplomacy_solve
    # ---------------

    def test_solve_1(self):
        r = StringIO("A Madrid Hold\nB London Support A\nC Berlin Support A\nD Austin Support E\nE Houston Move Madrid\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(w.getvalue(), "A Madrid\nB London\nC Berlin\nD Austin\nE [dead]\n")
            
    def test_solve_2(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Support A\nD Houston Support B\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC London\nD Houston\n")
    
    def test_solve_3(self):
        r = StringIO("A Berlin Hold\nB London Move Berlin\nC Austin Move Berlin\nD Barcelona Move Berlin\nE NewYork Support A\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(w.getvalue(), "A Berlin\nB [dead]\nC [dead]\nD [dead]\nE NewYork\n")
    
    def test_solve_4(self):
        r = StringIO("A Madrid Hold\nB London Move Madrid\nC Berlin Support A\nD Austin Move Berlin\nE Houston Support D")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC [dead]\nD Berlin\nE Houston\n")
    
    def test_solve_5(self):
        r = StringIO("A Madrid Hold\nB London Move Madrid\nC Berlin Support A\nD Austin Move Berlin\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC [dead]\nD [dead]\n")
    
    def test_solve_6(self):
        r = StringIO("A Madrid Hold\nB Detroit Move London\nC Berlin Support A\nD London Move Madrid\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A Madrid\nB London\nC Berlin\nD [dead]\n")

    def test_solve_7(self):
        r = StringIO("A Madrid Move London\nB London Support Madrid\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\n")

    def test_solve_8(self):
        r = StringIO("A Madrid Hold\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A Madrid\n")

    def test_solve_9(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Support B\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB Madrid\nC London\n")

    def test_solve_10(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\n")

    def test_solve_11(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Support B\nD Austin Move London\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC [dead]\nD [dead]\n")

    def test_solve_12(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Move Madrid\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC [dead]\n")

    def test_solve_13(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Move Madrid\nD Paris Support B\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB Madrid\nC [dead]\nD Paris\n")

    def test_solve_14(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Move Madrid\nD Paris Support B\nE Austin Support A\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC [dead]\nD Paris\nE Austin\n")

    def test_solve_15(self):
        r = StringIO("A Austin Support D\nB Berlin Hold\nC Cairo Hold\nD Detroit Move Austin\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB Berlin\nC Cairo\nD [dead]\n")

    def test_solve_16(self):
        r = StringIO("A Madrid Hold\nB Paris Hold\nC Moscow Move Madrid\nD Kiev Support C\nE Berlin Move Paris\nF Austin Support E\nG Houston Support F\nH Dallas Support F\nI Copenhagen Move Austin\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC Madrid\nD Kiev\nE [dead]\nF Austin\nG Houston\nH Dallas\nI [dead]\n")

    def test_solve_17(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Move Barcelona\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\nC Barcelona\n")

    def test_solve_18(self):
        r = StringIO("A Madrid Hold\nB Berlin Support A\nC Cairo Support B\nD Detroit Support C\nE NewYork Move Detroit\nF Austin Move Cairo\nG Georgetown Move Madrid\n")
        w = StringIO()
        diplomacy_solve(r,w)
        self.assertEqual(w.getvalue(), "A Madrid\nB Berlin\nC [dead]\nD [dead]\nE [dead]\nF [dead]\nG [dead]\n")

        
        
    
if __name__ == "__main__": #pragma: no cover
    main()
