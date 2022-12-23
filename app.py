from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

promotion = pd.read_csv('promotion_clean.csv')

# create app dash instance
app = Dash(external_stylesheets=[dbc.themes.LUX])




# cleansing data 
promotion[['department','region','education',
           'gender','recruitment_channel',
           'KPIs_met >80%','awards_won?',
           'is_promoted']] = promotion[['department','region',
                                        'education','gender',
                                        'recruitment_channel',
                                        'KPIs_met >80%','awards_won?',
                                        'is_promoted']].astype('category')

promotion[['date_of_birth','join_date']] = promotion[['date_of_birth','join_date']].astype('datetime64')

data_agg = promotion.groupby(['department','is_promoted']).count()[['employee_id']].reset_index()
data_agg = data_agg.sort_values(by = 'employee_id')
bar_plot1 = px.bar(
    data_agg,
    x = 'employee_id',
    y = 'department',
    color = 'is_promoted',
    color_discrete_sequence = ['#618685','#80ced6'],
    barmode = 'group',
    orientation='h',
    template = 'ggplot2',
    labels = {
        'department': 'Department',
        'employee_id': 'No of Employee',
        'is_promoted': 'Is Promoted?',
    },
    title = 'Number of employees in each department',
    height=700,
).update_layout(showlegend=False)


# BarPlot


# LinePlot
data_2020 = promotion[promotion['join_date'] >= '2020-01-01']
data_2020 = data_2020.groupby(['join_date']).count()['employee_id'].reset_index().tail(30)
line_plot2 = px.line(
    data_2020,
    x='join_date',
    y='employee_id',
    markers=True,
    color_discrete_sequence = ['#618685'],
    template = 'ggplot2',
    labels={
        'join_date':'Join date',
        'employee_id':'Number of employee'
    },
    title = 'Number of new hires in the last 30 days',
    height=700,
)

# title HTML
app.title = "Dashboard Employee"

# data Card
card =  [
    {
        'title': 'Information',
        'data': 'this is the informatiion of employeed in our Start-Up. help to identify who is a potential candidate for promotion',
        'width': 6,
        'type': 'description',
        'color': '#fefbd8'
    },
    {
        'title': 'Number Of Employees',
        'data':  promotion.shape[0],
        'width': 3,
        'type': 'data'.capitalize(),
        'color': '#80ced6'
    },
    {
        'title': 'Number Of promoted employees',
        'data': promotion[promotion['is_promoted']=='Yes'].shape[0],
        'width': 3,
        'type': 'data',
        'color': '#d5f4e6'
    },
]
# Navbar Component
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
    ],
    brand="Employee Promotion Dashboard",
    brand_href="#",
    color="#618685",
    dark=True,
)


# component card content
def generate_card_content(title, data):
    return [
    dbc.CardHeader(title),
    dbc.CardBody(
        [
            html.P(
                data,
            ),
        ]
    ),
]

# component Card
def generate_card(dataframe):
    return dbc.Row([
            dbc.Col(
                dbc.Card(
                    generate_card_content(dataframe[i]["title"], dataframe[i]["data"]),
                    color=dataframe[i]['color']
                    ), width=dataframe[i]['width'], 
                ) for i in range(len(dataframe)
            )
        ])

app.layout = html.Div([
    navbar,
    html.Br(),
    dbc.Container(children= dbc.Row(
            generate_card(card)
    ), fluid=True),
    html.Br(),

   dbc.Container(children=dbc.Row([

        ## Row 2 Col 1
        dbc.Col(dbc.Tabs([
            # Tab 1
            dbc.Tab(dcc.Graph(figure=bar_plot1),
            label='Each Department'),

            # Tab 2
            dbc.Tab(dcc.Graph(figure=line_plot2),
            label='New Hire'),
        ])),

        ## Row 2 Col 2
        dbc.Col([
            dcc.Dropdown(
                id='choose_dept',
                options=promotion['department'].unique(),
                value="Technology"
        ),
        dcc.Graph(id='plot3')
    ])

    ]), fluid=True),
    html.Hr(),
    html.Div(children="Ricky Ariansyah", style={'text-align': 'center'})
])

@app.callback(
    Output('plot3', 'figure'),
    Input('choose_dept', 'value')
)

def update_output(value):
    data_agg = promotion[promotion['department'] == value]
    hist_plot3 = px.histogram(
        data_agg,
        x = 'length_of_service',
        nbins = 20,
        color_discrete_sequence = ['#618685','#80ced6'],
        title = f'Length of Service Distribution in {value} Department',
        template = 'ggplot2',
        labels={
            'length_of_service': 'Length of Service (years)',
        },
        marginal = 'box',
        height=700,
    )
    return hist_plot3



if __name__ == '__main__':
    app.run_server(debug=True)


