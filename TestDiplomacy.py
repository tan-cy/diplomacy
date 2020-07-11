
#!/usr/bin/env python3

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase

from Diplomacy import diplomacy_read, diplomacy_print, diplomacy_solve, diplomacy_find_supported, diplomacy_find_supporters, diplomacy_find_start, diplomacy_attacked, diplomacy_solve

# --------------
# TestDiplomacy
# --------------

class TestDiplomacy(TestCase):

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

    def test_find_start1(self):
        l = ["A", "Austin" ,"Support", "B"]
        d = {}
        answer = diplomacy_find_start(l, d)
        self.assertEqual(answer, {'A':'Austin'})

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
    
    """
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
