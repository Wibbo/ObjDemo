import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import altair as alt


def build_page() -> None:
    """
    Defines a page in the streamlit application.
    :return: None
    """
    sns.set_palette('mako')
    st.markdown("## Looking at retail data")

    df_sales = pd.read_csv('./assets/retail-records.csv', dtype={'CustomerID': str})
    df_sales['InvoiceDate'] = pd.to_datetime(df_sales['InvoiceDate'])
    df_sales['Hour'] = df_sales['InvoiceDate'].dt.hour   
    df_sales.set_index('InvoiceDate', inplace=True)
    df_sales.index = pd.to_datetime(df_sales.index)
    df_months = df_sales.resample('M').sum()
    
    df_rows = df_sales.shape[0]
    df_cols = df_sales.shape[1] 

    st.markdown(f"""This demo loads transaction records from a UK retail organisation
                and provides insights into the data. The data contains the following
                information:""")
    st.markdown('###')
    st.markdown(f"""
                - Invoice number
                - Stock code
                - Product description
                - Quantity
                - Unit price
                - Customer ID
                - Country""")
    st.markdown('###')
    st.markdown(f"""
            This page illustrates some of the things that can be done, given a set
            of retail data. This is easlily changed to suit your own data and the 
            insights that you want to determine.""")

    st.markdown("## What's in the dataset?")
    st.markdown(f'The full dataset contains {df_rows:,} records.')
    st.markdown(f'Each record consists of {df_cols} columns of data.')    

    st.markdown('The following table shows the first few records from the dataset:')
    st.write(df_sales.head(8))

    ex_prepare = st.beta_expander(label='Pre-processing the data')
    with ex_prepare:
        st.markdown("## Cleaning and shaping the data")       
        st.markdown(f"""
            We need to pre-process the data to get it ready for subsequent analytics. 
            The steps taken here depend on the nature of the data and the insights
            you are trying to report.
            For this dataset, the following steps are taken:""")       
#        st.markdown('###')
        st.markdown(f"""
                    - Remove all records that do not have a CustomerID.
                    - Remove all records where the quantity is zero or less.
                    - Remove all records where the UnitPrice is zero.
                    - Remove all records where the StockCode is any of the following:
                        - M
                        - DOT
                        - BANK CHARGES
                        - D
                        - CRUK
                        - PADS
                        - POST
                        - S
                        - B
                        - C2
                        - AMAZONFEE
                    - Convert InvoiceDate to a datetime variable and separate days from hours. 
                        """)


        df_sales = df_sales[df_sales.Quantity > 0]
        df_sales = df_sales[df_sales.UnitPrice > 0]
        df_sales = df_sales[~df_sales.StockCode.isin(['M', 'DOT', 'BANK CHARGES', 'D', 'CRUK', 'S', 'PADS', 'POST', 'B', 'C2', 'AMAZONFEE'])]
        df_sales = df_sales.dropna(how='any', subset=['CustomerID'])
        rows_clean = df_sales.shape[0]
        
        st.markdown(f'After pre-processing, a total of {df_rows - rows_clean:,} records have been removed. There are now {rows_clean:,} remaining records.')   

    ex_examine = st.beta_expander(label='Reviewing the data')    
    with ex_examine:
        st.markdown("## Reviewing the clean data and its attributes")    
        records = st.slider('Select the number of records to display', 5, 1000, 50, 2)

        st.markdown('### Records from the dataset...')
        st.markdown('Clicking on a column will sort the data by that column.')
        st.write(df_sales.head(records))

        st.markdown('### Dataset column summaries')
        st.markdown(f'- There are {len(df_sales.StockCode.value_counts()):,} different products.')
        st.markdown(f'- The sales were made to {len(df_sales.CustomerID.value_counts()):,} unique customers.')
        st.markdown(f'- In total there are {len(df_sales.InvoiceNo.value_counts()):,} separate invoices.')
        st.markdown(f'- The data comes from {len(df_sales.Country.value_counts()):,} countries.')
        uk_sales = len(df_sales[df_sales.Country == 'United Kingdom'])
        st.markdown(f'- Most sales are UK based ({uk_sales:,} out of {rows_clean:,} or {uk_sales/rows_clean*100:.1f}%).')        

    ex_hours = st.beta_expander(label='Interesting insights from the data')    
    with ex_hours:
        st.markdown("## Visualising sales records") 
        
        f1, ax1 = plt.subplots(figsize = (15,8))
        sns.histplot(data=df_sales, x=df_sales['Hour'], binwidth=1, bins=24)
        ax1.set_title('Product sale times', fontsize=16)
        ax1.set(xlabel='Hour of sale', ylabel='Number of sales')
        mean = df_sales.Hour.mean()
        ax1.axvline(mean, color='r', linestyle='--')
        st.pyplot(f1)

        f2, ax2 = plt.subplots(1,2, figsize = (15,8))
        ax2[0].set_title('Quantity Sold', fontsize=16)
        ax2[1].set_title('Sales Revenue', fontsize=16)        
        c_Quantity = sns.barplot(x=df_months.index.values, y='Quantity', data=df_months, ax=ax2[0])       
        c_Price = sns.barplot(x=df_months.index.values, y='UnitPrice', data=df_months, ax=ax2[1])   
        c_Quantity.set_xticklabels(c_Quantity.get_xticklabels(), rotation=45)

        
        x_dates = df_months.index.strftime('%b %Y')
        c_Price.set_xticklabels(labels=x_dates, rotation=45, ha='right')
        c_Quantity.set_xticklabels(labels=x_dates, rotation=45, ha='right')

        st.pyplot(f2)

    