import json

    
def get_dct_fluid():
    with open(r'src/conf/fluid_database.json') as f:
        dct_fluid = json.load(f)
    return dct_fluid
    
dct_fluid = get_dct_fluid()

def Extract_fluid(name_fluid, dct_fluid=dct_fluid):
    for key, values in dct_fluid.items():
        if name_fluid in values['name']:
            return key, values
