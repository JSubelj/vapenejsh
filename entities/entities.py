# !/usr/bin/env python3
"""
Vape entities like flavour, base etc.

"""

__author__ = "Jan Šubelj"
__version__ = "0.1.0"
__license__ = "MIT"

from Singelton import Singelton


class Entity:
    def __init__(self, volume, price):
        self.volume = volume
        self.price = price
        self.price_per_ml = price / volume

    def __str__(self):
        return "Volume: %f, Price: %f, Price per ml: %f" % (self.volume, self.price, self.price_per_ml)

class Base(Entity):
    def __init__(self, pgvg, volume, price):
        if pgvg[0] + pgvg[1] != 100:
            raise ValueError("pgvg not 100%")

        self.pg = pgvg[0]
        self.vg = pgvg[1]
        super().__init__(volume, price)


class Nicotine(Entity):
    # shots
    def __init__(self, strength, volume, price):
        super().__init__(volume, price)
        self.strength = strength


class NicBase(Base):
    def __init__(self, base, nic, volume, wanted_strength=None, no_of_shots=None):
        if wanted_strength is None:
            dialution = NicBase.nic_dialution_per_quantity(no_of_shots, nic, volume)
        else:
            dialution = NicBase.nic_dialution(nic.strength, volume, wanted_strength)

        price = NicBase.calculate_price(dialution, nic, base)
        self.strength = dialution["end_nic_strength"]
        super().__init__((base.pg, base.vg), volume, price)

    def __str__(self) -> str:
        return ("Strength %f " % self.strength) + super().__str__()

    @staticmethod
    def calculate_price(dialution, nic, base):
        nic_vol = dialution["end_nic_quant"]
        base_vol = dialution["end_base_quant"]

        return nic_vol * nic.price_per_ml + base_vol * base.price_per_ml

    @staticmethod
    def nic_dialution(init_nic_strength, end_quantity, end_nic_strength):
        '''

        :param init_nic_strength: in mg/ml
        :param end_quantity: in ml
        :param end_nic_strength: in mg/ml
        :return:
        '''

        end_nic_quantity = (end_nic_strength * end_quantity) / init_nic_strength
        end_base_quantity = end_quantity - end_nic_quantity

        return {"end_nic_quant": end_nic_quantity, "end_base_quant": end_base_quantity,
                "end_nic_strength": end_nic_strength, "end_quant": end_quantity}

    @staticmethod
    def nic_dialution_per_quantity(no_of_shots, nic, end_quantity):
        end_nic_quantity = no_of_shots * nic.volume
        end_nic_strength = (end_nic_quantity * nic.strength) / end_quantity
        end_base_quantity = end_quantity - end_nic_quantity

        return {"end_nic_quant": end_nic_quantity, "end_base_quant": end_base_quantity,
                "end_nic_strength": end_nic_strength, "end_quant": end_quantity}


class Flavour(Entity):
    def __init__(self, company, name, price, quantity):
        self.company = company
        self.name = name
        super().__init__(quantity, price)

    def __str__(self) -> str:
        return ("Name: %s, Company: %s " % (self.name, self.company))+super().__str__()


class StorageEntity:
    def __init__(self, article: Entity):
        self.article = article
        self.inital_volume = article.volume
        self.current_volume = article.volume

    def add_new(self):
        self.current_volume += self.inital_volume

    def __str__(self):
        return "Name: %s, Initial vol: %f, Current vol: %f" % (self.article.name, self.inital_volume, self.current_volume)

class FlavourStorage(StorageEntity):
    def __init__(self, flavour: Flavour):
        self.name = flavour.name
        self.company = flavour.company
        super().__init__(flavour)




class TFA_F(Flavour):
    price = 3.95
    volume = 15

    # Flavour apprentice
    def __init__(self, name, price=None, volume=None):
        _price = price if price else self.price
        _volume = volume if volume else self.volume
        super().__init__(TFA(), name, _price, _volume)

    def __str__(self) -> str:
        return super().__str__()


