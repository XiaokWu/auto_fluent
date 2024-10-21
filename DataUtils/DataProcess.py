import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import conf.liquids as liq
from DataUtils.DataKit import Kit
from DataUtils.DataKit import DataLoader
import conf.Parameters as Parameters

def resultLoder(path):
    data = pd.read_csv(path, delimiter=',')
    data.rename(columns={
        'inlet_velocity':'InflowSpeed',
        'outlet_avg_temperature':'T_outflow',
        'heatsink_avg_temperature':'T_avg_heatsink',
        'heatsink_max_temperature':'T_max_heatsink',
        'inlet_avg_temperature':'T_inflow',
        'inlet_avg_pressure':'P_inflow',
        'outlet_avg_pressure':'P_outflow'
        },inplace=True)
    return data

        
def get_relativeErro(Meshs, base, Re, compare_cloumn):
    erorFrame = pd.DataFrame()
    for x in Re:
        addon = pd.DataFrame()
        addon['Re'] = [x]
        base_slic = base[base['Re']==x]
        i=1
        for mesh in Meshs:
            mesh_slic = mesh[mesh['Re']==x]
            addon[f'error_{i}'] = abs(mesh_slic[compare_cloumn].values-base_slic[compare_cloumn].values)*100/mesh_slic[compare_cloumn].values
            i+=1
        erorFrame = pd.concat([erorFrame,addon], ignore_index=True)
        
    for i in range(1,6):
        plt.plot(erorFrame['Re'], erorFrame[f'error_{i}'],'.-',label = f'errror_{i}')
    plt.xlabel('Re')
    plt.ylabel('Error(%)')
    plt.legend()
    plt.show()
    
    return erorFrame


def get_relativeData(Meshs, basefeatrue, baseScale, featrueColumn_y, plot):
    outFrame = pd.DataFrame()
    i=1
    for mesh in Meshs:
        addon = pd.DataFrame()
        mesh_slic = mesh[mesh[basefeatrue] == baseScale]
        addon[featrueColumn_y] = mesh_slic[featrueColumn_y]
        addon['mesh'] = i
        i+=1
        outFrame = pd.concat([outFrame,addon], ignore_index=True)
        
    if plot:
        plt.scatter(outFrame['mesh'],outFrame[featrueColumn_y])
        plt.show()
    
    return outFrame

    
    
def plot_data(heatsinks,feature_x,feature_y):
    i=1
    for heatsink in heatsinks:
        heatsink=heatsink.sort_values(by='%s'%feature_x,ascending=True)
        plt.plot(heatsink['%s'%feature_x],heatsink['%s'%feature_y], '.-', label='heatsink_%d'%i)
        i+=1
    plt.legend()
    plt.xlabel('%s'%feature_x)
    plt.ylabel('%s'%feature_y)
    plt.title('%s-%s figure of different heatsink'%(feature_x,feature_y))
    plt.tight_layout()
    plt.show()

def DataProcess():
    print('\n ###########################################  DataProcess  ###########################################')
    print('##################################  Extracting data from the result file  ###############################')
    output_data = DataLoader.output(Parameters.result_folder,Parameters.output_features)
    print('\n \n ##################################  Data extraction completed  #######################################')
    print(output_data)
    pd.DataFrame.to_csv(output_data, 'output.csv',index=False)
    
    # df = resultLoder('output.csv')
    # coolent = liq.Water()
    # inletSurface = 0.052**2
    # Re = df['Re']
    # lst_heatsink = [1,2]
    # dct_heatsink_df = {}
    # heatflux = 10000
    # for heatink_idx in lst_heatsink:
    #     dct_heatsink_df[f'heatsink_{heatink_idx}'] = df[df['heatsink']==heatink_idx]
    
    # for df in dct_heatsink_df.values():
    #     Kit.fluid().get_massFlow(df,coolent)
    #     Kit.heat().get_ThermalResistance_OFheatsink (df)
    #     Kit.heat().get_nusseltNumber_OFheatsink(df)
    #     Kit.fluid().get_Delta_P(df)
    #     Kit.heat().get_heatCo(df)
    
    # heatsinks = dct_heatsink_df.values()
    # print(heatsinks)
    # plot_data(heatsinks,'Re','h/Delta_P')
    
    
    
    
    
