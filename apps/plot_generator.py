import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import func_utils

colors_1 = ['#52057b', '#761FC1', '#BB6AF0', '#D4A2F6']
clock_colors = ['#52057b', '#892cdc']


def sleep_bar_plot_for_person(df, person, start, end):
    df = df.sort_values(by=['quality'], ascending=False)
    df['quality'] = df['quality'].astype('str')
    df = df[(df.start_date > start) & (df.start_date < end)]

    fig = px.bar(df[df.user == person], x='start_time', y='sleep_duration',
                 labels={
                     'start_time': '',
                     'sleep_duration': 'Sleep duration'
                 },
                 color_discrete_sequence=colors_1,
                 color='quality',
                 )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=14, color="white"),
        hoverlabel=dict(
            font_size=16
        ),
        legend_traceorder="grouped+reversed"
    )
    fig.update_traces(hovertemplate="Bed time: %{x}<br>Sleep duration: %{y}<br>")
    fig.layout.font.family = 'Rubik'
    return fig


def sleep_clock_dict(df):
    layout = go.Layout(
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=0  # top margin
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    clocks = dict()
    for id, row in df.iterrows():
        angle, duration, rest = func_utils.time_angles(row['mean_start_time'], row['mean_end_time'])
        clock_fig = go.Figure(data=[go.Pie(values=[duration, rest], labels=['Asleep', 'Awake'], textinfo="none",
                                           direction='clockwise', rotation=angle, showlegend=False,
                                           hovertemplate="<b>%{label}</b><br>Bed time: " + row['mean_start_time']
                                                         + "<br>Wake up time: " + row['mean_end_time']
                                                         + "<br>Average sleep duration: " + str(
                                               round(row['sleep_duration'],
                                                     2)) + 'h')])
        clock_fig.update_layout(layout)
        clock_fig.update_traces(marker=dict(colors=clock_colors, line=dict(color='white', width=1)), hoverinfo='skip')
        clock_fig.update_xaxes(side='left', type='category')
        clock_fig.update_yaxes(side='bottom', type='category')
        clocks[row['user']] = clock_fig

        clock_fig.add_shape(x0=0, x1=1, y0=0.5, y1=0.5, line=dict(color='white'), xref='paper', yref='paper')
        clock_fig.add_shape(x0=0.5, x1=0.5, y0=0, y1=1, line=dict(color='white'), xref='paper', yref='paper')

        clock_fig.add_annotation(text="6:00",
                                 xref="paper", yref="paper",
                                 x=0.95, y=0.54, showarrow=False, font=dict(color="white", size=14))

        clock_fig.add_annotation(text="18:00",
                                 xref="paper", yref="paper",
                                 x=0.05, y=0.54, showarrow=False, font=dict(color="white", size=14))

        clock_fig.add_annotation(text="12:00",
                                 xref="paper", yref="paper",
                                 x=0.57, y=0.05, showarrow=False, font=dict(color="white", size=14))

        clock_fig.add_annotation(text="24:00",
                                 xref="paper", yref="paper",
                                 x=0.58, y=0.95, showarrow=False, font=dict(color="white", size=14))

    return clocks


def sleep_regularity_scatter_plot(df, period):
    df = df[df['period'] == period]
    fig = px.scatter(df, x='user', y='std_min', size=[4, 4, 4],
                     labels={
                         'std_min': 'Standard deviation [min]',
                         'user': ''
                     })

    fig.update_traces(marker=dict(color=['#52057b', '#52057b', '#52057b']), hoverinfo='skip',
                      hovertemplate="%{x}<br>Standard deviation: %{y}min")

    fig.layout.font.family = 'Rubik'
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=14, color="white"),
        hoverlabel=dict(
            font_size=16
        )
    )

    return fig
