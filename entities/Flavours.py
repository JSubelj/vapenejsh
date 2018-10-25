# !/usr/bin/env python3

from entities.Storage import Entity, StorageEntity
from entities.Singelton import Singelton
import json


class Flavour(Entity, object):
    def __init__(self, company, name, price, quantity):
        self.company = company
        self.name = name
        super().__init__(quantity, price)

    def __str__(self) -> str:
        return ("{Name: %s, Company: %s, " % (self.name, self.company)) + super().__str__()+"}"

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class FlavourStorage(StorageEntity):
    def __init__(self, flavour: Flavour):
        self.name = flavour.name
        self.company = flavour.company
        super().__init__(flavour)

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class _Company:
    # should not be called
    derived_flavour_classes={}
    company_names={}

    def __init__(self,name,price=None,volume=None):
        self.company_name = name
        self.company_names[name]=self
        class_f, class_name =self.ClassFactory(self, price, volume)
        self.derived_flavour_classes[name] = (class_f, class_name)

    def return_derived_flavour_class(self,name):
        return self.derived_flavour_classes[name]

    def __str__(self):
        return self.company_name

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def ClassFactory(company, price=None,volume=None):
        def __init__(self, name):
            super(type(self), self).__init__(company, name, price if price else self.price,volume if volume else self.volume)
        split_c_name = company.company_name.split(" ")

        if len(split_c_name) == 1:
            class_name=company.company_name
        else:
            class_name=""
            for w in split_c_name:
                class_name+=w[0].capitalize()
        class_name+="_F"

        newclass = type(class_name, (Flavour,), {"__init__": __init__})
        globals()[class_name] = newclass
        return newclass, class_name


def Company(name, price=None, volume=None):
    if name in _Company.company_names.keys():
        c = _Company.company_names[name]
        dc, name = c.return_derived_flavour_class(name)
        return c, dc, name
    else:
        c = _Company(name, price, volume)
        dc, name = c.return_derived_flavour_class(name)
        return c, dc, name




class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.procentage = 0
        self.ingredients = ingredients

        for _, proc in self.ingredients.items():
            self.procentage += proc[0]

    def norm_procentage_to(self, value_to_norm):
        rel = value_to_norm / self.procentage
        ingredients = {}
        for name, (i,c) in self.ingredients.items():
            ingredients[name] = (i * rel,c)

        return Recipe(self.name, ingredients)

    def ingredients_to_string(self):
        string=""
        for flavour, (percentage,com) in self.ingredients.items():
            string+="\n\t\t"+flavour.name+" ("+com+") : "+str(percentage)+"%"
        return string

    def __str__(self) -> str:
        return "{Recipe "+self.name+":\n\t"+"Procentage: "+str(self.procentage)+"\n\t"+"Ingredients: "+self.ingredients_to_string()+"}"

    def toJSON(self):
        string = "{ \"name\":\""+self.name+"\",\n"+"\"procentage\":"+str(self.procentage)+",\n \"ingrediants\":{\n\t"
        for flavor, (precentage, _) in self.ingredients.items():
            string+=" \""+flavor.name+"_"+flavor.company.company_name+"\": "+str(precentage)+",\n\t"

        string=string[:-3]
        string+="}}"
        return string
