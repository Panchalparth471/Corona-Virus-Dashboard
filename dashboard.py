import numpy as np
import pandas as pd
from plotly import graph_objects as go
import dash
from dash import dcc
from dash import html
from dash import Input,Output

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
patients=pd.read_csv('IndividualDetails.csv')
total=patients.shape[0]
total_data=patients['current_status'].value_counts()
hospitalized=total_data['Hospitalized']
deaths=total_data['Deceased']
recovered=total_data['Recovered']
df=pd.read_csv('covid_19_india.csv')
df['Total Cases']=df['Confirmed'].cumsum()
fig=go.Figure(data=[go.Scatter(x=df['Date'],y=df['Total Cases'],mode='lines')],layout=go.Layout(title='Day by Day analysis',xaxis={'title':'Date'},yaxis={'title':'Day by Day Analysis'}))
df2=pd.read_csv('AgeGroupDetails.csv')
df2['Percentage']=df2['Percentage'].str.removesuffix('%').astype(float)
fig2=go.Figure(data=[go.Pie(labels=df2['AgeGroup'],values=df2['Percentage'],textinfo='label+percent')],layout=go.Layout(title='Age Distribution'))
options=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Deceased','value':'Deceased'},
    {'label':'Recovered','value':'Recovered'}
]


app = dash.Dash(__name__,external_stylesheets=[BS])

app.layout=html.Div([
    html.H1('Corona Virus Dashboard',style={'text-align':'center','margin':'20px'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Total Cases',className='text-light'),
                    html.H4(total,className='text-light')
                    
                    ],className='card-body')
            ],className='card bg-danger')
            
            ],className='col md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Active',className='text-light'),
                    html.H4(hospitalized,className='text-light')
                    
                    ],className='card-body')
            ],className='card bg-info')     
            ],className='col md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Recovered',className='text-light'),
                    html.H4(recovered,className='text-light')
                    
                    ],className='card-body')
            ],className='card bg-warning')
            
            ],className='col md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Deaths',className='text-light'),
                    html.H4(deaths,className='text-light')
                    
                    ],className='card-body')
            ],className='card bg-success')
            ],className='col md-6'),
        ],className='row'),
    html.Div([
         html.Div([
                dcc.Graph(figure=fig)
                ],className='col-md-6'),
        html.Div([
            dcc.Graph(figure=fig2)
        ],className='col-md-6')
        ],className='row',style={'margin-top':'15px'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options,value='All',style={'margin-bottom':'10px'}),
                    dcc.Graph(id='bar')
                    ],className='card-body')
                ],className='row')
            ],className='col md-3')
        ],className='row',style={'margin-top':'30px','padding':'10px'}),
    ],className='container')

@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(type):
    
    if type == 'All':
     pbar=patients['detected_state'].value_counts().reset_index()
     return {'data':[go.Bar(x=pbar['index'],y=pbar['detected_state'])],
            'layout':go.Layout(title='State Total Count',xaxis={'title':'States'},yaxis={'title':'Frequency'})}
     
    else:
     npat=patients[patients['current_status']==type]
     pbar=npat['detected_state'].value_counts().reset_index()
     return {'data':[go.Bar(x=pbar['index'],y=pbar['detected_state'])],
            'layout':go.Layout(title='State Total Count',xaxis={'title':'States'},yaxis={'title':'Frequency'})}



if(__name__=="__main__"):
    app.run_server(debug=True)
    
    