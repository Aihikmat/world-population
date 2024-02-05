#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="World Population Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Aihikmat',
        'About': '# This is a fancy World Population Dashboard\nCreated with Streamlit and love ❤️'
    },
)

# Custom CSS
custom_css = """
    body {
        background-image: url('https://cdn.pixabay.com/photo/2017/06/14/08/20/map-of-the-world-2401458_960_720.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #3498db;  /* Your desired text color */
    }
"""

# Set custom CSS
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

alt.themes.enable("dark")





#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
df_reshaped = pd.read_csv('world-population-reshaped.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('📈👩‍👩‍👧‍👦 Country Population Dashboard')

    year_list = list(df_reshaped['year'].unique())[::-1]

    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = df_reshaped[df_reshaped['year'] == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)


    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="country names",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year.population)),
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth





# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 5].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.Country, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)


#######################
# Dashboard Main Panel
col = st.columns((1.5, 6.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Gains/Losses')

    df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

    if selected_year > 1954:
        first_state_name = df_population_difference_sorted.Country.iloc[0]
        first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
        first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
    else:
        first_state_name = '-'
        first_state_population = '-'
        first_state_delta = ''
    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

    if selected_year > 1954:
        last_state_name = df_population_difference_sorted.Country.iloc[-1]
        last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
        last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
    else:
        last_state_name = '-'
        last_state_population = '-'
        last_state_delta = ''
    st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

    
    st.markdown('#### Countries Migration')

    if selected_year > 1954:
        # Filter states with population difference > 50000
        # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
        df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference > 50000]
        df_less_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference < -50000]
        
        # % of States with population difference > 50000
        country_migration_greater = round((len(df_greater_50000)/df_population_difference_sorted.Country.nunique())*100)
        country_migration_less = round((len(df_less_50000)/df_population_difference_sorted.Country.nunique())*100)
        donut_chart_greater = make_donut(country_migration_greater, 'Inbound Migration', 'green')
        donut_chart_less = make_donut(country_migration_less, 'Outbound Migration', 'red')
    else:
        country_migration_greater = 0
        country_migration_less = 0
        donut_chart_greater = make_donut(country_migration_greater, 'Inbound Migration', 'green')
        donut_chart_less = make_donut(country_migration_less, 'Outbound Migration', 'red')

    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write('Inbound')
        st.altair_chart(donut_chart_greater)
        st.write('Outbound')
        st.altair_chart(donut_chart_less)

with col[1]:
    st.markdown('#### Total Population')
    
    choropleth = make_choropleth(df_selected_year, 'Country', 'population', selected_color_theme)
    st.plotly_chart(choropleth, use_container_width=True)
    
    heatmap = make_heatmap(df_reshaped, 'year', 'Country', 'population', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)
    

with col[2]:
    st.markdown('#### Top Countries')

    st.dataframe(df_selected_year_sorted,
                 column_order=("Country", "population"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Country": st.column_config.TextColumn(
                        "Countries",
                    ),
                    "population": st.column_config.ProgressColumn(
                        "Population",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted.population),
                     )}
                 )


df_total = pd.read_csv('pop_year.csv')
columns_to_convert = ['Yearly Change %']
df_total[columns_to_convert] = df_total[columns_to_convert].apply(lambda x: pd.to_numeric(x.str.rstrip('%'), errors='coerce'))
# Remove '%' and convert to float for specific columns
columns_to_convert = ['World Population', 'Net Change', 'Density (P/km²)']
df_total[columns_to_convert] = df_total[columns_to_convert].apply(lambda x: pd.to_numeric(x.str.replace(',', ''), errors='coerce'))


with col[1]:
    st.markdown('#### World Population Over Time')

    # Assuming df_total is your DataFrame
    fig = px.line(df_total, x='Year', y='World Population', title='World Population Over Time',
                  labels={'World Population': 'Population', 'Year': 'Year'},
                  line_shape='linear')  # You can adjust 'line_shape' for different line styles

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='World Population',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0),
    )

    # Set the x-axis range
    fig.update_xaxes(range=[-4000, 2023])

    st.plotly_chart(fig, use_container_width=True)
    
    df = pd.read_csv('world_data.csv')
    # Sort the DataFrame by "Med. Age"
    df_sorted = df.sort_values(by='Med. Age')




    
with col[0]:
    st.markdown('#### Urban Pop % 2023 ')

    # Sort the DataFrame by 'Urban Pop %' in descending order
    df_sorted_urban_pop = df.sort_values(by='Urban Pop %', ascending=False)

    # Display only the top 10 rows
    st.dataframe(df_sorted_urban_pop[['Country', 'Urban Pop %']],
                 column_order=("Country", "Urban Pop %"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Country": st.column_config.TextColumn(
                        "Countries",
                    ),
                    "Urban Pop %": st.column_config.TextColumn(
                        "Urban Pop %",
                     )}
                 )
with col[1]:
    # Land Area (km²)
    st.markdown('#### Land Area (km²) in 2023')

    # Convert 'Land Area (km²)' to numeric and sort in descending order
    df['Land Area (km²)'] = pd.to_numeric(df['Land Area (km²)'].str.replace(',', ''), errors='coerce')
    df_sorted_land_area = df.sort_values(by='Land Area (km²)', ascending=False)

    # Add numbering to the DataFrame
    df_sorted_land_area['Rank'] = range(1, len(df_sorted_land_area) + 1)

    # Display only the top 10 rows with numbering
    st.dataframe(df_sorted_land_area[['Rank', 'Country', 'Land Area (km²)']],
                 column_order=("Rank", "Country", "Land Area (km²)"),
                 hide_index=True,
                 width=None,
                 column_config={
                     "Rank": st.column_config.TextColumn(
                         "Rank",
                     ),
                     "Country": st.column_config.TextColumn(
                         "Countries",
                     ),
                     "Land Area (km²)": st.column_config.TextColumn(
                         "Land Area (km²)",
                     )}
                 )


with col[2]:
    # Fertility Rate
    st.markdown('#### Fertility Rate 2023')

    # Sort the DataFrame by 'Fert. Rate' in descending order
    df_sorted_fertility_rate = df.sort_values(by='Fert. Rate %', ascending=False)

    # Display only the top 10 rows
    st.dataframe(df_sorted_fertility_rate[['Country', 'Fert. Rate %']],
                 column_order=("Country", "Fert. Rate %"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Country": st.column_config.TextColumn(
                        "Countries",
                    ),
                    "Fert. Rate %": st.column_config.TextColumn(
                        "Fert. Rate %",
                     )}
                 )
with col[2]:
    st.markdown('#### Median Age in 2023')

    # Display the rest of the rows when scrolling down
    #with st.expander('Show All Median Age', expanded=False):
        #st.table(df_sorted[['Country', 'Med. Age']])


    st.dataframe(df_sorted[['Country', 'Med. Age']],
                 column_order=("Country", "Med. Age"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Country": st.column_config.TextColumn(
                        "Countries",
                    ),
                    "Med. Age": st.column_config.TextColumn(
                        "Med. Age",
                     )}
                 )
    



    with st.expander('About', expanded=True):
        st.write('''
            - Data: [Worldometer - real time world statistics](https://www.worldometers.info/population/).
            - :orange[**Gains/Losses**]: countries with high inbound/ outbound migration for selected year
            - :orange[**Countries Migration**]: percentage of countries with annual inbound/ outbound migration > 50,000
            ''')

    








