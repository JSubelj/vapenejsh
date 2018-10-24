# !/usr/bin/env python3
"""
Vape entities like flavour, base etc.

"""

__author__ = "Jan Šubelj"
__version__ = "0.1.0"
__license__ = "MIT"

from Singelton import Singelton
















if __name__ == "__main__":
    MyStorage = Storage()

    nic = Nicotine(18, 10, 1.5)
    base = Base((50, 50), 1000, 15)
    nicbase = NicBase(base, nic, 100, no_of_shots=2)

    lynchee = TFA_F("Lynchee")
    pear = TFA_F("Pear")

    ingr = {"Lynchee": 4, "Pear": 6}
    rec = Recipe("krneki", ingr)
    rec = rec.norm_procentage_to(100)

    MyStorage.add_company(TFA())

    MyStorage.add_flavour(lynchee)
    MyStorage.add_flavour(pear)
    MyStorage.add_flavour_to_storage(lynchee)
    MyStorage.add_flavour_to_storage(pear)
    MyStorage.add_recipe(rec)

    print(dict_to_string(MyStorage.flavours))
    print(dict_to_string(MyStorage.current))
    print(MyStorage.could_it_be_made(rec, 10))
