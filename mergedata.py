#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


def merge_csv(csv_stock, search1, search2):


    # import the data
    # I am including two search terms here to compare results
    search_df1 = pd.read_csv(search1, header=1)
    search_df2 = pd.read_csv(search2, header=1)
    stock_df = pd.read_csv(csv_stock)

    search_df1.rename(columns={search_df1.columns[1]: "search_freq1"}, inplace=True)
    search_df2.rename(columns={search_df2.columns[1]: "search_freq2"}, inplace=True)

    # Use .head() to show the start of the data frame and .tail() to show the end
    display(pd.concat([search_df1.head(3), search_df1.tail(3)]))
    display(pd.concat([search_df2.head(3), search_df2.tail(3)]))
    display(pd.concat([stock_df.head(3), stock_df.tail(3)]))

    # dropping mismatching rows
    stock_df = stock_df.drop(index=[0, 1, 261])
    search_df1 = search_df1.drop(index=[0])
    search_df2 = search_df2.drop(index=[259])

    # reindexing the df's so they merge properly
    stock_df.index = range(len(stock_df))
    search_df1.index = range(len(search_df1))
    search_df2.index = range(len(search_df2))

    # Merging the df's
    main_df = stock_df.join(search_df1).join(search_df2["search_freq2"])
    main_df.insert(0, 'Week', main_df.pop('Week'))  # Moves 'Week' column to the front of the df

    # initializing change in search frequency variable
    change_df = pd.DataFrame()
    change_df[0] = 0

    # adds the data of the change in search frequencies per week into the variable
    for i in range(1, len(search_df1)):
        change_df[i] = search_df1.loc[i] - search_df1.loc[i - 1]

    # merge the df into the table
    change_df.rename(columns={change_df.columns[1]: "change_in_searches"}, inplace=True)
    main_df = main_df.join(change_df["change_in_search1"])


    main_df


merge_csv("^GSPTSE.csv","peach_search_data.csv", "recession_search_data.csv" )


# In[ ]:





# In[ ]:




