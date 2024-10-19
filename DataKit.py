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
        
        @staticmethod
        def get_heatsink_type(result_name):
            return result_name.split(',')[0].split('_')[1]

        @staticmethod
        def get_variable_info(variable):
            variable_type = variable.split('=')[0]
            variable_value = variable.split('=')[1] 
            return variable_type, variable_value

        @staticmethod
        def get_max_value(df, column):
            return df[column].max()

        @staticmethod
        def get_avg_value(df, column):
            return df[column].mean()

        @staticmethod
        def get_min_value(df, column):
            return df[column].min()


        def get_dct_feature_info(lst_feature):
            '''
            Get the dictionary of feature information
            '''
            dct = {}
            dct['variable'] = []
            for feature in lst_feature:
                feature_info = feature.split('_')
                if len(feature_info) == 1:
                    dct['variable'].append(feature)
                else:
                    face_name = feature_info[0]
                    if face_name not in dct.keys():
                        dct[face_name] = []
                    dct[face_name].append({feature_info[2]:feature_info[1]})
            return dct

        def extract_data_from_file(df_result,result_file_name, dct_feature_info):
            '''
            Extract the data from the csv file
            '''
            dct_data_kit = {
                'avg':DataLoader.get_avg_value,
                'max':DataLoader.get_max_value,
                'min':DataLoader.get_min_value
            }
            result = result_file_name
            result_face = result.split('_')[2].split('.')[0]
            variable = result.split('_')[1].split(',')[1]
            df_result.rename(columns={
                'velocity-magnitude':'velocity'
            }, inplace=True)
            df_result_addon = pd.DataFrame()
            df_result_addon['heatsink'] = [DataLoader.get_heatsink_type(result)]
            df_result_addon[DataLoader.get_variable_info(variable)[0]] = [DataLoader.get_variable_info(variable)[1]]
            if result_face in dct_feature_info.keys():
                for dct in dct_feature_info[result_face]:
                    physical_value = list(dct.keys())[0]
                    value_type = list(dct.values())[0]
                    if value_type in dct_data_kit.keys():
                        addon_value = dct_data_kit[value_type](df_result, physical_value)
                        df_result_addon[f"{result_face}_{value_type}_{physical_value}"] = [addon_value]
                    else:
                        raise ValueError(f"Invalid value type {value_type}")
                return df_result_addon
            else:
                pass



        def output(result_folder, features):
            output_data = pd.DataFrame(columns=features)
            dct_feature_info = DataLoader.get_dct_feature_info(features)
            lst_result = os.listdir(result_folder)
            lst_result.sort()
            output_data_line = pd.DataFrame()
            for result in lst_result:
                result_face = result.split('_')[2].split('.')[0]
                if result_face in dct_feature_info.keys():
                    df_result = pd.read_csv(os.path.join(result_folder, result))
                    df_result.columns = df_result.columns.str.strip()
                    addon = DataLoader.extract_data_from_file(df_result, result, dct_feature_info)
                    if output_data_line.empty:
                        output_data_line = addon
                    else:
                        output_data_line = pd.merge(output_data_line, addon, on = dct_feature_info['variable'])
                    if len(output_data_line.columns)==len(features):
                        # 排除空或全NA的条目
                        output_data_line = output_data_line.dropna(how='all')
                        if not output_data_line.empty:
                            output_data = pd.concat([output_data, output_data_line[features]], axis=0)
                        output_data_line = pd.DataFrame()
                    print(f'Processing file : {result}')
            return output_data
                    