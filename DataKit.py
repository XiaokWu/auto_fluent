import os
import pandas as pd
import numpy as np


class Kit:
    """_summary_
    """
    pass

    class fluid:
        
        @staticmethod    
        def get_Re(df, coolent):
            df['Re'] = df['InflowSpeed']*coolent.density*0.002/coolent.viscosity
            
        @staticmethod
        def get_massFlow(df, coolent):
            df['massFlow'] = df['InflowSpeed']*coolent.density*0.002
            
        @staticmethod
        def get_Delta_P(df):
            df['Delta_P'] = df['P_outflow']-df['P_inflow']

    class heat:
        
        @staticmethod
        def get_ThermalResistance(heatFlux, Delta_T, heatSurface=0.052**2):
            return Delta_T/(heatFlux*heatSurface)
        
        @staticmethod
        def get_nusseltNumber(ThermalResistance, coolent, chara_length):
            return (1/(ThermalResistance*chara_length**2))*chara_length/coolent.thermal_conductivity

        @staticmethod
        def get_ThermalResistance_OFheatsink(heatsink):
            HeatFlux = 10000
            T_heatsink = heatsink['T_max_heatsink']
            T_mean_fluid = (heatsink['T_outflow']+heatsink['T_inflow'])/2
            Delta_T = T_heatsink-T_mean_fluid
            heatsink['ThermalResistance'] = Kit.heat().get_ThermalResistance(HeatFlux, Delta_T)

        @staticmethod
        def get_nusseltNumber_OFheatsink(heatsink):
            heatsink['Nu'] = Kit.heat().get_nusseltNumber(heatsink['ThermalResistance'])

        @staticmethod
        def get_Delta_P(heatsink):
            heatsink['Delta_P'] = heatsink['P_outflow']-heatsink['P_inflow']

        @staticmethod
        def get_heatCo(heatsink):
            heatsink['h/Delta_P'] = -1/heatsink['Delta_P']*heatsink['ThermalResistance']

class DataLoader(Kit):    
        def __init__(self, inlet_postion, outlet_postion, output_features, output_folder) -> None:
            self.inlet_postion = inlet_postion
            self.outlet_postion = outlet_postion
            self.output_features = output_features
            self.output_folder = output_folder
        
        def extract_surface_result(inlet_position, outlet_position, result):
            inlet_result = result[result['x-coordinate']==inlet_position]
            outlet_result = result[result['x-coordinate']==outlet_position]
            return inlet_result, outlet_result
        
            
        def resultLoder(path):
            df = pd.read_csv(path, delimiter=',')
            df.columns = df.columns.str.replace(" ", "")
            return df
        
        def temperature_data(result, zone):
            avg_temperature = result['temperature'].mean()-273.15
            max_temperature = result['temperature'].max()-273.15
            return avg_temperature if zone == 'out' else max_temperature
        
        def datagather_and_process(self, base,variable):
            print("################# DataProcess #################")
            result_folder = os.path.join(self.result_folder, self.simulation_name)
            result_list = os.listdir(result_folder)
            feature_columns = self.output_features    
            output_data = pd.DataFrame(columns=feature_columns)
            for label in base:
                for flow in variable:
                    velocity = self.v[variable.index(flow)]
                    addon = pd.DataFrame(columns=feature_columns)
                    addon['heatsink'] = [label]
                    addon['Re'] = [flow]
                    addon['inlet_velocity'] = [velocity]
                    for result_name in result_list:
                        result_info = result_name.split(',')
                        label_name = result_info[0]
                        variable_number = result_info[1]
                        if label_name == label and float(variable_number)== flow:
                            zone = result_info[2]
                            result_path = os.path.join(result_folder, result_name)
                            result = self.resultLoder(result_path)
                            if zone == 'solid':
                                addon['heatsink_avg_temperature'] = result['temperature'].mean()-273.15
                                addon['heatsink_max_temperature'] = result['temperature'].max()-273.15
                            else:
                                inlet_result, outlet_result = self.extract_surface_result(self.inlet_position, self.outlet_position, result)
                                addon["outlet_avg_temperature"] = outlet_result['temperature'].mean()-273.15
                                addon['inlet_avg_temperature'] = inlet_result['temperature'].mean()-273.15
                                addon['outlet_avg_pressure'] = outlet_result['pressure'].mean()
                                addon['inlet_avg_pressure'] = inlet_result['pressure'].mean()

                    output_data=pd.concat([output_data,addon[feature_columns]], axis=0)
                print(f'heatsink{label}done')
            print("########### output ############")
            print(output_data)
            output_path = os.path.join(self.output_folder, f'output_{self.simulation_name}.csv')
            output_data.to_csv(output_path, index=False)
            