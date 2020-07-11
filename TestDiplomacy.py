#!/usr/bin/env python3

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase

from Diplomacy import diplomacy_read, diplomacy_print, diplomacy_solve, \
    diplomacy_eval, diplomacy_find_supported, diplomacy_find_supporters

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
        
    
    """
    # -----
    # solve
    # -----
    
    def test_solve_1(self):
        r = StringIO("A Madrid Hold\nB London Support A\nC Berlin Support A\nD Austin Support E\nE Houston Move Madrid\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(
            w.getvalue(), "A Madrid\n B London\n C Berlin\n D Austin\n E [dead]\n")

    def test_solve_2(self):
        r = StringIO("A Madrid Hold\nB Barcelona Move Madrid\nC London Support A\nD Houston Support B\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(
            w.getvalue(), "A [dead]\n B [dead]\n C [dead]\n D [dead]\n")

    def test_solve_3(self):
        r = StringIO("A Berlin Hold\nB London Move Berlin\nC Austin Move Berlin\nD Barcelona Move Berlin\nE NewYork Support A\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(
            w.getvalue(), "A Berlin\n B [dead]\n C [dead]\n D [dead]\n E NewYork\n")

    def test_solve_4(self):
        r = StringIO("A Madrid Hold\nB London Move Madrid\nC Berlin Support A\nD Austin Move Berlin\n E Houston Support D")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(
            w.getvalue(), "A [dead]\n B [dead]\n C [dead]\n D Berlin\n E Houston")

    """

if __name__ == "__main__":
    main()
