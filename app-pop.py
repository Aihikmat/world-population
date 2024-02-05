import pandas as pd
import streamlit as st

df = pd.read_csv('/home/hiki/Documents/Uni/Master-Curriculum/missing semester/world_data.csv')
df['Population (2023)'] = pd.to_numeric(df['Population (2023)'].str.replace(',', ''), errors='coerce')
df['Density (P/km²)'] = pd.to_numeric(df['Density (P/km²)'].str.replace(',', ''), errors='coerce')
df['Net Change'] = pd.to_numeric(df['Net Change'].str.replace(',', ''), errors='coerce')
df['Land Area (km²)'] = pd.to_numeric(df['Land Area (km²)'].str.replace(',', ''), errors='coerce')
df['Migrants'] = pd.to_numeric(df['Migrants'].str.replace(',', ''), errors='coerce')
df['Fert. Rate %'] = pd.to_numeric(df['Fert. Rate %'], errors='coerce')
df['Med. Age'] = pd.to_numeric(df['Med. Age'], errors='coerce')
# Remove '%' and convert to float for specific columns
columns_to_convert = ['Yearly Change %', 'Urban Pop %', 'World Share %']
df[columns_to_convert] = df[columns_to_convert].apply(lambda x: pd.to_numeric(x.str.rstrip('%'), errors='coerce'))

# Streamlit app
st.title('Country Information Search')

# User input for selecting a country from a dropdown with search bar
search_country = st.text_input('Search for a country:')
selected_country = st.selectbox('Select a country:', df['Country'].loc[df['Country'].str.contains(search_country, case=False)].tolist(), format_func=lambda x: x.capitalize() if x else "")

# Display information for the selected country
if selected_country:
    st.subheader(f'Information for {selected_country}')
    st.write(f'Population (2023): {df.loc[df["Country"] == selected_country, "Population (2023)"].values[0]}')
    st.write(f'Yearly Change %: {df.loc[df["Country"] == selected_country, "Yearly Change %"].values[0]}')
    st.write(f'Net Change: {df.loc[df["Country"] == selected_country, "Net Change"].values[0]}')
    st.write(f'Density (P/km²): {df.loc[df["Country"] == selected_country, "Density (P/km²)"].values[0]}')
    st.write(f'Land Area (km²): {df.loc[df["Country"] == selected_country, "Land Area (km²)"].values[0]}')
    st.write(f'Migrants: {df.loc[df["Country"] == selected_country, "Migrants"].values[0]}')
    st.write(f'Fertility Rate %: {df.loc[df["Country"] == selected_country, "Fert. Rate %"].values[0]}')
    st.write(f'Median Age: {df.loc[df["Country"] == selected_country, "Med. Age"].values[0]}')
    st.write(f'Urban Population %: {df.loc[df["Country"] == selected_country, "Urban Pop %"].values[0]}')
    st.write(f'World Share %: {df.loc[df["Country"] == selected_country, "World Share %"].values[0]}')
else:
    st.warning('No matching country found.')

st.markdown('#### Top States')

st.dataframe(df,
                column_order=("Country", "Population (2023)"),
                hide_index=True,
                width=None,
                column_config={
                "Country": st.column_config.TextColumn(
                    "Country",
                ),
                "Population (2023)": st.column_config.ProgressColumn(
                    "Population (2023)",
                    format="%f",
                    min_value=0,
                    max_value=max(df['Population (2023)']),
                    )}
                )

