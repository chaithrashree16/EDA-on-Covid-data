import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def cleanData(): #This is the user-defined function that will be called into the main.py file

        # Load csv
        survey_df = pd.read_csv("https://storage.googleapis.com/hk3782/dashboard-data-latest.csv")
        
        # update column names to lowercase as per standard
        survey_df.columns = survey_df.columns.str.replace(' ', '_').str.lower()


        # drop unused columns
        survey_df.drop(['row_id','survey_link','last_updated','survey_producer','footnote','fcs'], axis=1, inplace=True)

        # replace null values
        survey_df['lending_category'] = survey_df['lending_category'].replace('..','is_null')
        survey_df['urban_rural'].fillna('Not reported', inplace = True)

        # remove null values
        survey_df.dropna(axis = 0, how = 'any',subset = ['month','sample_total'],inplace = True)

        # sort columns
        survey_df.sort_values(['year','month'], inplace = True, ascending = True)

        # type casts
        survey_df.month = survey_df['month'].astype(int)


        # Combining month and year to get date format.I am giving day = 1 and assuming the same for all the columns for analysis purpose.
        survey_df['month_year'] = pd.to_datetime(survey_df[['year', 'month']].assign(DAY=1))

        #Below query returns the countries which participated multiple times in survey and their
        #corresponding wave, income group, sample total for each wave and count of sub category of indicators surveyed for them

        many_wave_df = survey_df.query('urban_rural == "National" & industry == "All" & many_waves == 1').groupby(
                ['country', 'wave', 'income_group', 'sample_total'])['country'].count()
        many_wave_df

        #Segmentation

        segments = [-1, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, np.inf]
        labels = ['0%', '1% - 10%', '11% to 20%', '21% to 30%', '31% - 40%', '41% to 50%', '51% - 60%', '61% - 70%',
                  '71% - 80%', '81% - 90%', '>90%']
        response_group = pd.cut(survey_df.indicator_val, segments, labels=labels)
        survey_df['response_group'] = response_group
        survey_df[['country', 'wave', 'income_group', 'sample_total', 'indicator_topic', 'indicator_val',
                   'response_group']]


        return survey_df

