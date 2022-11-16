# import statements
import pandas as pd
from IPython.display import display

# import the data
# I am including two search terms here to compare results
search_df1 = pd.read_csv("recession_search_data.csv", header=1)
search_df2 = pd.read_csv("peach_search_data.csv", header=1)
stock_df = pd.read_csv("^GSPTSE.csv")

search_df1.rename(columns={search_df1.columns[1]: "search_freq1"},
                  inplace=True)
search_df2.rename(columns={search_df2.columns[1]: "search_freq2"},
                  inplace=True)

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
# Moves 'Week' column to the front of the df
main_df.insert(0, 'Week', main_df.pop('Week'))


def norm_min_max(df, cols):
    for col in cols:
        df[col] = df[col] / df[col].abs().max()


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


# price_movement(main_df, 'Adj Close')

norm_min_max(main_df, ['Adj Close', 'search_freq1', 'search_freq2'])


main_df.plot(x='Date', y=['Adj Close', 'search_freq1', 'search_freq2'])


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


print(measure_correlation(main_df, ['Adj Close', 'search_freq1']))
print(measure_correlation(main_df, ['Adj Close', 'search_freq2']))

print(measure_correlation2(main_df, ['Adj Close', 'search_freq1']))
print(measure_correlation2(main_df, ['Adj Close', 'search_freq2']))
