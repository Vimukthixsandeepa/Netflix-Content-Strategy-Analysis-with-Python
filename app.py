import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"

netflix_data = pd.read_csv("data/netflix_content_2023.csv")

netflix_data['Hours Viewed'] = netflix_data['Hours Viewed'].replace(',', '', regex=True).astype(float)

# aggregate viewership hours by content type
content_type_viewership = netflix_data.groupby('Content Type')['Hours Viewed'].sum()

fig = go.Figure(data=[
    go.Bar(
        x=content_type_viewership.index,
        y=content_type_viewership.values,
        marker_color=['skyblue', 'salmon']
    )
])

fig.update_layout(
    title='Total Viewership Hours by Content Type (2023)',
    xaxis_title='Content Type',
    yaxis_title='Total Hours Viewed (in billions)',
    xaxis_tickangle=0,
    height=500,
    width=800
)

# aggregate viewership hours by language
language_viewership = netflix_data.groupby('Language Indicator')['Hours Viewed'].sum().sort_values(ascending=False)

fig = go.Figure(data=[
    go.Bar(
        x=language_viewership.index,
        y=language_viewership.values,
        marker_color='lightcoral'
    )
])

fig.update_layout(
    title='Total Viewership Hours by Language (2023)',
    xaxis_title='Language',
    yaxis_title='Total Hours Viewed (in billions)',
    xaxis_tickangle=45,
    height=600,
    width=1000
)
# convert the "Release Date" to a datetime format and extract the month
netflix_data['Release Date'] = pd.to_datetime(netflix_data['Release Date'])
netflix_data['Release Month'] = netflix_data['Release Date'].dt.month

# aggregate viewership hours by release month
monthly_viewership = netflix_data.groupby('Release Month')['Hours Viewed'].sum()

fig = go.Figure(data=[
    go.Scatter(
        x=monthly_viewership.index,
        y=monthly_viewership.values,
        mode='lines+markers',
        marker=dict(color='blue'),
        line=dict(color='blue')
    )
])

fig.update_layout(
    title='Total Viewership Hours by Release Month (2023)',
    xaxis_title='Month',
    yaxis_title='Total Hours Viewed (in billions)',
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    height=600,
    width=1000
)

# extract the top 5 titles based on viewership hours
top_5_titles = netflix_data.nlargest(5, 'Hours Viewed')

top_5_titles[['Title', 'Hours Viewed', 'Language Indicator', 'Content Type', 'Release Date']]

# aggregate viewership hours by content type and release month
monthly_viewership_by_type = netflix_data.pivot_table(index='Release Month',
                                                      columns='Content Type',
                                                      values='Hours Viewed',
                                                      aggfunc='sum')

fig = go.Figure()

for content_type in monthly_viewership_by_type.columns:
    fig.add_trace(
        go.Scatter(
            x=monthly_viewership_by_type.index,
            y=monthly_viewership_by_type[content_type],
            mode='lines+markers',
            name=content_type
        )
    )

fig.update_layout(
    title='Viewership Trends by Content Type and Release Month (2023)',
    xaxis_title='Month',
    yaxis_title='Total Hours Viewed (in billions)',
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    height=600,
    width=1000,
    legend_title='Content Type'
)


# define seasons based on release months
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

# apply the season categorization to the dataset
netflix_data['Release Season'] = netflix_data['Release Month'].apply(get_season)

# aggregate viewership hours by release season
seasonal_viewership = netflix_data.groupby('Release Season')['Hours Viewed'].sum()

# order the seasons as 'Winter', 'Spring', 'Summer', 'Fall'
seasons_order = ['Winter', 'Spring', 'Summer', 'Fall']
seasonal_viewership = seasonal_viewership.reindex(seasons_order)

fig = go.Figure(data=[
    go.Bar(
        x=seasonal_viewership.index,
        y=seasonal_viewership.values,
        marker_color='orange'
    )
])

fig.update_layout(
    title='Total Viewership Hours by Release Season (2023)',
    xaxis_title='Season',
    yaxis_title='Total Hours Viewed (in billions)',
    xaxis_tickangle=0,
    height=500,
    width=800,
    xaxis=dict(
        categoryorder='array',
        categoryarray=seasons_order
    )
)

monthly_releases = netflix_data['Release Month'].value_counts().sort_index()

monthly_viewership = netflix_data.groupby('Release Month')['Hours Viewed'].sum()

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=monthly_releases.index,
        y=monthly_releases.values,
        name='Number of Releases',
        marker_color='goldenrod', 
        opacity=0.7,
        yaxis='y1'
    )
)

