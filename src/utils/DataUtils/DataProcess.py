import pandas as pd
from src.utils.DataUtils.DataKit import DataLoader_beta as DataLoader
import src.conf.Parameters as Parameters
import src.utils.DataUtils.Plot as Plot

def DataProcess():
    print('\n ###########################################  DataProcess  ###########################################')
    if not Parameters.plot_only:
        print('##################################  Extracting data from the result file  ###############################')
        dct_output_data = DataLoader.output(Parameters.result_folder,Parameters.outputs_infos)
        print('\n \n ##################################  Data extraction completed  #######################################\n\n')
        for key, value in dct_output_data.items():
            value.rename(columns={
                'case':Parameters.outputs_infos['case_label']
            }, inplace=True)
            print(f'\n\n#######################{key} : {value.shape}#######################')
            print(value)
            pd.DataFrame.to_csv(value, f'out_{key}.csv',index=False)
    if is_plot():
        check_plot()
        df = resultLoder(Parameters.reslut_file_name)
        label_feature, feature_x, feature_y, geometry, plot_additional_feature = Parameters.label_feature, Parameters.feature_x, Parameters.feature_y, Parameters.geometry,Parameters.plot_additional_feature
        Plot.plot_beta(df, label_feature, feature_x, feature_y, geometry, plot_additional_feature)
    
def check_plot():
    output_features = list(Parameters.rename.values())+Parameters.plot_additional_feature+[Parameters.case_label]+list(Parameters.simulation_variables.keys())
    for feature in [Parameters.feature_x, Parameters.feature_y, Parameters.label_feature]:
        if feature not in output_features:
            raise KeyError(f"Cann't plot: {feature} not in output_features or not calculated")
        
def is_plot():
    if not Parameters.on_server:
        return True
    else:
        if Parameters.plot_on_server:
            return True
    
def resultLoder(path):
    data = pd.read_csv(path, delimiter=',')
    data.rename(columns=Parameters.rename,inplace=True)
    return data
    
    
    
    
    