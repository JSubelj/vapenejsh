# !/usr/bin/env python3




class Entity:
    def __init__(self, volume, price):
        self.volume = volume
        self.price = price
        self.price_per_ml = price / volume

    def __str__(self):
        return "Volume: %f, Price: %f, Price per ml: %f" % (self.volume, self.price, self.price_per_ml)





class StorageEntity:
    def __init__(self, article: Entity):
        self.article = article
        self.inital_volume = article.volume
        self.current_volume = article.volume

    def add_new(self):
        self.current_volume += self.inital_volume

    def __str__(self):
        return "Name: %s, Initial vol: %f, Current vol: %f" % (
        self.article.name, self.inital_volume, self.current_volume)


from entities.Flavours import *

class Storage:
    def __init__(self):
        with open("tmp.pck", "rb") as f:
            import pickle
            # TODO: vsakič k se shran company zapiše to v pickle
            self = pickle.load(f)
            return

        self.current = {} # hierarchy: {Company: {Flavour: FlavourStorage}}
        self.recepies = {} # hierarchy: {recepie_name: {procentage: Recepie}}
        self.flavours = {} # hierarchy: {flavour.name+_+company_name: Flavour}
        self.companies = {}

    def jsonify_companies(self):
        string=""
        for key, val in self.companies.items():
            string+="{\""+key+"\" : "+val.toJSON()+"},"

        return string[:-1]

    def jsonify_flavours(self):
        string = "{"
        for key, val in self.flavours.items():
            string += "\"" + key + "\" : " + val.toJSON() + ","
        string = string[:-1]
        string+="}"
        return string

    def jsonify_recepies(self):
        string = "{"
        for key, val in self.recepies.items():
            string += "\n\""+str(key)+"\" : ["
            for key, val in val.items():
                string += "\n\t{\"" + str(key) + "\" : " + val.toJSON() + "},"
            string=string[:-1]+"],"

        string=string[:-1]
        string+="}"
        return string

    def jsonify_current(self):
        string="{\n"
        # companies
        for comp, flavour_dict in self.current.items():
            string+="\""+comp.company_name+"\":[\n"
            for flavour, flavour_storage in flavour_dict.items():
                string+="{\""+flavour.name+"\":"+flavour_storage.toJSON()+"},\n"
            string=string[:-2]
            string+="],\n"

        return string[:-2]+"\n}"

    def get_recepies(self):
        lst = []
        for _, procentage_dict in self.recepies.items():
            for _, recepie in procentage_dict.items():
                lst.append(recepie)
        return lst

    def get_current(self):
        lst = []
        for company in self.current:
            for flavour, flavour_storage in self.current[company].items():
                lst.append(flavour_storage)

        return lst

    def get_flavours(self):
        lst=[]
        for _, flavour in self.flavours.items():
            lst.append(flavour)
        return lst

    def add_company(self, company):
        if company.company_name in self.companies.keys():
            return

        self.companies[company.company_name] = company
        self.current[company] = {}

    def get_companies(self):
        return [comp for _, comp in self.companies.items()]

    def add_flavour_to_storage(self, flavour: Flavour):
        if flavour in self.current[flavour.company].keys():
            self.current[flavour.company][flavour].add_new()
            return

        self.add_flavour(flavour)
        self.current[flavour.company][flavour] = FlavourStorage(flavour)

    def add_flavour(self, flavour: Flavour):
        if flavour.company.company_name not in self.companies.keys():
            self.add_company(flavour.company)
        self.flavours[flavour.name+"_"+flavour.company.company_name] = flavour

    def get_flavour(self, flavour_name, company_name):
        return self.flavours[flavour_name+"_"+company_name]

    def get_flavour_from_storage(self, flavour: Flavour) -> FlavourStorage:
        return self.current[flavour.company][flavour]

    def add_recipe(self, recipe: Recipe):
        ingredients = {}

        for f_name, proc in recipe.ingredients.items():
            ingredients[self.get_flavour(f_name,"The Flavour Apprentice" if proc[1]=="TFA" else proc[1])] = proc

        if recipe.name not in self.recepies:
            self.recepies[recipe.name] = {}

        self.recepies[recipe.name][recipe.procentage] = Recipe(recipe.name, ingredients)

    def get_recipe(self, name):
        return self.recepies[name]

    def create_recipe(self, _recepie: Recipe, volume):
        if not self.could_it_be_made(_recepie,volume)[0]:
            return False

        recepie = self.recepies[_recepie.name][_recepie.procentage]
        for flavour, (precentage, _) in recepie.ingredients.items():
            storage_flavour = self.get_flavour_from_storage(flavour)
            storage_flavour.current_volume += - precentage * 0.01 * volume

    def could_it_be_made(self, _recepie: Recipe, volume):
        recepie = self.recepies[_recepie.name][_recepie.procentage]
        what_remains = {}
        for flavour, (precentage, _) in recepie.ingredients.items():
            current_vol = self.get_flavour_from_storage(flavour).current_volume
            remaining_vol = current_vol - precentage * 0.01 * volume
            if remaining_vol < 0:
                return False, "%s current %f needed %f" % (flavour.name, current_vol, remaining_vol)
            what_remains[flavour.name] = remaining_vol

        return True, what_remains
