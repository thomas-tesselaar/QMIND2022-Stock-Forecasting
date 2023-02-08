#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 16:38:52 2022

@author: thomastesselaar
"""

import pandas as pd
from IPython.display import display


def merge_csv(stock_name:str, search_terms:list[str], pathname = "", 
              stock_rows_to_drop = [0,261], search_rows_to_drop = [], 
              search_suffix = '_search_data', print_head = True):
    
    # import stock data
    stock_df = pd.read_csv(pathname + stock_name + '.csv')
    
    # drop unnecessary columns
    stock_df = stock_df[['Date', 'Adj Close', 'Volume']]
    
    # drop rows which don't lineup and re-index
    stock_df = stock_df.drop(index=stock_rows_to_drop)
    stock_df.index = range(len(stock_df))
    
    for i, search_term in enumerate(search_terms):
        # import search data
        search_df = pd.read_csv(pathname + search_term + search_suffix + '.csv', header=1)
        
        # rename header for uniqueness
        search_df.rename(columns={search_df.columns[1]: "sf_" + str(i)}, inplace=True)
        
        # drop rows which don't lineup and re-index
        search_df = search_df.drop(index=search_rows_to_drop)
        search_df.index = range(len(search_df))
        
        # merge to the main dataframe
        stock_df = stock_df.join(search_df["sf_" + str(i)])
        
    
    # add week to the dataframe
    stock_df = stock_df.join(search_df["Week"])
    stock_df.insert(0, 'Week', stock_df.pop('Week')) 
    
    if(print_head):
        display(stock_df.head(5))
    
    return stock_df


# normalizes numbers to between 0 and 1
def norm_min_max(df, cols):
    for col in cols:
        df[col] = df[col] / df[col].abs().max()
        
# normalizes numbers using z-score
def norm_z_score(df, cols):
    for col in cols:
        df[col] = (df[col] - df[col].mean()) / df[col].std()    
        
"""
Function that will compare the adj. close values to its previous value to check
if the price has gone up or down. 1 for price gone up, -1 for down, 0 for same.
"""

def price_movement(df, cols):
    #  list that will be converted to the price movement column
    price_change = [0]  # starts with 0 because first value doesn't compare
    for i in range(1, len(df)):
        # looping through each value in the column
        if df.iloc[i][cols] > df.iloc[i - 1][cols]:
            price_change.append(1)
        elif df.iloc[i][cols] < df.iloc[i - 1][cols]:
            price_change.append(-1)
        else:
            price_change.append(0)

    df['Price Movement'] = price_change
    

# Gets the change in search frequency and the movement
def search_change(df, num_search_terms):
    for i in range(num_search_terms):
        search_move = [0]
        search_change = [0]  # starts with 0 because first value doesn't compare
        for j in range(1, len(df)):
            # looping through each value in the column
            change_val = df.iloc[j]['sf_' + str(i)] - df.iloc[j - 1]['sf_' + str(i)]
            search_change.append(change_val)
            if(change_val):
                search_move.append(int(change_val/abs(change_val)))
            else:
                search_move.append(0)

        df['Search Change ' + str(i)] = search_change
        df['Search Movement ' + str(i)] = search_move
        


# Gets two, five, and ten week average trailing search frequency
def trailing_search_avg(df, num_search_terms):
    week_lengths = [2,5,10]
    for i in range(num_search_terms):
        for j in week_lengths:
            x_week = []
            last_x_weeks_sum = 0
            for k in range(j-1):
                last_x_weeks_sum += df.iloc[k]['sf_' + str(i)]
                x_week.append(last_x_weeks_sum/(k+1))

            for k in range(j-1, len(df)):
                last_x_weeks_sum += df.iloc[k]['sf_' + str(i)]
                
                x_week.append(last_x_weeks_sum/j)
                
                last_x_weeks_sum -= df.iloc[k-j+1]['sf_' + str(i)]
                
            df[str(j) + ' week avg ' + str(i)] = x_week
            

def one_week_ago_search(df, num_search_terms):
    for i in range(num_search_terms):
        data = [0]  # starts with 0 because first value doesn't compare
        for j in range(1, len(df)):
            # looping through each value in the column
            data.append(df.iloc[j - 1]['sf_' + str(i)])
        
        df['One Week Ago Search ' + str(i)] = data




def derive_columns(df, num_search_terms, print_head = True):
    price_movement(df, 'Adj Close')
    search_change(df, num_search_terms)
    trailing_search_avg(df, num_search_terms)
    one_week_ago_search(df, num_search_terms)
    
    if(print_head):
        display(df.head(5))
    
    
def prep_for_learning(df, normalize = None, print_head = True):
    clean_df = df
    clean_df = clean_df.drop(columns = ['Week', 'Date', 'Adj Close', 'Volume'])
    
    # Moves Price Movement to the end of the df
    clean_df.insert(len(clean_df.columns)-1, 'Price Movement', clean_df.pop('Price Movement'))
    
    # drops first row and re-indexes
    clean_df = clean_df.drop(0)
    clean_df.index = range(len(clean_df))
    
    if(normalize == 'min-max'):
        norm_min_max(clean_df, clean_df.columns)
    elif(normalize == 'z-score'):
        norm_z_score(clean_df, clean_df.columns)
    
    if(print_head):
        display(clean_df.head(5))
    
    return clean_df


# the function for comparing how similar two columns are in their movements
# takes in a dataframe and columns to compare and returns an float between 0
# and 1 representing correlation
# a correlation of near 1 means the two columns share similar peaks and troughs
# a correlation of near 0 means the two columns are inverse to each other
# a correlation of near 0.5 means the two columns are independant, ie. the is
# no correlation
def measure_correlation(df, cols):
    if len(cols) != 2:
        print("Invalid number of columns")
        return -1

    count_same = 0

    for i in range(len(df) - 2):
        if df.iloc[i][cols[0]] < df.iloc[i + 1][cols[0]]:
            a = 1
        elif df.iloc[i][cols[0]] == df.iloc[i + 1][cols[0]]:
            a = 0
        else:
            a = -1

        if df.iloc[i][cols[1]] < df.iloc[i + 1][cols[1]]:
            b = 1
        elif df.iloc[i][cols[1]] == df.iloc[i + 1][cols[1]]:
            b = 0
        else:
            b = -1

        if b == a:
            count_same += 1

    return count_same / (len(df) - 1)


def measure_correlation2(df, cols):
    if len(cols) != 2:
        print("Invalid number of columns")
        return -1
    
    # checks correlation between two columns
    # -1 being more inversely correlated, 1 being more linearly correlated
    # 0 being completely uncorrelated
    correlation = df[cols[0]].corr(df[cols[1]])
    return correlation
    
    


