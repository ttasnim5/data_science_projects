# process_world_bank_data.py
import pandas as pd
import os

def process_world_bank_data(input_file='data/API_USA_DS2_en_csv_v2_3511.csv', output_file='data/cleaned_world_bank_data.csv'):
    """Cleans and processes the World Bank CSV data."""

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Resolve paths relative to the project root
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    input_file = os.path.join(project_root, input_file)
    output_file = os.path.join(project_root, output_file)

    df = pd.read_csv(input_file)
    
    # filter relevant indicators
    filter_terms = "population ages|urban population|rural population|food insecurity|PM2.5|merchandise trade|merchandise exports|commercial service exports|GDP per capita|carbon intensity"
    df = df[df['Indicator Name'].str.contains(filter_terms, case=False, na=False)]

    # melt the year columns into a single column (wide format -> long format)
    df = df.melt(
        # id_vars remain unchanged
        id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
        var_name='Year', # new column name
        value_name='WB Value' # new column holding comtents of previous year columns
    ) 
    # melt turns all the year entries into strings, while to_numeric reverses it 
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna()

    # save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

process_world_bank_data()