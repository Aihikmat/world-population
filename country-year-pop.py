import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
'''
# List of countries
countries = [
    'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra',
    'Angola', 'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia',
    'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
    'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
    'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
    'Brazil', 'British Virgin Islands', 'Brunei-darussalam', 'Bulgaria', 'Burkina Faso',
    'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada',
    'Caribbean Netherlands', 'Cayman Islands', 'Central African Republic',
    'Chad', 'Chile', 'China', 'Colombia', 'Comoros',
    'Congo', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Curacao',
    'Cyprus', 'Czechia', 'cote-d-ivoire', 'Denmark', 'Djibouti', 'Dominica',
    'Dominican Republic', 'Democratic-Republic-of-the-Congo', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Faeroe Islands',
    'Falkland-Islands-malvinas', 'Fiji', 'Finland', 'France', 'French Guiana',
    'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana',
    'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam',
    'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See',
    'Honduras', 'China-Hong-Kong-Sar', 'Hungary', 'Iceland', 'India', 'Indonesia',
    'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica',
    'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait',
    'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
    'Liechtenstein', 'Lithuania', 'Luxembourg', 'China-Macao-Sar', 'Madagascar', 'Malawi',
    'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
    'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova',
    'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique',
    'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia',
    'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North Korea',
    'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
    'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland',
    'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Reunion',
    'Saint-Barthelemy', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia',
    'Saint Martin', 'Saint Pierre and Miquelon', 'Samoa', 'San Marino',
    'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
    'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia',
    'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea',
    'South Sudan', 'Spain', 'Sri Lanka', 'Saint-Vincent-and-the-Grenadines',
    'State of Palestine', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland',
    'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'North Macedonia', 'Thailand',
    'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia',
    'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'UK',
    'Uganda', 'Ukraine', 'United Arab Emirates', 'us',
    'United States Virgin Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela',
    'Vietnam', 'Wallis-and-Futuna-Islands', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe'
]



# Base URL for Worldometer country pages
base_url = 'https://www.worldometers.info/world-population/'


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
# Folder to store CSV files
output_folder = 'missing semester/country_population_data'
create_folder(output_folder)

# Iterate through each country
for country in countries:
    # Construct the URL for the specific country
    country_url = base_url + country.lower().replace(' ', '-') + '-population/'
    
    # Send a GET request to the URL
    response = requests.get(country_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with population data
        table = soup.find('table', {'class': 'table table-striped table-bordered table-hover table-condensed table-list'})
        
        if table:
            # Extract data from the table
            rows = table.find_all('tr')[1:]  # Skip the header row

            # Create a DataFrame for the country's population data
            country_data = []

            for row in rows:
                columns = row.find_all('td')
                year = columns[0].text.strip()
                population = columns[1].text.strip()

                country_data.append({'Year': year, 'Population': population})

            # Create a DataFrame and save it to a CSV file
            df = pd.DataFrame(country_data)
            output_file_path = os.path.join(output_folder, f'{country}_population_data.csv')
            df.to_csv(output_file_path, index=False)

            print(f'{country} data saved to {output_file_path}')
        else:
            print(f'No data found for {country}')
    else:
        print(f'Failed to retrieve data for {country}')


# Folder containing individual CSV files
input_folder = 'missing semester/country_population_data'

# List to store DataFrames for each country
dfs = []

# Iterate through each file in the folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Add a new column for the country name
        country_name = filename.replace('_population_data.csv', '')
        df['Country'] = country_name
        
        # Append the DataFrame to the list
        dfs.append(df)

# Merge DataFrames based on 'Year' and 'Population'
merged_df = pd.concat(dfs, ignore_index=True)

# Pivot the DataFrame to have years as columns
pivot_df = merged_df.pivot(index='Country', columns='Year', values='Population')

# Save the pivoted DataFrame to a new CSV file
output_file_path = 'pivoted_population_data.csv'
pivot_df.to_csv(output_file_path)

print(f'Pivoted data saved to {output_file_path}')

# Load the pivoted DataFrame from the CSV file
input_file_path = 'pivoted_population_data.csv'
pivoted_df = pd.read_csv(input_file_path, header=[0, 1], index_col=0)

# List of years to keep
years_to_keep = [
    '2024', '2023', '2022', '2020', '2015',
    '2010', '2005', '2000', '1995', '1990',
    '1985', '1980', '1975', '1970', '1965',
    '1960', '1955'
]

# Filter columns to keep only specified years
filtered_df = pivoted_df[years_to_keep]

# Save the filtered DataFrame to a new CSV file
output_file_path = 'filtered_population_data.csv'
filtered_df.to_csv(output_file_path)

print(f'Filtered data saved to {output_file_path}')

# Load the filtered DataFrame from the CSV file
input_file_path = 'filtered_population_data.csv'
filtered_df = pd.read_csv(input_file_path, header=0, index_col=0)

# List of years to convert
years_to_convert = [
    '2024', '2023', '2022', '2020', '2015',
    '2010', '2005', '2000', '1995', '1990',
    '1985', '1980', '1975', '1970', '1965',
    '1960', '1955'
]

# Convert population values in specified years to numeric, remove commas
filtered_df[years_to_convert] = filtered_df[years_to_convert].apply(
    lambda col: pd.to_numeric(col.str.replace(',', ''), errors='coerce')
)

# Save the converted DataFrame to a new CSV file
output_file_path = 'numerical_population_data.csv'
filtered_df.to_csv(output_file_path)

print(f'Converted data saved to {output_file_path}')

df = pd.read_csv('numerical_population_data.csv')

countries_abbreviation = {
    "Afghanistan": "AF",
    "Albania": "AL",
    "Algeria": "DZ",
    "American Samoa": "AS",
    "Andorra": "AD",
    "Angola": "AO",
    "Anguilla": "AI",
    "Antigua and Barbuda": "AG",
    "Argentina": "AR",
    "Armenia": "AM",
    "Aruba": "AW",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahamas": "BS",
    "Bahrain": "BH",
    "Bangladesh": "BD",
    "Barbados": "BB",
    "Belarus": "BY",
    "Belgium": "BE",
    "Belize": "BZ",
    "Benin": "BJ",
    "Bermuda": "BM",
    "Bhutan": "BT",
    "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Brazil": "BR",
    "British Virgin Islands": "VG",
    "Brunei-darussalam": "BN",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burundi": "BI",
    "Cabo Verde": "CV",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Caribbean Netherlands": "BQ",
    "Cayman Islands": "KY",
    "Central African Republic": "CF",
    "Chad": "TD",
    "Chile": "CL",
    "China": "CN",
    "Colombia": "CO",
    "Comoros": "KM",
    "Congo": "CG",
    "Cook Islands": "CK",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cuba": "CU",
    "Curacao": "CW",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "cote-d-ivoire": "CI",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Democratic-Republic-of-the-Congo": "CD",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Eritrea": "ER",
    "Estonia": "EE",
    "Ethiopia": "ET",
    "Faeroe Islands": "FO",
    "Falkland-Islands-malvinas": "FK",
    "Fiji": "FJ",
    "Finland": "FI",
    "France": "FR",
    "French Guiana": "GF",
    "French Polynesia": "PF",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Gibraltar": "GI",
    "Greece": "GR",
    "Greenland": "GL",
    "Grenada": "GD",
    "Guadeloupe": "GP",
    "Guam": "GU",
    "Guatemala": "GT",
    "Guinea": "GN",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Haiti": "HT",
    "Holy See": "VA",
    "Honduras": "HN",
    "China-Hong-Kong-Sar": "HK",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Isle of Man": "IM",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kiribati": "KI",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Laos": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "China-Macao-Sar": "MO",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Marshall Islands": "MH",
    "Martinique": "MQ",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Mayotte": "YT",
    "Mexico": "MX",
    "Micronesia": "FM",
    "Moldova": "MD",
    "Monaco": "MC",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Montserrat": "MS",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Myanmar": "MM",
    "Namibia": "NA",
    "Nauru": "NR",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Caledonia": "NC",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Niger": "NE",
    "Nigeria": "NG",
    "Niue": "NU",
    "North Korea": "KP",
    "Northern Mariana Islands": "MP",
    "Norway": "NO",
    "Oman": "OM",
    "Pakistan": "PK",
    "Palau": "PW",
    "Panama": "PA",
    "Papua New Guinea": "PG",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Puerto Rico": "PR",
    "Qatar": "QA",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "Reunion": "RE",
    "Saint-Barthelemy": "BL",
    "Saint Helena": "SH",
    "Saint Kitts and Nevis": "KN",
    "Saint Lucia": "LC",
    "Saint Martin": "MF",
    "Saint Pierre and Miquelon": "PM",
    "Samoa": "WS",
    "San Marino": "SM",
    "Sao Tome and Principe": "ST",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Sierra Leone": "SL",
    "Singapore": "SG",
    "Sint Maarten": "SX",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Solomon Islands": "SB",
    "Somalia": "SO",
    "South Africa": "ZA",
    "South Korea": "KR",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Saint-Vincent-and-the-Grenadines": "VC",
    "State of Palestine": "PS",
    "Sudan": "SD",
    "Suriname": "SR",
    "Swaziland": "SZ",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syria": "SY",
    "Taiwan": "TW",
    "Tajikistan": "TJ",
    "Tanzania": "TZ",
    "North Macedonia": "MK",
    "Thailand": "TH",
    "Timor-Leste": "TL",
    "Togo": "TG",
    "Tokelau": "TK",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkey": "TR",
    "Turkmenistan": "TM",
    "Turks and Caicos Islands": "TC",
    "Tuvalu": "TV",
    "UK": "GB",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "us": "US",
    "United States Virgin Islands": "VI",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Vanuatu": "VU",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Wallis-and-Futuna-Islands": "WF",
    "Western Sahara": "EH",
    "Yemen": "YE",
    "Zambia": "ZM",
    "Zimbabwe": "ZW"
}


df['country_code'] = [countries_abbreviation[x] for x in df["Country"]]

new_columns = ['Country', 'country_code', '2024', '2023', '2022', '2020', '2015', '2010', '2005',
       '2000', '1995', '1990', '1985', '1980', '1975', '1970', '1965', '1960',
       '1955'] 
df = df.reindex(columns=new_columns)
#new_columns = ['states', 'states_code', 'id', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
 #      '2017', '2018', '2019']
#df = df.reindex(columns=new_columns)
print(df.head())
# Save data to CSV
df.to_csv('world-population-states-code.csv', index=False)

df = pd.read_csv('world-population-states-code.csv')

# Reshape the DataFrame
df_reshaped = pd.melt(df, id_vars=['Country', 'country_code'], var_name='year', value_name='population')

# Convert 'year' column values to integers
df_reshaped['Country'] = df_reshaped['Country'].astype(str)
df_reshaped['year'] = df_reshaped['year'].astype(int)
df_reshaped['population'] = pd.to_numeric(df_reshaped['population'], errors='coerce')
df_reshaped['id'] = df_reshaped['Country'].astype('category').cat.codes + 1


df_reshaped.to_csv('world-population-reshaped.csv')

df = pd.read_csv('missing semester/world-population-reshaped.csv')

# Update country code for Namibia
df.loc[df['Country'] == 'Namibia', 'country_code'] = 'NA'

namibia_entries = df[df['Country'] == 'Namibia']
#print(namibia_entries)

df.to_csv('world-population-reshaped.csv')'''


'''df = pd.read_csv('missing semester/world-population-reshaped.csv')

# Delete entries for the year 2024
df = df[df['year'] != 2024]

# Display the updated DataFrame
print("\nDataFrame after deleting entries for the year 2024:")
print(df)

# Save the remaining DataFrame to a CSV filev
df.to_csv('world-population-reshaped.csv', index=False)'''


#df = pd.read_csv('missing semester/world-population-reshaped.csv', na_values=['nan'])
# Convert 'country_code' to string data type
#df['country_code'] = df['country_code'].astype(str)

# Display the DataFrame after conversion
#print("\nDataFrame after converting 'country_code' to string:")
#print(df.loc[df['Country']== 'Namibia'])
#df.to_csv('world-population-reshaped.csv', index=False)
#df = pd.read_csv('missing semester/world-population-reshaped.csv')
#print(df.loc[df['Country']== 'Namibia'])



