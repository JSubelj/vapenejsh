# !/usr/bin/env python3

from entities.Storage import Entity, StorageEntity
from entities.Singelton import Singelton
import json


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
    def __init__(self,name,price=None,volume=None):
        self.company_name = name
        self.spawn_class_for_flavours(name,price,volume)
        TFA_F("lb")

    def __str__(self):
        return self.company_name

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)



    def constructor_for_flavours(self, name, price=None, volume=None):
        super().__init__(self.company, name, price if price else self.price,
                                      volume if volume else self.volume)

    def spawn_class_for_flavours(self, company_name: str,price=None,volume=None):
        split_c_name = company_name.split(" ")

        if len(split_c_name) == 1:
            class_name=company_name+"_F"
        else:
            class_name=""
            for w in split_c_name:
                class_name+=w[0].capitalize()
            class_name+="_F"
        globals()[class_name] = type(class_name,(Flavour,),{
                        "price": price,
                        "volume": volume,
                        "company": self,
                        "__init__": self.constructor_for_flavours,
                        "__str__": lambda self: super(class_name,self).__str__(),
                        "toJSON": lambda self: json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
                    })



'''
class TFA_F(Flavour):
    price = 3.95
    volume = 15
    company = Company("The Flavour Apprentice")

    # Flavour apprentice
    def __init__(self, name, price=None, volume=None):
        _price = price if price else self.price
        _volume = volume if volume else self.volume
        super().__init__(self.company, name, _price, _volume)

    def __str__(self) -> str:
        return super().__str__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

'''



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
