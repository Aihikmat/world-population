# World Population Visualization

## Overview

This project visualizes world population data from 1955 to 2023, obtained from Worldometer through web scraping. Multiple scraping operations were performed due to the data being distributed across different tables on the website. Either clone this repo or use the streamlit online version to see the deployment in browser using this link https://world-population-vis.streamlit.app/

## Data Retrieval

The data was scraped in several steps to collect comprehensive information. The following visualizations were then created using the retrieved data:

## Visualizations

1. **Choropleth Map:**
    - The choropleth map provides a visual representation of world population per country.
    - It allows users to quickly identify population density and variations across different regions.

2. **Heatmap:**
    - The heatmap displays world population data per country for the selected year.
    - It offers an alternative perspective, highlighting concentration and distribution patterns.

3. **Line Chart - Total World Population Progress:**
    - The line chart illustrates the progression of total world population over the years.
    - It helps viewers understand the overall trend and growth rate.


4. **Gains and Losses**
   - countries with high inbound/ outbound migration for selected year
5. **Donat chart**
   - percentage of countries with annual inbound/ outbound migration > 50,000
6. **Tables:**
    - Several tables are included to showcase top countries in various categories for the year 2023 only:
        - Land Area (km²)
        - Fertility Rate (%)
        - Median Age
        - Urban Population (%)

## Data Sources

The data used in this project is sourced from [Worldometer](https://www.worldometers.info/), a reliable and widely-used platform for real-time global statistics.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Aihikmat/world-population-visualization.git
2. Install the requirements
   ```bash
   pip install -r requirements.txt
3. run the streamlit app str_app.py :
   ```bash
   streamlit run str_app.py

## Dependencies

- Python 3.x
- Required Python packages listed in `requirements.txt`

## Credits

- **Data Source:** Worldometer
- **Visualization Tools:** Plotly, Altair

# License

This project is licensed under the [MIT License](LICENSE).

