from os import write
import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt


@st.cache
def pre_process_data(data_frame):
    """Prepares the dataset as described on the main page.
    Args:
        The dataframe to be processed.
    Returns:
        The processed dataframe.
    """
    # Add any preprocessing that needs to be done here.
    return data_frame


@st.cache
def import_sales_data():
    """Loads and initialises the sales data from a csv file.
    Returns:
        [type]: A dataframe containing the sales data.
    """
    df_sales = pd.read_csv('./assets/transactions.csv')
    df_sales['transaction_dt'] = pd.to_datetime(df_sales['transaction_dt'])
    df_sales.set_index('transaction_dt', inplace=True)
    df_sales.index = pd.to_datetime(df_sales.index)
    return df_sales  


def show_summary_data(df):
    st.markdown('## Transaction summary')
    st.markdown(f'There are {df.shape[0]:,} records, each with {df.shape[1]} attributes.')
    st.markdown(f'The following applies to the data:')

    store_count = len(df['store'].value_counts())
    customer_count = len(df['customer'].value_counts())
    cashier_count = len(df['cashier'].value_counts())
    altered_sales = df[df['alt_price_amt_total'] > 0].shape[0]
    voids = df[df['void_qty'] != 0].shape[0]
    total = df['total_amt'].sum()
    start = df.index.min().strftime('%b %d %Y')
    end = df.index.max().strftime('%b %d %Y')

    st.markdown(f'- Number of stores {store_count}')
    st.markdown(f'- Number of customers {customer_count:,}')
    st.markdown(f'- Number of cashiers {cashier_count:,}')  
    st.markdown(f'- Number of altered sales {altered_sales:,}')    
    st.markdown(f'- Number of void records {voids:,}')    
    st.markdown(f'- The total amount transacted is £{total:,.2f} between {start} and {end}.')

def create_session_variables():
    if 'loaded' not in st.session_state:
        st.session_state.loaded = False

    if 'summary' not in st.session_state:
        st.session_state.summary = False

    if 'refunds' not in st.session_state:
        st.session_state.refunds = False    

def set_action_state(action):
    """Sets session state variables that determine 
    what the application displays.
    Args:
        action: A string representing what option was chosen by the user.
    """
    if action == 'Load data':
        st.session_state.loaded = True 
        st.session_state.summary = False        
        st.session_state.refunds = False

    if action == 'Show data summary':
        st.session_state.loaded = True 
        st.session_state.summary = True        
        st.session_state.refunds = False       

    if action == 'Process alterations':
        st.session_state.loaded = True 
        st.session_state.summary = False        
        st.session_state.refunds = True   


def build_page() -> None:
    """
    Definition for the retail sales page.
    :return: None
    """
    sns.set_style("darkgrid")
    st.markdown('A demo showing how cashier/customer transaction data can indicate potential sweethearting fraud.')
  
    df_sales = import_sales_data()
    df_altered = df_sales.groupby(by=['cashier', 'customer'], as_index=False).size()

    create_session_variables()

    st.sidebar.markdown('---')

    get_action = st.sidebar.radio('What do you want to do?',('Load data', 'Show data summary', 'Process alterations'))
    
    if st.sidebar.button('Submit'):
        set_action_state(get_action)
        
    if st.session_state.loaded:
        st.markdown(f'Successfully loaded {df_sales.shape[0]:,} transaction records.')
        record_count = st.slider('Select records to display (maximum is 5000)', 10, 5000, 10)
        st.write(df_sales.head(record_count))

    if st.session_state.summary:
        show_summary_data(df_sales)

    if st.session_state.refunds:
        st.markdown('## Repeated discounts')
        min_alt = st.slider('Select minimum repeat price alterations', 5, 16, 5, 1)
        df_plot = df_altered[df_altered['size'] >= min_alt]
        df_plot = df_plot.sort_values(by=['size'], ascending=True)

        avg_altered = df_altered['size'].mean()        


        start = df_sales.index.min().strftime('%b %d %Y')
        end = df_sales.index.max().strftime('%b %d %Y')

        cash_num = df_plot['cashier'].nunique()
        cust_num = df_plot['customer'].nunique()
        end = df_sales.index.max().strftime('%b %d %Y')
        smy = 'Showing all cashier - customer interactions where more than ' 
        smy += f'{min_alt} price alterations were made in the period from '
        smy += f'{start} to {end}. '
        smy += f'\n\nThere are {cash_num} cashiers who have processed at least {min_alt} alterations with {cust_num} customers.'
        smy += f'\n\nThe average price reductions per cashier-customer combination is {avg_altered:.2f}'
        
        col1, col2 = st.beta_columns(2)
        col1.header('Table of interactions')

        col1.write(df_plot)
        col2.header('Summary of interactions')
        col2.write(smy)

        f1, ax1 = plt.subplots(figsize = (15,6))
        p1 = sns.swarmplot(x='cashier', y='size', data=df_plot, size=20)
        ax1.set_title('Cashiers processing multiple price alterations for the same customer')
        ax1.set(xlabel='Cashiers who have altered pricing', ylabel='Number of alterations')
        p1.set_xticklabels(p1.get_xticklabels(), rotation=90)
        st.pyplot(f1)

