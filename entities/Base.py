# !/usr/bin/env python3

from entities.Storage import Entity

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

if __name__ == "__main__":
    nic = Nicotine(18, 10, 1.5)
    base = Base((50, 50), 1000, 15)
    nicbase = NicBase(base, nic, 100, no_of_shots=2)