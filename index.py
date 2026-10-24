# Day 20

import streamlit as st
import pandas as pd



uploaded_file = st.file_uploader("Upload a CSV file", type="csv")


page = st.sidebar.selectbox('Select your page', ['Home', 'Data Analysis', 'Visualization'], index=0)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if page == 'Home':
        st.title('Welcome to the Home Page')
        st.write('This is the home page of the Streamlit app.')

    elif page == 'Data Analysis':

        st.write('Select the analysis you want to perform:')

        description = st.checkbox('Description Analysis')
        missing_values = st.checkbox('Missing Values Analysis')

        description_table = df.describe()
        missing_values_table = df.isna().sum()

        st.subheader('DataFrame')
        st.write(df.head(5))

        st.header('Output')

        if description:
            st.subheader('Descriptive Statistics')
            st.write(description_table)

        if missing_values:
            st.subheader('Missing Values Analysis')
            st.write(missing_values_table)

    else:
            st.subheader("Data preview")
            st.dataframe(df.head())

            numeric_cols = df.select_dtypes(include="number").columns.tolist()

            if not numeric_cols:
                st.warning("This file has no numeric columns to plot on the Y axis.")
            else:
                col1, col2, col3 = st.columns(3)
                x_col = col1.selectbox("X axis (categories)", df.columns, index=None)
                y_col = col2.selectbox("Y axis (numbers)", numeric_cols,index=None)
                agg = col3.selectbox("If X repeats, combine with", ["sum", "mean", "count"])

                # Combine rows that share the same X value
                if x_col and y_col is not None:
                    if x_col == y_col:
                        st.warning("X and Y columns cannot be the same. Please select different columns.")
                    else:
                        chart_data = df.groupby(x_col)[y_col].agg(agg).reset_index()

                        st.subheader(f"{agg.capitalize()} of {y_col} by {x_col}")
                        st.bar_chart(chart_data, x=x_col, y=y_col)
                else:
                    st.warning("Please select both X and Y columns to generate the chart.")

                
else:
    st.info("☝️ Upload a CSV file to get started")