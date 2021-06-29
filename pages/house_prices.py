import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import statsmodels.api as sm


def build_page() -> None:
    """
    Defines a page in the streamlit application.
    :return: None
    """
    st.markdown("## Predicting house prices")

    house_data = pd.read_csv('./assets/house_data.csv')
    # drop columns that we don't need
    house_data.drop(['id', 'date', ], axis='columns', inplace=True)

    stat_describe = st.beta_expander(label='What does this demo do?')
    with stat_describe:
        st.markdown(f"""This demo loads {house_data.shape[0]} house related records 
                    from a csv file. Each record provides {house_data.shape[1]} attributes
                    relating to its house along with the value for the property.The demo 
                    uses multiple regression to predict the value of new properties.  
        """)

        st.markdown('### The first few rows from the data...')
        st.write(house_data.head(12))
        st.markdown('### Basic statistics for the data')
        st.write(house_data.describe())
        BBox = (-122.519, -121.315, 47.1559, 47.7776)
        


    stat_expand = st.beta_expander(label='Show data and statistics')
    with stat_expand:
        house_map = plt.imread('./assets/map.png')
        f5, ax = plt.subplots(figsize = (15,18))
        sns.scatterplot(house_data.long, house_data.lat, zorder=1, alpha= 0.4, s=10)
        ax.set_title('House locations')
        ax.set_xlim(-122.519, -121.315)
        ax.set_ylim(47.1559, 47.7776)
        ax.imshow(house_map, zorder=0, extent = BBox)
        st.pyplot(f5)

    pair_expand = st.beta_expander(label='Show price and attribute correlations')
    with pair_expand:
        corr = house_data.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        #cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.color_palette("YlOrBr", as_cmap=True)
        f5, ax5 = plt.subplots(figsize=(15, 9))
        sns.heatmap(corr, mask=mask, annot=True)
        st.pyplot(f5)

    stats_expand = st.beta_expander(label='Regression calculation')
    with stats_expand:
        y = house_data['price']
        x1 = house_data[['bathrooms', 'sqft_living', 'grade', 'sqft_above', 'sqft_living15']]
        x = sm.add_constant(x1)
        results = sm.OLS(y, x).fit()
        st.write(results.summary())

        f5 = plt.figure(figsize=(20,12))
        f5 = sm.graphics.plot_partregress_grid(results, fig=f5)
        st.pyplot(f5)