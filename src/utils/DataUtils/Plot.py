from src.utils.DataUtils.DataKit import Kit
import matplotlib.pyplot as plt
import pandas as pd
import src.conf.liquids as liq


        
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

def extract_lst_feature(df, feature):
    #提取一个指定特征在dataframe中的所有取值
    lst_value = []
    for value in df[feature]:
        if value not in lst_value:
            lst_value.append(value)
    return lst_value

def plot_data_beta(df, label_feature, feature_x, feature_y):
    lst_label_value = extract_lst_feature(df, label_feature)
    for label_value in lst_label_value:
        df_label = df[df[label_feature]==label_value]
        plt.plot(df_label[feature_x],df_label[feature_y], '.-', label=f'{label_feature}={label_value}')
    plt.legend()
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    plt.title(f'{feature_x}-{feature_y} figure of different {label_feature}')
    plt.tight_layout()
    plt.show()
    
def calculate_feature(df, feature, add_args=None):
    dct_calculate_method = {
        'Re': Kit.fluid().get_Re,
        'massflow': Kit.fluid().get_massFlow,
        'Delta_P': Kit.fluid().get_Delta_P,
        'h/Delta_P': Kit.heat().get_heatCo,
        'Nu': Kit.heat().get_nusseltNumber_OFheatsink,
        'ThermalResistance': Kit.heat().get_ThermalResistance_OFheatsink
    }
    if add_args:
        dct_calculate_method[feature](df, add_args)
    else:
        dct_calculate_method[feature](df)
        
def plot_beta(df, label_feature, feature_x, feature_y, dct_gemoetry, lst_addon_faeatures):
    df = df.sort_values(by=feature_x,ascending=True)
    for feature in lst_addon_faeatures:
        calculate_feature(df, feature)
    plot_data_beta(df, label_feature, feature_x, feature_y)

    

    
# def plot():
#     df = resultLoder('output.csv')
#     Re = df['Re']
#     lst_heatsink = [1,2]
#     dct_heatsink_df = {}
#     heatflux = 10000
#     for heatink_idx in lst_heatsink:
#         dct_heatsink_df[f'heatsink_{heatink_idx}'] = df[df['heatsink']==heatink_idx]
    
#     for df in dct_heatsink_df.values():
#         # Kit.fluid().get_massFlow(df,coolent)
#         Kit.heat().get_ThermalResistance_OFheatsink (df)
#         Kit.heat().get_nusseltNumber_OFheatsink(df)
#         Kit.fluid().get_Delta_P(df)
#         Kit.heat().get_heatCo(df)
    
#     heatsinks = dct_heatsink_df.values()
#     print(heatsinks)
#     plot_data(heatsinks,'Re','h/Delta_P')