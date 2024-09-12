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