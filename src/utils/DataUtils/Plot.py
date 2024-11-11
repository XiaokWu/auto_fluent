from src.utils.DataUtils.DataKit import Kit
import matplotlib.pyplot as plt
import pandas as pd

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
        df_label = df_label.sort_values(by=feature_x,ascending=True)
        plt.plot(df_label[feature_x],df_label[feature_y], '.-', label=f'{label_feature}={label_value}')
    plt.legend()
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    plt.title(f'{feature_x}-{feature_y} figure of different {label_feature}')
    plt.tight_layout()
    plt.show()
    
def calculate_feature_method(df, feature, add_args=None):
    dct_calculate_method = {
        'Re': Kit.fluid().get_Re,
        'massflow': Kit.fluid().get_massFlow,
        'Delta_P': Kit.fluid().get_Delta_P,
        'h/Delta_P': Kit.heat().get_heatCo,
        'h':Kit.heat().get_convertive_cof_OFheatsink,
        'ThermalResistance': Kit.heat().get_ThermalResistance_OFheatsink,
        'Nu': Kit.heat().get_nusseltNumber_OFheatsink,
        'Pr': Kit.heat().get_prandtlNumber
    }
    try:
        dct_calculate_method[feature](df, add_args)
    except TypeError:
        dct_calculate_method[feature](df)
        
def calculate_feature(df,dct_gemoetry,lst_addon_faeatures):
    df_return = pd.DataFrame()
    chara_length = dct_gemoetry['characteristic_length']
    for _ ,row in df.iterrows():
        df_row = row.copy()
        for feature in lst_addon_faeatures:
            calculate_feature_method(df_row, feature, chara_length)
        df_return = pd.concat([df_return, df_row.to_frame().T], axis=0)
    return df_return
        
def plot_beta(df, label_feature, feature_x, feature_y, dct_gemoetry, lst_addon_faeatures):
    Kit.heat().get_convertive_cof_OFheatsink(df)
    df = calculate_feature(df, dct_gemoetry, lst_addon_faeatures)
    print('##############################################################################################')
    print(df)
    plot_data_beta(df, label_feature, feature_x, feature_y)
