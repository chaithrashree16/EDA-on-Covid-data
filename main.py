import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import jupyter_dash
from wordcloud import WordCloud, STOPWORDS 
import base64
from io import BytesIO
from pandas._libs.tslibs.period import period_asfreq_arr
import visualization_cards
import data_clean_module 
app = jupyter_dash.JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
# survey_df = pd.read_csv("https://storage.googleapis.com/hk3782/dashboard-data-latest.csv")
# survey_df.columns = survey_df.columns.str.replace(' ', '_').str.lower()
# survey_df['month_year'] = pd.to_datetime(survey_df[['year', 'month']].assign(DAY=1))

# Call the module/user defined function to clean the data
survey_df = data_clean_module.cleanData()

df_all_industry = survey_df[survey_df.industry =='All']

"""# Card layout"""
card1,card2,card3, card4 = visualization_cards.set_cardlayout()

"""# Dynamic Bar chart for Number of people surveyed"""

df = survey_df.copy()
df = df[(df.urban_rural == 'National') & (df.industry == 'All')]
df = df.groupby(['region_code','wave','indicator_topic'])[['sample_subset']].sum()
df.reset_index(inplace=True)
df = df.sort_values('indicator_topic')


"""# Scatter plot"""

covid_FS = survey_df[(survey_df.indicator_topic== 'Food Security')& (survey_df.indicator == 'FS_day')  & (survey_df.urban_rural == 'National') & (survey_df.industry == 'All')]
df2 = pd.DataFrame(covid_FS,columns=['region','country','wave','month_year','gdp_pc','sample_total','indicator_val'])
df2=df2.drop_duplicates()
df2=df2.sort_values('month_year')

df2['gdp_pc'] = df2['gdp_pc'].fillna(0)
df2.head
fig3 = px.scatter(df2, x="gdp_pc", y="sample_total",animation_frame="wave",animation_group="country",
                 size="indicator_val",color="wave", hover_name="country",
                  log_x=True, 
                  size_max=55, range_x=[800,30000], range_y=[-10,9000],
                  labels= {'sample_total': 'Total number of people surveyed','gdp_pc':'Per Capita Income'})
                #  log_x=True, size_max=60)
fig3.update_layout(title={
    'text': "<b>Food Security Survey response Vs per capita income </b>",  'x': 0.45,
    'y': 0.95,
    'xanchor': 'center',
    'yanchor': 'top'
    })
fig3.update_layout(showlegend=False)
#fig3.show()


"""# Word cloud"""

df1 = survey_df.copy()
words = df1.indicator_topic.unique()
plt.subplots(figsize = (8,8))
wordcloud = WordCloud (
                    background_color = 'white',
                    width = 552,
                    height = 364
                        ).generate(' '.join(words))
wc_img1 = wordcloud.to_image()
with BytesIO() as buffer:
    wc_img1.save(buffer, 'png')
    img1 = base64.b64encode(buffer.getvalue()).decode()
fig20 = plt.imshow(wordcloud) # image show
plt.axis('off') # to off the axis of x and y
#plt.show()

words1 = df1.country.unique()
plt.subplots(figsize = (8,8))
wordcloud = WordCloud (
                    background_color = 'white',
                    width = 552,
                    height = 364
                        ).generate(' '.join(words1))
wc_img2 = wordcloud.to_image()
with BytesIO() as buffer:
    wc_img2.save(buffer, 'png')
    img2 = base64.b64encode(buffer.getvalue()).decode()
fig21 = plt.imshow(wordcloud) # image show
plt.axis('off') # to off the axis of x and y
#plt.show()

words2 = df1.region.unique()
plt.subplots(figsize = (8,8))
wordcloud = WordCloud (
                    background_color = 'white',
                    width = 552,
                    height = 364
                        ).generate(' '.join(words2))
wc_img3 = wordcloud.to_image()
with BytesIO() as buffer:
    wc_img3.save(buffer, 'png')
    img3 = base64.b64encode(buffer.getvalue()).decode()
fig22 = plt.imshow(wordcloud) # image show
plt.axis('off') # to off the axis of x and y


#pie chart

