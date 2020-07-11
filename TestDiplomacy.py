#!/usr/bin/env python3

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase


from Diplomacy import diplomacy_read, diplomacy_print, diplomacy_solve, \
    diplomacy_eval, diplomacy_find_supported, diplomacy_find_supporters, \
    diplomacy_compare, diplomacy_find_start, diplomacy_attacked

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

    # --------------------
    # diplomacy_find_start
    # --------------------

    def test_find_start1(self):
        l = ["A", "Austin" ,"Support", "B"]
        d = {}
        answer = diplomacy_find_start(l, d)
        self.assertEqual(answer, {'A':'Austin'})

    # ------------------
    # diplomacy_attacked
    # ------------------

    def test_attacked1(self):
        attackers = {'A':'Madrid', 'C':'Madrid', 'E':'Houston'}
        current = {'A':'Austin', 'B':'Madrid', 'C':'Houston', 'D':'NewYork', 'E':'Detroit'}
        answer = diplomacy_attacked(attackers, current)
        self.assertEqual(answer, {'B':['A','C'], 'C':['E']})

    def test_attacked2(self):
        attackers = {'A': 'Madrid', 'C':'Madrid', 'D':'Madrid', 'E':'Houston', 'G':'Houston', 'H':'NewYork'}
        current = {'A':'Austin', 'B':'Madrid', 'C':'Cairo', 'D':'Houston', 'E':'Tomball', 'F':'NewYork','G':'LaPaz','H':'Tarija'}
        answer = diplomacy_attacked(attackers, current)
        self.assertEqual(answer, {'B':['A','C','D'], 'D':['E','G'], 'F':['H']})

    def test_attacked3(self):
        attackers = {}
        current = {'A':'Austin','B':'Madrid', 'C':'Cairo'}
        answer = diplomacy_attacked(attackers, current)
        self.assertEqual(answer, {})
    
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
        
    
    
    # -----
    # solve
    # -----

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

if __name__ == "__main__":
    main()
