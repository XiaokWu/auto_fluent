class Liquid:
    def __init__(self, density, viscosity, prandtl_number,spec_heat,thermal_conductivity):
        self.density = density
        self.viscosity = viscosity
        self.prandtl_number = prandtl_number
        self.spec_heat = spec_heat
        self.thermal_conductivity = thermal_conductivity

class Water(Liquid):
    def __init__(self):
        super().__init__(997.0, 0.001, 7.0, 4186.0, 0.606)

class Air(Liquid):
    def __init__(self):
        super().__init__(1.225, 0.000018, 0.7, 1006.43, 0.0242)

class Oil(Liquid):
    def __init__(self):
        super().__init__(850.0, 0.1, 100.0, 2000.0, 0.15)

class Mercury(Liquid):
    def __init__(self):
        super().__init__(13500.0, 0.001, 0.025, 140.0, 8.5)

def Extract_fluid(name_fluid):
    dct_water = {
        'name': ['water', 'H2O', 'Water'],
        'val' : Water()
    }

    dct_air = {
        'name': ['air', 'Air'],
        'val' : Air()
    }

    dct_oil = {
        'name': ['oil', 'Oil'],
        'val' : Oil()
    }

    dct_mercury = {
        'name': ['mercury', 'Mercury'],
        'val' : Mercury()
    }
    
    lst_fluids = [dct_water, dct_air, dct_oil, dct_mercury]
    for dct in lst_fluids:
        if name_fluid in dct['name']:
            return dct['val']
    
    