# !/usr/bin/env python3

from entities.Storage import Entity, StorageEntity
from entities.Singelton import Singelton

class Flavour(Entity):
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

class Company:
    def __init__(self,name):
        self.company_name = name

    def __str__(self):
        return self.company_name

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
def TFA():
    return Company("The Flavour Apprentice")

class TFA_F(Flavour):
    price = 3.95
    volume = 15
    company = TFA()

    # Flavour apprentice
    def __init__(self, name, price=None, volume=None):
        _price = price if price else self.price
        _volume = volume if volume else self.volume
        super().__init__(self.company, name, _price, _volume)

    def __str__(self) -> str:
        return super().__str__()

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)





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
