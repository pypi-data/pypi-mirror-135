import math
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 999)
pd.set_option('display.max_colwidth', None)
from IPython.display import display_html
from itertools import chain, cycle
import psutil
import time
import re
from re import search

# infolib
def info(dataframe): # cambiare in info

    """
    info(dataframe)

    Parameters:
    	(dataframe): pandas.DataFrame object

    Returns:
    	pandas.DataFrame stat overview
    """

    target = "https://github.com/AntonelloManenti/infolib"

    def convert_size(size_bytes):
        if size_bytes==0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def display_side_by_side(*args, titles = cycle([''])):
        html_str = ''
        for df, title in zip(args, chain(titles, cycle(['</br>'])) ):
            html_str+='<th style="text-align:center"><td style="vertical-align:top">'
            html_str+=f'<h3>{title}</h3>'
            html_str+=df.to_html().replace('table', 'table style="display:inline"')
            html_str+='</td></th></br></br>'
        display_html(html_str, raw=True)
        return

    if isinstance(dataframe, pd.DataFrame)==False:
        print(f"This function expects PandasDataframe argument.\n{type(dataframe)} is not a valid argument.\n\nFor more info about info() visit {target}")

    else:
        if dataframe.empty==True:
            display_side_by_side(dataframe, titles=[f"Warning! Your PandasDataframe is empty"])
            print(f"\n\nFor more info about info() visit {target}"")
        else:
            try:
                Df_desc = {'dataset': [], 'columns': [], 'rows': [], 'rows_whitout_NaN': [], 'rows_whit_NaN':[], 'rows_duplicate':[],
                           'rows_unique':[], 'memory_usage':[]}

                namedf = 'dataframe'
                Df_desc['dataset'].append(namedf)

                try:
                    if not isinstance(dataframe.index, pd.MultiIndex):

                        if dataframe.index.name==None and 'index' not in dataframe.columns: # crea index ma se c'è index in un'altra colonna qualsiasi crea level_0 e se c'è già da errore

                            dataframes = dataframe.reset_index()
                            dataframes = dataframes.drop('index', axis=1)

                        else:

                            if dataframe.index.name=='index' or 'index' in dataframe.columns: # crea level0 e se c'è level_0 da errore
                                dataframes = dataframe.rename(columns={'index': 'index_test'})
                                dataframes = dataframes.reset_index()
                                dataframes = dataframes.drop('index', axis=1)
                                dataframes = dataframes.rename(columns={'index_test': 'index'})

                            else: # non crea nulla
                                dataframes = dataframe.reset_index()

                    if isinstance(dataframe.index, pd.MultiIndex):
                        dataframes = dataframe.reset_index()
                        for i in dataframes.columns:
                            if re.search(r'level_', i):
                                dataframes.drop(i, axis=1, inplace=True)

                except Exception as e:
                    print(f'Maybe there are one or more columns named level_ *. You need to change the name of those columns.\n\nFor more info about info() visit {target}')
                    print(repr(e))

                i = len(dataframes.columns)
                Df_desc['columns'].append(i)

                i = len(dataframes.index)
                Df_desc['rows'].append(i)

                i = len(dataframes.index)-len(dataframe.drop_duplicates())
                Df_desc['rows_duplicate'].append(i)

                i = len(dataframes.index)-(len(dataframe.index)-len(dataframe.drop_duplicates()))
                Df_desc['rows_unique'].append(i)

                i = len(dataframes.index)-(len(dataframe[dataframe.isna().any(axis=1)].index))
                Df_desc['rows_whitout_NaN'].append(i)

                i = len(dataframes[dataframes.isna().any(axis=1)].index)
                Df_desc['rows_whit_NaN'].append(i)

                i = dataframes.memory_usage(deep=True, index=True).sum()
                i = convert_size(i)
                Df_desc['memory_usage'].append(i)

                DataFrames = pd.DataFrame.from_dict(Df_desc, orient='columns')
                DataFrames = DataFrames.set_index('dataset')
                DataFrames.index.name = None

                Tot_desc_num = {'feature_name': [], 'dtypes': [], 'not_NaN': [], 'NaN': [], 'unique':[],
                          'mean':[], 'std':[], 'min':[], 'max':[], '25%':[], '50%':[], '75%':[]}
                Tot_desc_cat = {'feature_name': [], 'dtypes': [], 'not_NaN': [], 'NaN': [], 'unique':[],
                          'top':[], 'freq':[], 'min_len':[], 'max_len':[]}


                for i in dataframes.columns:

                    if search('int', dataframes[i].dtype.name) or search('float', dataframes[i].dtype.name):

                        Tot_desc_num['feature_name'].append(i)

                        a = dataframes[i].dtypes
                        Tot_desc_num['dtypes'].append(a)

                        a = dataframes[i].count()
                        Tot_desc_num['not_NaN'].append(a)

                        a = dataframes[i].isna().sum()
                        Tot_desc_num['NaN'].append(a)

                        a = dataframes[i].nunique()
                        Tot_desc_num['unique'].append(a)

                        a = round(dataframes[i].mean(),3)
                        Tot_desc_num['mean'].append(a)

                        a = round(dataframes[i].std(),3)
                        Tot_desc_num['std'].append(a)

                        a = round(dataframes[i].min(),3)
                        Tot_desc_num['min'].append(a)

                        a = round(dataframes[i].max(),3)
                        Tot_desc_num['max'].append(a)

                        a = round(dataframes[i].quantile(0.25),3)
                        Tot_desc_num['25%'].append(a)

                        a = round(dataframes[i].quantile(0.5),3)
                        Tot_desc_num['50%'].append(a)

                        a = round(dataframes[i].quantile(0.75),3)
                        Tot_desc_num['75%'].append(a)

                    else:
                        Tot_desc_cat['feature_name'].append(i)

                        a = dataframes[i].dtypes
                        Tot_desc_cat['dtypes'].append(a)

                        a = dataframes[i].count()
                        Tot_desc_cat['not_NaN'].append(a)

                        a = dataframes[i].isna().sum()
                        Tot_desc_cat['NaN'].append(a)

                        a = dataframes[i].nunique()
                        Tot_desc_cat['unique'].append(a)

                        a = dataframes[i].value_counts().idxmax()
                        Tot_desc_cat['top'].append(a)

                        a = dataframes[i].value_counts()
                        a = a.iloc[0]
                        Tot_desc_cat['freq'].append(a)

                        a = []
                        for ii in dataframes[i].astype(str):
                            b = len(ii)
                            a.append(b)
                        ma = max(a)
                        mi = min(a)
                        Tot_desc_cat['max_len'].append(ma)
                        Tot_desc_cat['min_len'].append(mi)

                Numerical_Features = pd.DataFrame.from_dict(Tot_desc_num, orient='columns')
                Numerical_Features = Numerical_Features.set_index('feature_name')
                Numerical_Features.index.name = None

                Categorical_Features = pd.DataFrame.from_dict(Tot_desc_cat, orient='columns')
                Categorical_Features = Categorical_Features.set_index('feature_name')
                Categorical_Features.index.name = None

                Sample = dataframe.sample(3)

                if not DataFrames.empty:
                    if not Numerical_Features.empty:
                        if not Categorical_Features.empty:
                            print()
                            display_side_by_side(DataFrames, Numerical_Features, Categorical_Features, Sample, titles = [f'Overview of {namedf}','Numeric Features', 'Other Features', f'Sample of {namedf}'])

                if not DataFrames.empty:
                    if not Numerical_Features.empty:
                        if Categorical_Features.empty:
                            print()
                            display_side_by_side(DataFrames, Numerical_Features, Sample, titles = [f'Overview of {namedf}','Numeric Features', f'Sample of {namedf}'])

                if not DataFrames.empty:
                    if Numerical_Features.empty:
                        if not Categorical_Features.empty:
                            print()
                            display_side_by_side(DataFrames, Categorical_Features, Sample, titles = [f'Overview of {namedf}', 'Features', f'Sample of {namedf}'])

            except Exception as e:
                print(repr(e))
                print(f'For more info about info() visit {target}')

    return