df3d = survey_df[(survey_df.industry== 'All')& (survey_df.indicator == 'Demo_hsize') & (survey_df.urban_rural == 'National')]
df3d = df3d[(survey_df.urban_rural == 'National') & (survey_df.industry == 'All')]
df3d= df3d.drop_duplicates()
dfd = df3d.groupby(['country','income_group'])['sample_total'].count()

pie = px.pie(df3d, values='sample_total', names='region',
             title='samples collected against various regions based on their income groups',
             hover_data=['income_group'], labels={'samples':'samples_collected'})

pie.update_layout(title={
    'text': "<b>Region wise Survey Statistics</b>",
    'x': 0.5,
    'y': 0.98,
    'xanchor': 'center',
    'yanchor': 'top'
    })
pie.update_layout(margin=dict(t=30, b=5, l=0, r=0))
pie.update_layout(showlegend=False)
pie.update_traces(textposition='inside', textinfo='percent+label' )


"""# Layout

**Side Bar Layout**
"""

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H6("DASHBOARD", className="display-6"),
        # html.H4("MENU", className="display-4"),
        html.Hr(),
        html.P(
            "Analysis Menu", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Survey Analysis", href="/", active="exact"),
                dbc.NavLink("Food Security Analysis", href="/page-1", active="exact"),
                dbc.NavLink("GDP Per Capita Analysis", href="/page-2", active="exact"),
                dbc.NavLink("Conclusion", href="/conclusion", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

"""**Card Layout**"""

card1, card2, card3, card4 = visualization_cards.set_cardlayout()

"""**Page** **layout**"""



@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                  html.Div(children=[

    html.H1('',
            style={'text-align': 'center', 'font-style': 'cursive'}),
    dbc.Row([
        dbc.Col(html.H1(html.B("COVID-19 impact survey data analysis"), style={'text-align': 'center','color': '#3098f4'}
                        )
        )
    ]),
  html.Br(),
#****************************
#Card layout
#**************************** 
  html.Hr(),
  html.Br(),
  dbc.Row(
            [
            dbc.Col(card1,  width=9, lg=3),
            dbc.Col(card2,  width=7, lg=3),
            dbc.Col(card3,  width=7, lg=3),
            dbc.Col(card4,  width=6, lg=3),
            ],
            
            justify="center",
  ),
    html.Hr(),

#****************************
#World map layout
#****************************

    html.Div([
      html.H2('World map highlighting countries surveyed', style={'text-align': 'center'}),
              html.Br(),
              html.Div(children='''
                 Below graph shows the countries which participated in Covid-19 impact survey. We are able to observe the survey volume for each country the country's income group for the selected survey wave.
              '''),

              html.Br(),
              html.Br(),
   
     html.Div(children=[

        html.Div([
            # html.H2('World map highlighting countries surveyed', style={'text-align': 'center'}),
            # html.Br(),
            # html.Div(children='''
            #      Below graph shows the countries which participated in Covid-19 impact survey. We are able to observe the survey volume for each country the country's income group for the selected survey wave.
            #   ''', style={'text-align': 'left'}),

            html.Br(),
            html.Br(),
        html.Div(children=[


                html.Label(['Choose Survey WAVE:']),

                dcc.Dropdown(id="wave",
                             options=[
                                 {"label": "WAVE1", "value": "WAVE1"},
                                 {"label": "WAVE2", "value": "WAVE2"},
                                 {"label": "WAVE3", "value": "WAVE3"},
                                 {"label": "WAVE4", "value": "WAVE4"},
                                 {"label": "WAVE5", "value": "WAVE5"},
                                 {"label": "WAVE6", "value": "WAVE6"},
                                 {"label": "WAVE7", "value": "WAVE7"},
                                 {"label": "WAVE8", "value": "WAVE8"},
                                 {"label": "WAVE9", "value": "WAVE9"},
                                 {"label": "WAVE10", "value": "WAVE10"},
                                 {"label": "WAVE11", "value": "WAVE11"},
                                 {"label": "WAVE12", "value": "WAVE12"},
                                 {"label": "WAVE13", "value": "WAVE13"},
                                 {"label": "WAVE14", "value": "WAVE14"},
                                 {"label": "WAVE15", "value": "WAVE15"},
                                 {"label": "WAVE16", "value": "WAVE16"},
                                 {"label": "WAVE17", "value": "WAVE17"}
                             ],

                             multi=False,
                             value="WAVE1",
                             clearable=False,

                             ),

            ], style={'display': 'flex', 'flex-direction': 'column'}),

            html.Br(),


            dcc.Graph(
                id='worldmapfig1',
                figure={}
            ),
        ], style={'width': '90%'}),
   ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around',"border":"2px black solid"}),
 html.Hr(),
 html.Br(),

# word cloud and pie graph

dbc.Row(
    
   
            [
            dbc.Col(children=[

#***************
# Word cloud
#***************
        html.Div([
              html.H2('Word Cloud Visualization', style={'text-align': 'center'}),
              html.Br(),
              html.Div(children='''
                Below plot shows different word cloud in each tab. The various indicators surveyed, countries and regions surveyed are depicted in each tab.
              '''),

              html.Br(),
              html.Br(),
              html.Br(),
        dcc.Tabs([

        # First tab
        dcc.Tab(label='Indicators Surveyed' ,children=[

            # First graph
            html.Img(src="data:image/png;base64," + img1,style={
                    "border":"2px black solid",
                    # 'display': 'inline-block',
                    'vertical-align': 'bottom',
                    'width': 'auto',
                     "align-items": "center",'margin' : '0px 30px 0px 0px'
                        })],style={'width': '33%'}),
               
            dcc.Tab(label='Countries Surveyed', children=[
                        # Second graph
                        html.Img(src="data:image/png;base64," + img2,style={
                                "border":"2px black solid",
                                'width': 'auto', 
                                'display': 'flex', 
                                'align-items': 'center',
                                 'justify-content': 'center',
                                 "align":"center",
                                 'margin' : '0px 30px 0px 0px'}
                              #  'display': 'inline-block',
                              #   'align-items': 'center', 'justify-content': 'center',
                              #  'width': '30%',
                                    # }
                                )],style={'width': '33%'}),

            # Third graph
            dcc.Tab(label='Continents Surveyed', children=[
                        html.Img(src="data:image/png;base64," + img3,style={
                                "border":"2px black solid",
                                'width': 'auto', 
                                'display': 'flex', 
                                'align-items': 'center',
                                 'justify-content': 'center',
                                 "align":"center",
                                 'margin' : '0px 30px 0px 0px'}
                              #  'display': 'inline-block',
                              #   'align-items': 'center', 'justify-content': 'center',
                              #  'width': '30%',
                                    # }
                                )],style={'width': '33%'}),
            
            ], style={'width': 'auto',"align-items": "center", "justify-content": "center",'margin' : '0px 30px 12px 5px'})

        ])
        ], style={'width': '45%'}),

           
#
#**********Pie chart******
    html.Div([
      html.H2('Regionwise Split', style={'text-align': 'center'}),
              html.Br(),
              html.Div(children='''
                This Pie chart shows the number of surveys done in each region. We can see that Sub-Saharan Africa is the most surveyed region. 


              '''),

              html.Br(),
              html.Br(),
      dbc.Col( html.Div(children=[
                    dcc.Graph(
                        id='pie chart',
                        figure=pie
                        )], style={"border":"2px black solid",'width': 'auto','height': '400',"align-items": "center", "justify-content": "center",'margin' : '0px 0px 0px 5px'})
              )
       ], style={'width': '45%'}),
           ]),    
      ]),
      html.Hr(),
 #]),
        ])]
    elif pathname == "/page-1":
        return [
#********Barchart***********
html.Br(),

  html.H2('Survey Topic Statistics'),
html.Br(),

              html.Div(children='''
                This visualization shows the number of surveys done in each indicator topic, for selected region and wave.
                We can observe that Demographics and Food security are the highly surveyed topics in all regions.
                With a focus on Sub-Saharan Africa region, which had the largest percentage of surveys, we can clearly observe the food security survey concentration, 
                which leads us to analyze this indicator further to observe the trends
              
              '''),
               html.Br(),
html.Br(),
    html.Div(children=[


   
  #  html.H1("Survey Topic Statistics", style={'text-align': 'center'}),


  html.Div(children=[

			html.Div(children=[
							   
					  html.Label(['Choose Survey Region:']),
    dcc.Dropdown(id="slct_region",
                 options=[
                     {"label": "East Asia and Pacific", "value": "EAP"},
                     {"label": "Sub Saharan Africa", "value": "SSA"},
                     {"label": "Middle East & North Africa", "value": "MNA"},
                     {"label": "Latin America & Caribbean", "value": "LAC"},
                     {"label": "Europe & Central Asia", "value": "ECA"}
                     ],
                 multi=False,
                 value="EAP",
                 clearable=False,
                 ),

			   ], style={'display': 'flex', 'flex-direction': 'column',"width": "50%"}),
				
				html.Br(),

				html.Div(children=[

					html.Label(['Choose Survey WAVE:']),
    dcc.Dropdown(id="slct_wave",
                 options=[
                                 {"label": "WAVE1", "value": "WAVE1"},
                                 {"label": "WAVE2", "value": "WAVE2"},
                                 {"label": "WAVE3", "value": "WAVE3"},
                                 {"label": "WAVE4", "value": "WAVE4"},
                                 {"label": "WAVE5", "value": "WAVE5"},
                                 {"label": "WAVE6", "value": "WAVE6"},
                                 {"label": "WAVE7", "value": "WAVE7"},
                                 {"label": "WAVE8", "value": "WAVE8"},
                                 {"label": "WAVE9", "value": "WAVE9"},
                                 {"label": "WAVE10", "value": "WAVE10"},
                                 {"label": "WAVE11", "value": "WAVE11"},
                                 {"label": "WAVE12", "value": "WAVE12"},
                                 {"label": "WAVE13", "value": "WAVE13"},
                                 {"label": "WAVE14", "value": "WAVE14"},
                                 {"label": "WAVE15", "value": "WAVE15"},
                                 {"label": "WAVE16", "value": "WAVE16"},
                                 {"label": "WAVE17", "value": "WAVE17"}
                             ],
                 multi=False,
                 value="WAVE1",
                 clearable=False,
                 ),

					  ],  style={'display': 'flex', 'flex-direction': 'column',"width": "50%"}),


		], style={'display': 'flex', 
				  'flex-direction': 'row',
				  'justify-content': 'flex-start', 
				  'gap': '10px'}),

   
    

    dcc.Graph(id='survey_size_map', figure={}),

   ], style={'width': '94%', 'padding': '4% 2% 0% 2%', 'margin-left': '1%',"border":"2px black solid"}),
        
        html.Br(),
        html.Br(),
        html.Br(),
        html.Hr(),

#*************
#Sunburst
#*************
html.H2('Food Security Survey Response Analysis'),
html.Br(),
              html.Div(children='''
                Below  sunburst visualization shows the FS survey response stats for countries which participated in more than one survey wave.
                The intent of this visualization is to find if food security related issues got better over the period of time.
                Analysis shows that the situations has got better overtime, across the regions.
                We observed the same trend when we looked at our focus region of Sub Saharan Africa especially for the indicator on staying without food for whole day.
                
                
              '''),
html.Br(),
html.Br(),
html.Div([  
                        
                        
		# html.H2("Food Security Survey Response Analysis", style={'text-align': 'Center'}),

		html.Div(children='''
		'''),

		html.Br(),

		html.Div(children=[

			html.Div(children=[
							   
					  html.Label(['Choose Survey Region:']),

					  dcc.Dropdown(id="region_list",
							  options=[
								  # {"label": "South Asia", "value": "South Asia"},
								  {"label": "Latin America & Caribbean", "value": "Latin America & Caribbean"},
								  {"label": "East Asia & Pacific", "value": "East Asia & Pacific"},
								  {"label": "Europe & Central Asia", "value": "Europe & Central Asia"},
								  {"label": "Middle East & North Africa", "value": "Middle East & North Africa"},
								  {"label": "Sub-Saharan Africa", "value": "Sub-Saharan Africa"}
							  ],

							  multi=False,
							  value="East Asia & Pacific",
							  clearable=False,
	  
					  ),

			   ], style={'display': 'flex', 'flex-direction': 'column',"width": "50%"}),
				
				html.Br(),

				html.Div(children=[

					html.Label(['Choose Food Security indicator:']),

					dcc.Dropdown(id="food_sub",
						  options=[
							  {"label": "Able to access any staple food in the past 7 days -all staple food items ", "value":"Prev_AS_other"},
                {"label": "Able to access any staple food in the past 7 days - first 3 staple food items", "value":"Prev_AnyStaple"},
                {"label": "Able to access staple food item 1 in the past 7 days when needed ", "value":"Prev_Sfood1"},
                {"label": "Able to access staple food item 2 in the past 7 days when needed", "value":"Prev_Sfood2"},
                {"label": "Able to access staple food item 3 in the past 7 days when needed", "value":"Prev_Sfood3"},
                {"label": "Able to access any other staple food in the past 7 days ", "value":"Prev_Sfood_other"},
                {"label": "In the last 30 days, went without eating for a whole day due to lack of money ", "value":"FS_day"},
                {"label": "In the last 30 days, were hungry but did not eat due to lack of money ", "value":"FS_hungry"},
                {"label": "In the last 30 days, you ran out of food due to a lack of money or other resources? ", "value":"FS_ranout"},
                {"label": "In the last 30 days, you skipped a meal due to lack of money or other resources", "value":"FS_skipmeal"},
                {"label": "In the last 30 days, was anyone unable to eat healthy/nutritious or preferred food due to lack of resources", "value":"FS_unable"},
                {"label": "In the last 30 days, ate only a few kinds of foods due to lack of money", "value":"FS_atefew"},
                {"label": "In the last 30 days, ate less than they thought they should due to lack of money", "value":"FS_ateless"},
                {"label": "In the last 30 days, you worried about running out of food due to a lack of money or other resources", "value":"FS_worried"}
							  ],
							  
							  multi=False,
							  value="FS_day",
							  clearable = False,
						 ),  

					  ],  style={'display': 'flex', 'flex-direction': 'column',"width": "70%"}),


		], style={'display': 'flex', 
				  'flex-direction': 'row',
				  'justify-content': 'flex-start', 
				  'gap': '10px'}),
		

		html.Br(),

		dcc.Graph(id='sunburst', figure={}),
     
    ], style={'width': '94%', 'padding': '4% 2% 0% 2%', 'margin-left': '1%',"border":"2px black solid"}),



   html.Br(),
   html.Hr(),
   html.Br(),

    ]
    elif pathname == "/page-2":
        return [
                   html.Br(),

#***************
# Scatter plot
#***************
        html.H2('Correlation of Per Capita income & Food Security '),

   html.Br(),
              html.Div(children='''
                Below visualization shows scatter plot of food security survey response (question on went without food for one day), against corresponding countries per capita income.  
              We can observe that high income countries had lower food security issues(depicted by the size of the bubble) and were also surveyed less.
              We can also observe that the severity of food security issues has declined over the waves, 
              which indicate that people and government are better prepared and are able to handle the pandemic situation.
                


              '''),
                 html.Br(),
         html.Br(),
        html.Div(children=[
                    dcc.Graph(
        id='scatter plot',
        figure=fig3
    )
                ], style={"border":"2px black solid"}) ,
                

        html.Br(),
        html.Br(),
        html.Hr(),
        html.Br(),

# ]
# , style={'backgroundColor': 'white'}
# )
      ]

    elif pathname == "/conclusion":
        return [
                   html.Br(),
   html.Br(),
        html.H2('Conclusion'),
                html.Br(),
         html.Div(children='''
                Based on our analysis, we can observe that the region most surveyed is Sub-Saharan Africa, with 42% of surveys as depcited in the pie chart.
                On closer analysis of Sub-Saharan Africa we see that food security is the most surveyed topic across waves. We can see the same pattern across
                other regions too. Based on this we can conclude that food security is one of the major contributing factor of global pandemic impact. 

              '''),
html.Br(),
                 html.Div(children='''
               Focusing on food security topic, and question on went without eating whole day,
              '''),
                 html.Div(children='''
               We can observe that high income countries are less impacted and less surveyed, 
               where as the lower income countries are more surveyed and seems more impacted

              '''),

        html.Br(),
          html.Br(),
        html.Br(),
        html.Hr(),
        html.Br(),
                
        ]

"""# Callback"""

@app.callback(
    Output(component_id='survey_size_map', component_property='figure'),
    [Input(component_id='slct_region', component_property='value'),
     Input(component_id='slct_wave', component_property='value')]
)
def update_graph(option_slctd,option1_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df.copy()
    dff = dff[(dff["region_code"] == option_slctd) & (dff["wave"] == option1_slctd)]
    dff = dff.sort_values("indicator_topic")
    figure = px.bar(
        data_frame=dff,
        x='indicator_topic',
        y='sample_subset',
        hover_data=['indicator_topic', 'sample_subset']
        ,labels={'indicator_topic':'Survey Topic','sample_subset': 'Number of people surveyed'}
        ,template='seaborn'
    )

    figure.update_layout(title={
    'text': "<b>Countries which participated in covid impact Survey</b>",
    })


    return figure

@app.callback(
    Output(component_id='worldmapfig1', component_property='figure'),

    [Input(component_id='wave', component_property='value')]
)
def update_graph1(option_slctd):
    '''dff = final_df.copy()
    dff = dff[(dff["wave"] == option_slctd)]'''

    covid_effct_df = survey_df.copy()
    fig2 = covid_effct_df[covid_effct_df['wave'] == option_slctd].groupby(['country','income_group','sample_total']).size().to_frame().sort_values([0], ascending=False).reset_index()
    fig2.columns = ['country','income_group', 'sample_total', 'count']


    worldmapfig1 = px.choropleth(
    data_frame=fig2,
    locationmode='country names',
    locations='country',
    scope='world',
    color='country',
    hover_data=['country', 'income_group','sample_total'],
    color_continuous_scale=px.colors.sequential.Peach,
    labels={'country':'Country List'},
    template='plotly_white'
    )

    worldmapfig1.update_layout(title={
    'text': "<b>Countries which participated in covid impact Survey</b>",
    'x': 0.4,
    'y': 1,
    'xanchor': 'center',
    'yanchor': 'top'
    },
    margin=dict(l=0, r=0, t=96, b=0))

    return worldmapfig1

@app.callback(
    Output(component_id='sunburst', component_property='figure'),
    [Input(component_id='region_list', component_property='value'),
     Input(component_id='food_sub', component_property='value')]
)

def update_graph2(option_slctd2,option_slctd3):
      #sun_df = df_all_industry[ df_all_industry.region.isin(['South Asia']) & df_all_industry.urban_rural.isin(['National']) &  df_all_industry.indicator_topic.isin(['Food Security']) & df_all_industry.indicator.isin(['FS_day']) & df_all_industry.many_waves == 1 ]
      sun_df = df_all_industry[ (df_all_industry.region == option_slctd2) & (df_all_industry.urban_rural=='National') &  (df_all_industry.indicator_topic == 'Food Security') & (df_all_industry.indicator == option_slctd3) & (df_all_industry.many_waves == 1) ]
      #sun_df = df_all_industry[ df_all_industry.region.isin([option_slctd2]) & df_all_industry.urban_rural.isin(['National']) &  df_all_industry.indicator_topic.isin(['Food Security']) & df_all_industry.indicator.isin([option_slctd3]) & df_all_industry.many_waves == 1 ]

    
      fig4 = px.sunburst(
        data_frame=sun_df,
        #path=['wave','country','indicator_val_range'],
        #path=['indicator_val_range','wave','country'],
        #path=['country','indicator_val_range','wave'],
        path=['country','indicator_val','wave'],
        #path=['country','wave','indicator_val_range'],
        #path=['country','income_group','indicator_val_range'],
        values = 'sample_subset',
        color=sun_df.sample_subset,
        color_discrete_sequence=px.colors.qualitative.Pastel,
      )
      fig4.update_layout(title={
          'text': "<b>Food Security Response Stats across WAVES</b>",
          'x': 0.5,
          'y': 0.95,
          'xanchor': 'center',
          'yanchor': 'top'
      },
          margin=dict(t=50, l=45, r=45, b=45))

      return (fig4)

"""# App execution"""

if __name__ == '__main__':
    app.run_server( port=8080, debug=True,dev_tools_ui=False,dev_tools_props_check=False)
