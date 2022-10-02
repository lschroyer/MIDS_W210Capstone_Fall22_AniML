import numpy as np
from datetime import datetime,timedelta, date
import pandas as pd
import sqlite3
import json



#loading data
def load_data():

    # Read sqlite query results into a pandas DataFrame
    # con = sqlite3.connect("amzn-products.db")
    con = sqlite3.connect("products.db")
    df = pd.read_sql_query("SELECT * from product ", con)

    # Verify that result of SQL query is stored in the dataframe
    print(df.head(5))

    con.close()
    
    return df

def load_category_data(category_name):

    # Read sqlite query results into a pandas DataFrame

    # con = sqlite3.connect("amzn-products.db")
    con = sqlite3.connect("products.db")
   
    sql = 'select * from product where category = "{}"'.format(category_name)
    
    df = pd.read_sql_query(sql, con)
    
    # Verify that result of SQL query is stored in the dataframe
    print(df.head(5))

    con.close()

    return df

## Data Cleaning
def clean_data(df):
    # Trim spaces in all columns in the dataframe

    def trim_all_columns(df):
        # Trim whitespace from ends of each value across all series in dataframe    
        trim_strings = lambda x: x.strip() if isinstance(x, str) else x
        return df.applymap(trim_strings)

    # simple example of trimming whitespace from data elements
    df = trim_all_columns(df)
    print(df)
    
    
    # Fixing Currency Columns 

    # Est_Monthly_Revenue
    # df.Est_Monthly_Revenue = [x.strip('$') for x in df.Est_Monthly_Revenue]
    # df.Est_Monthly_Revenue = df.Est_Monthly_Revenue.str.replace(',', '').astype(float)

    # Est_Monthly_Sales
    # df.Est_Monthly_Sales = df.Est_Monthly_Sales.str.replace(',', '').astype(float)

    # Price
    df.Price = [x.strip('$') for x in df.Price]
    df.Price = df.Price.str.replace(',', '').astype(float)

    # Fees
    # df.Fees = [x.strip('$') for x in df.Fees]
    # df.Fees = df.Fees.str.replace(',', '').astype(float)

    # Net
    # df.Net = [x.strip('$') for x in df.Net]
    # df.Net = df.Net.str.replace(',', '').astype(float)

    # Check Data Type in Rank
    # See different data types in the same column.  

    ### Fixing Rank column
    df['Rank'].apply(type)
    
    # Check Data Type in Rank
    # See different data types in the same column. 
    df['Rank'].apply(type).value_counts()


    def clean_rank_data(x):
        # If the value is a string, then remove currency symbol, delimiters, and N.A.
        # otherwise, the value is numeric and can be converted
        if isinstance(x, str):
            return(x.replace('$', '').replace(',', '').replace('N.A.','0'))
        return(x)
    
    # Clean data and convert to float data type
    df['Rank'] = df['Rank'].apply(clean_rank_data).astype('float')
    
    # Check Data Type in Rank
    # See float data types in the column. 
    df['Rank'].apply(type).value_counts()

    ### Fixing Est_Monthly_Revenue, Est_Monthly_Sales, Fees, and Net columns
    
    # Check Data Type in Est_Monthly_Revenue
    # See different data types in the same column.  
    df['Est_Monthly_Revenue'].apply(type)
    
    # Check Data Type in Est_Monthly_Revenue
    # See different data types in the same column. 
    df['Est_Monthly_Revenue'].apply(type).value_counts()
    
    def clean_Revenue_Sales_Fees_Net_data(x):
        # If the value is a string, then remove currency symbol, delimiters, and N.A.
        # otherwise, the value is numeric and can be converted

        if isinstance(x, str):
            return(x.replace('$', '').replace(',', '').replace('N.A.','0').replace('--','0').replace('< ','-'))
        return(x)
    
    # Clean data and convert to float data type
    df['Est_Monthly_Revenue'] = df['Est_Monthly_Revenue'].apply(clean_Revenue_Sales_Fees_Net_data).astype('float')

    # Clean data and convert to float data type
    df['Est_Monthly_Sales'] = df['Est_Monthly_Sales'].apply(clean_Revenue_Sales_Fees_Net_data).astype('float')

    # Clean data and convert to float data type
    df['Fees'] = df['Fees'].apply(clean_Revenue_Sales_Fees_Net_data).astype('float')

    # Clean data and convert to float data type
    df['Net'] = df['Net'].apply(clean_Revenue_Sales_Fees_Net_data).astype('float')

    # Check Data Type in Est_Monthly_Revenue
    # See float data types in the column. 
    df['Est_Monthly_Revenue'].apply(type).value_counts()

    df.Est_Monthly_Revenue
    

    return df