fig.add_trace(
    go.Scatter(
        x=monthly_viewership.index,
        y=monthly_viewership.values,
        name='Viewership Hours',
        mode='lines+markers',
        marker=dict(color='red'),
        line=dict(color='red'),
        yaxis='y2'
    )
)

fig.update_layout(
    title='Monthly Release Patterns and Viewership Hours (2023)',
    xaxis=dict(
        title='Month',
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    yaxis=dict(
        title='Number of Releases',
        showgrid=False,
        side='left'
    ),
    yaxis2=dict(
        title='Total Hours Viewed (in billions)',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(
        x=1.05,  
        y=1,
        orientation='v',
        xanchor='left'
    ),
    height=600,
    width=1000
)

netflix_data['Release Day'] = netflix_data['Release Date'].dt.day_name()

weekday_releases = netflix_data['Release Day'].value_counts().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

# aggregate viewership hours by day of the week
weekday_viewership = netflix_data.groupby('Release Day')['Hours Viewed'].sum().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=weekday_releases.index,
        y=weekday_releases.values,
        name='Number of Releases',
        marker_color='blue',
        opacity=0.6,
        yaxis='y1'
    )
)

fig.add_trace(
    go.Scatter(
        x=weekday_viewership.index,
        y=weekday_viewership.values,
        name='Viewership Hours',
        mode='lines+markers',
        marker=dict(color='red'),
        line=dict(color='red'),
        yaxis='y2'
    )
)

fig.update_layout(
    title='Weekly Release Patterns and Viewership Hours (2023)',
    xaxis=dict(
        title='Day of the Week',
        categoryorder='array',
        categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ),
    yaxis=dict(
        title='Number of Releases',
        showgrid=False,
        side='left'
    ),
    yaxis2=dict(
        title='Total Hours Viewed (in billions)',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(
        x=1.05,  
        y=1,
        orientation='v',
        xanchor='left'
    ),
    height=600,
    width=1000
)


# define significant holidays and events in 2023
important_dates = [
    '2023-01-01',  # new year's day
    '2023-02-14',  # valentine's ay
    '2023-07-04',  # independence day (US)
    '2023-10-31',  # halloween
    '2023-12-25'   # christmas day
]

# convert to datetime
important_dates = pd.to_datetime(important_dates)

# check for content releases close to these significant holidays (within a 3-day window)
holiday_releases = netflix_data[netflix_data['Release Date'].apply(
    lambda x: any((x - date).days in range(-3, 4) for date in important_dates)
)]

# aggregate viewership hours for releases near significant holidays
holiday_viewership = holiday_releases.groupby('Release Date')['Hours Viewed'].sum()


import dash
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__)

# Color palette
COLORS = {
    'bg': '#1a1a1a',         # Dark background
    'card': '#242424',       # Card background
    'primary': '#e50914',    # Netflix red
    'text': '#ffffff',       # White text
    'grid': '#333333',       # Grid lines
    'accent1': '#00ff00',    # Success green
    'accent2': '#ff9900'     # Warning orange
}