class Company:
    company_name = ""
    def __str__(self):
        return "Company Name: "+self.company_name

class TFA(Company, metaclass=Singelton):
    company_name = "The Flavour Apprentice"



class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.procentage = 0
        self.ingredients = ingredients

        for _, proc in self.ingredients.items():
            self.procentage += proc

    def norm_procentage_to(self, value_to_norm):
        rel = value_to_norm / self.procentage
        ingredients = {}
        for name, i in self.ingredients.items():
            ingredients[name] = i * rel

        return Recipe(self.name, ingredients)


class Storage:
    def __init__(self):
        self.current = {}
        self.recepies = {}
        self.flavours = {}

    def add_company(self, company):
        if company in self.current.keys():
            return
        self.current[company] = {}

    def add_flavour_to_storage(self, flavour: Flavour):
        if flavour.name in self.current[flavour.company].keys():
            self.current[flavour.company][flavour].add_new()
            return

        self.current[flavour.company][flavour] = FlavourStorage(flavour)
        self.flavours[flavour] = flavour

    def add_flavour(self, flavour: Flavour):
        self.flavours[flavour.name] = flavour


    def get_flavour(self, flavour_name):
        return self.flavours[flavour_name]

    def get_flavour_from_storage(self, flavour: Flavour) -> FlavourStorage:
        return self.current[flavour.company][flavour]

    def add_recipe(self, recipe: Recipe):
        ingredients = {}

        for f_name, proc in recipe.ingredients.items():
            ingredients[self.get_flavour(f_name)] = proc

        if recipe.name not in self.recepies:
            self.recepies[recipe.name] = {}

        self.recepies[recipe.name][recipe.procentage] = Recipe(recipe.name, ingredients)

    def get_recipe(self, name):
        return self.recepies[name]

    def create_recipe(self, _recepie: Recipe, volume):
        if not self.could_it_be_made(_recepie)[0]:
            return False

        recepie = self.recepies[_recepie.name][_recepie.procentage]
        for flavour, precentage in recepie.items():
            storage_flavour = self.get_flavour_from_storage(flavour)
            storage_flavour.current_volume += - precentage * 0.01 * volume

    def could_it_be_made(self, _recepie: Recipe, volume):
        recepie = self.recepies[_recepie.name][_recepie.procentage]
        what_remains = {}
        for flavour, precentage in recepie.ingredients.items():
            current_vol = self.get_flavour_from_storage(flavour).current_volume
            remaining_vol = current_vol - precentage * 0.01 * volume
            if remaining_vol < 0:
                return False, "%s current %f needed %f" % (flavour.name, current_vol, remaining_vol)
            what_remains[flavour.name] = remaining_vol

        return True, what_remains




def dict_to_string(dictionary, no_print=True):
    string=""
    for key, value in dictionary.items():
        if isinstance(value,dict):
            string+= '{ '+ str(key)+ ' : {'+ str(dict_to_string(value, no_print=False)) + '} }'
        else:
            string+= '{ '+ str(key)+ ' : {'+ str(value) + '} }'
    print(string)

if __name__ == "__main__":
    MyStorage = Storage()

    nic = Nicotine(18, 10, 1.5)
    base = Base((50, 50), 1000, 15)
    nicbase = NicBase(base, nic, 100, no_of_shots=2)

    lynchee = TFA_F("Lynchee")
    pear = TFA_F("Pear")

    ingr = {"Lynchee":4, "Pear":6}
    rec = Recipe("krneki",ingr)
    rec = rec.norm_procentage_to(100)

    MyStorage.add_company(TFA())

    MyStorage.add_flavour(lynchee)
    MyStorage.add_flavour(pear)
    MyStorage.add_flavour_to_storage(lynchee)
    MyStorage.add_flavour_to_storage(pear)
    MyStorage.add_recipe(rec)

    print(dict_to_string(MyStorage.flavours))
    print(dict_to_string(MyStorage.current))
    print(MyStorage.could_it_be_made(rec,10))