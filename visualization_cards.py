import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
import jupyter_dash
import visualization_cards

# Load Variables for cards
survey_df = pd.read_csv("https://storage.googleapis.com/hk3782/dashboard-data-latest.csv")
survey_df.columns = survey_df.columns.str.replace(' ', '_').str.lower()
covid_effct_df = survey_df.copy()
num_regions = str(covid_effct_df['region'].nunique())
pop_survey = pd.DataFrame(covid_effct_df,columns=['region','country','wave','month_year','sample_total'])
pop_survey=pop_survey.drop_duplicates()
total_sample  = int(pop_survey['sample_total'].sum())
total_sample = '{:,}'.format(total_sample)
num_countries = str(covid_effct_df['country'].nunique())
num_indicator_topics = str(covid_effct_df['indicator_topic'].nunique())

#Card Layout
def set_cardlayout():
    
    card1 = dbc.Card([
        dbc.CardBody([
            html.H1(num_regions, className="card-title",id="card_num1"),
            html.H3(" Regions ", className="card-text1",id="card_text1")
            ]
        )],
        style={'display': 'inline-block',
            'width': '100%',
            'text-align': 'center',
            'color':'white',
            'background-color': '#3098f4'},
        outline=True)
    card2 = dbc.Card([
        dbc.CardBody([
            html.H1(num_countries, className="card-title",id="card_num2"),
            html.H3(" Countries", className="card-text2",id="card_text2")
            ]
        )],
        style={'display': 'inline-block',
            'width': '100%',
            'text-align': 'center',
            'color':'white',
            'background-color': '#3098f4'},
        outline=True)
    card3 = dbc.Card([
        dbc.CardBody([
            html.H1(num_indicator_topics, className="card-title3",id="card_num3"),
            html.H3("Indicators", className="card-text3",id="card_text3")
            ]
        )],
        style={'display': 'inline-block',
            'width': '100%',
            'text-align': 'center',
            'color':'white',
            'background-color': '#3098f4'},
        outline=True)
    card4 = dbc.Card([
        dbc.CardBody([
            html.H1(total_sample, className="card-title4",id="card_num4"),
            html.H3("  Surveys  ", className="card-text4",id="card_text4")
            ]
        )],
        style={'display': 'inline-block',
            'width': '100%',
            'text-align': 'center',
            'color':'white',
            'background-color': '#3098f4'},
        outline=True)
    return(card1,card2,card3,card4)
