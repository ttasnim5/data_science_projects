# analyze_data.py
import pandas as pd

def combine_datasets(output_file='./data/merged_data.csv'):
    # load datasets
    wb_data = pd.read_csv('data/cleaned_world_bank_data.csv')
    aq_data = pd.read_csv('data/openaq_data.csv')

    # extract year from OpenAQ data using 'period.datetimeFrom.local'
    aq_data['Year'] = pd.to_datetime(aq_data['period.datetimeFrom.local']).dt.year
    aq_data = aq_data.rename(columns={'value': 'PM10'})
    # drop columns from dataframe that are irrelevant/unhelpful
    aq_data.drop(['flagInfo.hasFlags', 'parameter.id', 
                'period.datetimeFrom.utc', 'period.datetimeFrom.local', 'period.datetimeTo.utc',
                'period.datetimeTo.local', 'summary.min', 'summary.q02', 'summary.q25', 'summary.median',
                'summary.q75', 'summary.q98', 'summary.max', 'summary.avg', 'summary.sd', 
                'coverage.expectedCount', 'coverage.expectedInterval', 'coverage.observedCount', 
                'coverage.observedInterval', 'coverage.percentComplete', 'coverage.percentCoverage', 
                'coverage.datetimeFrom.utc', 'coverage.datetimeFrom.local', 'coverage.datetimeTo.utc', 
                'coverage.datetimeTo.local', ], axis=1, inplace=True)
    # merge datasets on Year // inner join to only include years present in both datasets
    merged_data = pd.merge(wb_data, aq_data, on='Year', how='inner')

    # save the merged dataset
    merged_data.to_csv(output_file, index=False)
    print("Merged data saved to 'data/merged_data.csv'")
    return merged_data

combine_datasets()