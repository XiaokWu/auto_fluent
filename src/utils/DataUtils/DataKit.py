import os
import pandas as pd
import src.conf.liquids as liq


class Kit:
    """_summary_
    Kits for dataprocessing
    """
    class fluid:
        
        @staticmethod    
        def get_Re(df, chara_length):
            coolent = liq.get_dct_fluid(df['fluid'])[1]
            density = coolent['density']
            viscosity = coolent['viscosity']
            df['Re'] = df['InflowSpeed']*density*chara_length/viscosity
            
        @staticmethod
        def get_massFlow(df, chara_length):
            coolent = liq.get_dct_fluid(df['fluid'])[1]
            density = coolent['density']
            df['massFlow'] = df['InflowSpeed']*coolent['density']*chara_length
            
        @staticmethod
        def get_Delta_P(df):
            df['Delta_P'] = df['P_outflow']-df['P_inflow']

    class heat:
        
        @staticmethod
        def get_ThermalResistance(heatFlux, Delta_T, heatSurface=0.052**2):
            return Delta_T/(heatFlux*heatSurface)
        
        @staticmethod
        def get_convertive_cof(heatFlux, Delta_T):
            return heatFlux/Delta_T
        
        @staticmethod
        def get_nusseltNumber(h, coolent, chara_length):
            return h*chara_length/coolent['thermal_conductivity']

        @staticmethod
        def get_ThermalResistance_OFheatsink(df):
            HeatFlux = df['heatflux']
            T_heatsink = df['T_max_heatsink']
            T_mean_fluid = (df['T_outflow']+df['T_inflow'])/2
            Delta_T = T_heatsink-T_mean_fluid
            df['ThermalResistance'] = Kit.heat().get_ThermalResistance(HeatFlux, Delta_T)
            
        @staticmethod
        def get_convertive_cof_OFheatsink(df):
            HeatFlux = df['heatflux']
            T_heatsink = df['T_max_heatsink']
            T_mean_fluid = (df['T_outflow']+df['T_inflow'])/2
            Delta_T = T_heatsink-T_mean_fluid
            df['h'] = Kit.heat.get_convertive_cof(HeatFlux, Delta_T)

        @staticmethod
        def get_nusseltNumber_OFheatsink(df, chara_length):
            coolent = liq.Extract_fluid(df['fluid'])[1]
            df['Nu'] = Kit.heat().get_nusseltNumber(df['h'], coolent, chara_length)

        @staticmethod
        def get_Delta_P(df):
            df['Delta_P'] = df['P_outflow']-df['P_inflow']

        @staticmethod
        def get_heatCo(df):
            df['h/Delta_P'] = -1/df['Delta_P']*df['ThermalResistance']

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
    
    def same_list(lst1, lst2):
        '''
        Check if two lists are the same
        '''
        if len(lst1) != len(lst2):
            return False
        for i in range(len(lst1)):
            if lst1[i] != lst2[i]:
                return False
        return True
    
        
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
        try:
            return df[column].max()
        except(KeyError):
            print(f"Invalid column name {column}")

    @staticmethod
    def get_avg_value(df, column):
        try:
            return df[column].mean()
        except(KeyError):
            print(f"Invalid column name {column}")

    @staticmethod
    def get_min_value(df, column):
        try:
            return df[column].min()
        except(KeyError):
            print(f"Invalid column name {column}")


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
                    
class DataLoader_beta(DataLoader):
    def group_result_files(result_folder):
        '''
        Group the result files by the variable
        '''
        dct_result = {}
        lst_result = os.listdir(result_folder)
        lst_result.sort()
        for result in lst_result:
            result_variable = result.split('.')[0].split('_')[0]
            lst_variable = result_variable.split(',')
            lst_variable_name = []
            for variable in lst_variable:
                variable_name = DataLoader.get_variable_info(variable)[0]
                lst_variable_name.append(variable_name)
            if not dct_result:
                key = ','.join(lst_variable_name)
                dct_result[key] = [result]
            else:
                for key in dct_result.keys():
                    if DataLoader.same_list(lst_variable_name, key.split(',')):
                        dct_result[key].append(result)
                        break
                else:
                    key = ','.join(lst_variable_name)
                    dct_result[key] = [result]
        return dct_result
    
    
    
    def extract_data_from_file(df_result,result_file_name, dct_feature_info):
        '''
        Extract the data from the csv file
        '''
        dct_data_kit = {
            'avg':DataLoader.get_avg_value,
            'max':DataLoader.get_max_value,
            'min':DataLoader.get_min_value
        }
        result_info = result_file_name.split('.')[0]
        variable_info = result_info.split('_')[0]
        result_face = result_info.split('_')[1]
        list_variables = variable_info.split(',')
        df_result.rename(columns={
            'velocity-magnitude':'velocity'
        }, inplace=True)
        df_result_addon = pd.DataFrame()
        for variable in list_variables:
            variable_type, variable_value = DataLoader.get_variable_info(variable)
            try:
                variable_value = eval(variable_value)
            except (NameError, SyntaxError):
                pass
            df_result_addon[variable_type] = [variable_value]
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
        
    def output(result_folder, outputs_infos):
        '''
        Output the data from the result files
        '''
        features = outputs_infos['output_features']
        dct_feature_info = DataLoader.get_dct_feature_info(features)
        dct_result_groups =  DataLoader_beta.group_result_files(result_folder)
        dct_output_data = {}
        for group_name, lst_result in dct_result_groups.items():
            lst_result_variables = group_name.split(',')
            dct_feature_info['variable'] = lst_result_variables
            output_features = lst_result_variables + features
            output_data = pd.DataFrame(columns=output_features)
            lst_result.sort()
            output_data_line = pd.DataFrame()
            for result in lst_result:
                result_info = result.split('.')[0]
                try:
                    print(f'Processing file : {result}')
                    result_face = result_info.split('_')[1]
                    if result_face in dct_feature_info.keys():#保证结果文件的面信息在输出特征中
                        df_result = pd.read_csv(os.path.join(result_folder, result))
                        df_result.columns = df_result.columns.str.strip()
                        addon = DataLoader_beta.extract_data_from_file(df_result, result, dct_feature_info)#提取数据
                        if output_data_line.empty:
                            output_data_line = addon
                        else:
                            output_data_line = pd.merge(output_data_line, addon, on = dct_feature_info['variable'])
                        if len(output_data_line.columns)==len(output_features):
                            # 排除空或全NA的条目
                            output_data_line = output_data_line.dropna(how='all')
                            if not output_data_line.empty:
                                output_data = pd.concat([output_data, output_data_line[output_features]], axis=0)
                            output_data_line = pd.DataFrame()
                except (KeyError):
                    print(f'结果文件{result}格式错误')
            dct_output_data[group_name] = output_data
        return dct_output_data