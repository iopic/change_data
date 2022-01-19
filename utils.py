import pandas as pd
import json
from datetime import datetime
from itertools import combinations

import numpy as np

def prep_data(df,val_col='Count',title_prefix=''):
    cat = [x for x in df.columns if x != val_col][0]
    values = df['Count'].tolist()
    labels = df[cat].tolist()
    return {'title':''+cat, 'values':values,'labels':labels}


def special_processing(df, col_name,val_col):
    if col_name == 'some value':
        #do something
        pass
    else:
        group_df = df.groupby([col_name]).size().reset_index(name=val_col)


def single_groupby(df,val_col = 'Count',exclude_cols=[]):
    """
    create all possible single variable rollups for a given df, applying name of val_col
    to counts
    if include exclude cols, won't make tables for those (i.e. time)
    """
    dfs = []
    for col in [x for x in df.columns if x not in exclude_cols]:
        #can insert the special conditioning certain columns need -- group_df = special_processing()
        group_df = df.groupby([col]).size().reset_index(name=val_col)
        dfs.append(group_df.copy())
    return dfs

def double_groupby(df,cat_col1, cat_col2, time_col = 'Date',val_col = 'Count',exclude_cols=[]):
    """
    create all possible double variable rollups for a given df, applying name of val_col
    to counts
    if include exclude cols, won't make tables for those (i.e. time)
    """
    dfs = []
    exclude_cols.append(time_col)
    to_combine = [x for x in df.columns if x not in exclude_cols]
    possible_pairs = combinations(to_combine, r=2)
    for pair in possible_pairs:
        #can insert the special conditioning certain columns need -- group_df = special_processing()
        group_df = df.groupby(pair).size().reset_index(name=val_col)
        dfs.append(group_df.copy())
    return dfs


def time_groupby(df,time_col,count_col='Count',exclude_cols=[]):
    """
    creates all possible time groupbys, with no other variables:
    time alone as counts - month, quarter, year rollups
    time with another variable too
    """

    #make index datetime
    df.index = pd.to_datetime(df[time_col],format='%d/%m/%Y')

    dfs = []
    #first with single variable/time combo, and without the variable
    exclude_cols.append(time_col)
    for col in [x for x in df.columns if x not in exclude_cols]:
        group2_df_m = df.groupby([pd.Grouper(freq='M'),col]).size().reset_index(name=count_col)
        #remake index as time
        #group2_df.index = pd.to_datetime(group2_df[time_col],format='%Y-%m-%d')
        group2_df_m['Date'] = group2_df_m.Date.dt.to_period('M').dt.strftime('%Y_%m')

        group2_df_q = df.groupby([pd.Grouper(freq='Q'),col]).size().reset_index(name=count_col)
        #remake index as time
        #group2_df.index = pd.to_datetime(group2_df[time_col],format='%Y-%m-%d')
        group2_df_q['Date'] = group2_df_q.Date.dt.to_period('M').dt.strftime('Q%q_%Y')

        dfs += [group2_df_m.copy(), group2_df_q.copy()]
    #then do single rollups at month/quarter/year levels
    group_df_m = df.groupby(pd.Grouper(freq='M')).size().reset_index(name=count_col)
    group_df_q = df.groupby(pd.Grouper(freq='Q')).size().reset_index(name=count_col)
    #extra formatting if we care
    group_df_m['Date'] = group_df_m.Date.dt.to_period('M').dt.strftime('%Y_%m')
    group_df_q['Date'] = group_df_q.Date.dt.to_period('Q').dt.strftime('Q%q_%Y')

    dfs += [group_df_m, group_df_q]


    return dfs

def load_data():
    df = pd.read_csv('/Users/samahol/Documents/change_data/instance/covid_impact_education.csv')
    #make a couple of df
    val_col = 'Count'
    #generate single groupby dfs
    dfs = single_groupby(df,val_col=val_col)

    chart_data = []
    for df in dfs:
        chart_data.append(prep_data(df))
    return chart_data