app.layout = html.Div([
    # Header with Title and Total Numbers
    html.Div([
        html.H1("NETFLIX CONTENT ANALYTICS 2023", style={'color': COLORS['primary'], 'margin': 0}),
        html.Div([
            html.Div([
                html.H3("2.4B", style={'margin': '0', 'color': COLORS['accent1']}),
                html.P("Total Views", style={'margin': '0'})
            ], style={'textAlign': 'center'}),
            html.Div([
                html.H3("190+", style={'margin': '0', 'color': COLORS['accent2']}),
                html.P("Countries", style={'margin': '0'})
            ], style={'textAlign': 'center'}),
            html.Div([
                html.H3("1240", style={'margin': '0', 'color': COLORS['primary']}),
                html.P("Active Shows", style={'margin': '0'})
            ], style={'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'})
    ], style={'padding': '20px', 'backgroundColor': COLORS['card'], 'borderRadius': '10px', 'marginBottom': '20px'}),
    
    # Main Grid Layout
    html.Div([
        # Left Column - 60%
        html.Div([
            # Monthly Trend Chart
            html.Div([
                dcc.Graph(
                    figure=go.Figure(
                        data=[go.Scatter(
                            x=monthly_viewership.index,
                            y=monthly_viewership.values,
                            fill='tozeroy',
                            line=dict(color=COLORS['primary'], width=3),
                            name='Monthly Views'
                        )],
                        layout=go.Layout(
                            title='Monthly Viewership Trends',
                            plot_bgcolor=COLORS['card'],
                            paper_bgcolor=COLORS['card'],
                            font=dict(color=COLORS['text']),
                            height=300,
                            margin=dict(l=40, r=40, t=60, b=40),
                            xaxis=dict(showgrid=True, gridcolor=COLORS['grid']),
                            yaxis=dict(showgrid=True, gridcolor=COLORS['grid'])
                        )
                    ),
                    config={'displayModeBar': False}
                )
            ], style={'backgroundColor': COLORS['card'], 'borderRadius': '10px', 'padding': '15px', 'marginBottom': '20px'}),
            
            # Weekly Patterns
            html.Div([
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x=weekday_releases.index,
                                y=weekday_releases.values,
                                name='Releases',
                                marker_color=COLORS['accent2']
                            ),
                            go.Scatter(
                                x=weekday_viewership.index,
                                y=weekday_viewership.values,
                                name='Views',
                                line=dict(color=COLORS['accent1'], width=3)
                            )
                        ],
                        layout=go.Layout(
                            title='Weekly Release Patterns & Viewership',
                            plot_bgcolor=COLORS['card'],
                            paper_bgcolor=COLORS['card'],
                            font=dict(color=COLORS['text']),
                            height=300,
                            margin=dict(l=40, r=40, t=60, b=40),
                            xaxis=dict(showgrid=True, gridcolor=COLORS['grid']),
                            yaxis=dict(showgrid=True, gridcolor=COLORS['grid']),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                    ),
                    config={'displayModeBar': False}
                )
            ], style={'backgroundColor': COLORS['card'], 'borderRadius': '10px', 'padding': '15px'})
        ], style={'width': '60%', 'paddingRight': '20px'}),
        
        # Right Column - 40%
        html.Div([
            # Content Type Distribution
            html.Div([
                dcc.Graph(
                    figure=go.Figure(
                        data=[go.Pie(
                            labels=content_type_viewership.index,
                            values=content_type_viewership.values,
                            hole=.7,
                            marker=dict(colors=[COLORS['primary'], COLORS['accent2']])
                        )],
                        layout=go.Layout(
                            title='Content Distribution',
                            plot_bgcolor=COLORS['card'],
                            paper_bgcolor=COLORS['card'],
                            font=dict(color=COLORS['text']),
                            height=200,
                            margin=dict(l=20, r=20, t=60, b=20),
                            showlegend=True
                        )
                    ),
                    config={'displayModeBar': False}
                )
            ], style={'backgroundColor': COLORS['card'], 'borderRadius': '10px', 'padding': '15px', 'marginBottom': '20px'}),
            
            # Language Distribution
            html.Div([
                dcc.Graph(
                    figure=go.Figure(
                        data=[go.Bar(
                            x=language_viewership.index[:5],  # Show top 5 languages
                            y=language_viewership.values[:5],
                            marker_color=COLORS['primary']
                        )],
                        layout=go.Layout(
                            title='Top Languages',
                            plot_bgcolor=COLORS['card'],
                            paper_bgcolor=COLORS['card'],
                            font=dict(color=COLORS['text']),
                            height=200,
                            margin=dict(l=40, r=40, t=60, b=40),
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor=COLORS['grid'])
                        )
                    ),
                    config={'displayModeBar': False}
                )
            ], style={'backgroundColor': COLORS['card'], 'borderRadius': '10px', 'padding': '15px', 'marginBottom': '20px'}),
            
            # Top 5 Titles Table
            html.Div([
                html.H3("Top Performing Titles", style={'color': COLORS['text'], 'marginTop': '0'}),
                html.Table([
                    html.Thead(
                        html.Tr([
                            html.Th("Title", style={'textAlign': 'left'}),
                            html.Th("Views", style={'textAlign': 'right'})
                        ])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(top_5_titles.iloc[i]['Title']),
                            html.Td(f"{top_5_titles.iloc[i]['Hours Viewed']}M", style={'textAlign': 'right'})
                        ]) for i in range(len(top_5_titles))
                    ])
                ], style={'width': '100%', 'color': COLORS['text']})
            ], style={'backgroundColor': COLORS['card'], 'borderRadius': '10px', 'padding': '15px'})
        ], style={'width': '40%'})
    ], style={'display': 'flex'})
], style={
    'padding': '20px',
    'backgroundColor': COLORS['bg'],
    'minHeight': '100vh',
    'fontFamily': 'Arial, sans-serif'
})

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Netflix Analytics</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                background-color: #1a1a1a;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #333;
            }
            th {
                font-weight: bold;
                color: #e50914;
            }
            .js-plotly-plot .plotly .modebar {
                display: none !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True)