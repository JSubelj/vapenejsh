from entities import *

def dict_to_string(dictionary, no_print=True):
    string = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            string += '{ ' + str(key) + ' : {' + str(dict_to_string(value, no_print=False)) + '} }'
        else:
            string += '{ ' + str(key) + ' : {' + str(value) + '} }'
    print(string)

def list_to_string(lst):
    string = "["
    for i in lst:
        string+=str(i)+",\n"
    string += "]"
    return string

if __name__ == "__main__":
    import sys

    print(hasattr(sys,"real_prefix"))
    MyStorage = Storage()

    nic = Nicotine(18, 10, 1.5)
    base = Base((50, 50), 1000, 15)
    nicbase = NicBase(base, nic, 100, no_of_shots=2)

    TFA = Company("The Flavour Apprentice",3.95,15)
    '''lynchee = TFA_F("Lynchee")
    pear = TFA_F("Pear")

    ingr = {"Lynchee": (4,"TFA"), "Pear": (6,"TFA")}
    rec = Recipe("krneki", ingr)
    rec2 = Recipe("bla",ingr)
    rec1 = rec.norm_procentage_to(100)

    MyStorage.add_flavour(lynchee)
    MyStorage.add_flavour(pear)
    MyStorage.add_flavour_to_storage(lynchee)
    MyStorage.add_flavour_to_storage(pear)
    MyStorage.add_recipe(rec)
    MyStorage.add_recipe(rec1)
    MyStorage.add_recipe(rec2)
    '''
    #print(MyStorage.current[TFA()])
    #print(list_to_string(MyStorage.get_recepies()))
    #print(list_to_string(MyStorage.get_flavours()))
    #print(MyStorage.current)
    #MyStorage.create_recipe(rec1,10)
    #print(list_to_string(MyStorage.get_current()))
    #print(list_to_string(MyStorage.get_companies()))
    import json
    #print(json.dumps(json.loads(MyStorage.jsonify_companies()),indent=4,sort_keys=True))
    #print(json.loads(MyStorage.jsonify_flavours()))
    #print(json.loads(MyStorage.jsonify_recepies()))
    #print(json.loads(MyStorage.jsonify_current()))
    #print(MyStorage.could_it_be_made(rec,100))