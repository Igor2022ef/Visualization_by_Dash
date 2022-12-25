from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from waitress import serve


class DashPage:

    def __init__(self, numb: pd.DataFrame, df1: pd.DataFrame):
        self.numb = numb
        self.df1 = df1
        self.inf_inf1 = []
        self.inf_inf2 = []
        self.x = []
        self.y = []
        self.a = [self.inf_inf1.append(numb1) for numb1 in numb['Year']]
        self.b = [self.inf_inf2.append(numb2) for numb2 in numb['Index']]
        self.c = [(self.x.append(inf_inf1[i]), self.y.append(inf_inf2[i])) for i in [2, 5, 8, 11]]
        self.external_stylesheets = [
                {
                    "href": "https://fonts.googleapis.com/css2?"
                            "family=Lato:wght@400;700&display=swap",
                    "rel": "stylesheet",
                },
            ]
        self.app = Dash(__name__, external_stylesheets=external_stylesheets)
        self.df = numb.copy()
        self.fig = px.bar(df, x="Year", y='Index', color="index_name", barmode="group")
        self.fig1 = go.Figure(data=[go.Scatter(x=[x[0], x[1], x[2], x[3]], y=[y[0], y[1], y[2], y[3]])])
        self.infa3 = html.Div(children=[
            html.Div(
                children=[
                    html.H2(children='Цепной, базисный индексы.',
                            className='header-description')], className='header')])

        self.infa1 ='Цепной индекс инфляции рассчитывается по отношению к предыдущему периоду. Он как бы по' \
                    ' цепочке, от периода к периоду, передает влияние инфляции. Такой индекс удобно'\
                                 ' использовать по отношению к параметрам, для которых в модели отдельно задана цена'\
                                 ' и физические объемы.Базисный индекс инфляции показывает влияние инфляции нарастающим'\
                                 ' итогом от начала проекта. Он удобен в работе со статьями доходов и затрат, задаваемых'\
                                 ' денежными суммами, без деления на объемы и цены.'
        # className='header-description')], className='header')])

        self.infa4 = html.Div(children=[
            html.Div(
                children=[
                    html.H1(children='Темп инфляции.',
                            className='header-description')], className='header')])

        self.infa2 = html.Div(children=[
            html.Div(
                children=[
                    html.P(
                        children='Темп инфляции - это параметр, который используется не только для того, чтобы поразить'
                                 ' публику красивой каритинкой, но для реального прогноза деятельности компании на периоды'
                                 ' расчета планируемой себестоимости, заработной платы и т.п.')])])
        # className='header-description')], className='header')])

    def layout(self):
        return html.Div(children=[
                html.Div(
                    children=[
                        html.H1(children='Представление данных изменения инфляции за 2019 - 2022 гг.',
                                className='header-title')], className='header'),

                html.Div([
                    dcc.Dropdown(['Индексы', 'Темп инфляции'], 'Индексы', id='demo-dropdown', multi=True),
                    html.Div(id='dd-output-container')
                ]),
                html.H2(
                    children="Доли продуктов в потребительской корзине",
                    className='header-description'
                ),
                html.P(
                    children="График позволяет оценить динамику величины затрат по каждой составляющей продуктовой "
                             "корзины и наглядно демонстрирует, на какие из них приходятся наименьшие и наибольшие расходы.",
                ),
                dcc.Graph(id='my-graph'),
                dcc.Slider(
                    id='Year-slider',
                    min=self.df1['Year'].min(),
                    max=self.df1['Year'].max(),
                    value=self.df1['Year'].min(),
                    marks={str(Year): str(Year) for Year in self.df1['Year'].unique()},
                    step=None
                )])

    def run(self):
        self.app.layout = self.layout()

        self.app.callback(
            Output('dd-output-container', 'children'),
            Input('demo-dropdown', 'value')
            )(self.updete_output)
        self.app.callback(
            Output('my-graph', 'figure'),
            [Input('Year-slider', 'value')])(self.update_figure)

        serve(self.app.server, host='127.0.0.1', port=5050)

    def updete_output(self, value):
        fig_print = []
        if 'Индексы' in value:
            fig_print.append(self.infa3), fig_print.append(dcc.Graph(figure=self.fig))
            fig_print.append(
                html.Div(children=[
                    html.Div(
                        children=[
                            html.P(
                                children=self.infa1)])]))
        if 'Темп инфляции' in value:
            fig_print.append(self.infa4), fig_print.append(dcc.Graph(figure=self.fig1)), fig_print.append(self.infa2)
        return fig_print

    def update_figure(self, selected_Year):
        filtered_df = self.df1[self.df1.Year == selected_Year]

        fig3 = px.scatter(filtered_df, x="Quantity", y="Price",
                          size="size", color="item", hover_name="item",
                          log_x=False, size_max=100)
        return fig3


numb = pd.read_csv('infl_date.csv')
df1 = pd.read_csv('DateForBubleMyne.csv')

inf_inf1 = []
inf_inf2 = []
x = []
y = []
a = [inf_inf1.append(numb1) for numb1 in numb['Year']]
b = [inf_inf2.append(numb2) for numb2 in numb['Index']]
c = [(x.append(inf_inf1[i]), y.append(inf_inf2[i])) for i in [2,5,8,11]]

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)                     #Эта строка и строки выше про импорт шрифтов из статьи
                                                                                     #https://proglib.io/p/tutorial-vizualizaciya-dannyh-v-vebe-s-pomoshchyu-python-i-dash-2021-01-11
#app = Dash(__name__)
df = pd.DataFrame(numb)


fig = px.bar(df, x="Year", y='Index', color="index_name", barmode="group")
fig1 = go.Figure(data=[go.Scatter(x=[x[0], x[1], x[2], x[3]], y=[y[0], y[1], y[2], y[3]])])

infa3 = html.Div(children=[
    html.Div(
        children=[
            html.H2(children='Цепной, базисный индексы.',
                    className='header-description')], className='header')])

infa1 = html.Div(children=[
    html.Div(
        children=[
            html.P(children='Цепной индекс инфляции рассчитывается по отношению к предыдущему периоду. Он как бы по'
                            ' цепочке, от периода к периоду, передает влияние инфляции. Такой индекс удобно'
                            ' использовать по отношению к параметрам, для которых в модели отдельно задана цена'
                            ' и физические объемы.Базисный индекс инфляции показывает влияние инфляции нарастающим'
                            ' итогом от начала проекта. Он удобен в работе со статьями доходов и затрат, задаваемых'
                            ' денежными суммами, без деления на объемы и цены.')])])
                    # className='header-description')], className='header')])

infa4 = html.Div(children=[
    html.Div(
        children=[
            html.H1(children='Темп инфляции.',
                    className='header-description')],className='header')])

infa2 = html.Div(children=[
    html.Div(
        children=[
            html.P(children='Темп инфляции - это параметр, который используется не только для того, чтобы поразить'
                            ' публику красивой каритинкой, но для реального прогноза деятельности компании на периоды'
                            ' расчета планируемой себестоимости, заработной платы и т.п.')])])
                    # className='header-description')], className='header')])


app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H1(children='Представление данных изменения инфляции за 2019 - 2022 гг.',
                    className='header-title')], className='header'),
    #         html.H2(
    #             children='Цепной, базисный индексы и темп инфляции.',
    #                  className='header-description'
    # ),


    html.Div([
            dcc.Dropdown(['Индексы', 'Темп инфляции'],'Индексы', id='demo-dropdown', multi=True),
            html.Div(id='dd-output-container')
                ]),

    #         html.H2(
    #             children="Темп инфляции",
    #                 className='header-description'
    # ),
    #         html.P(
    #             children="",
    # ),
            html.H2(
                children="Доли продуктов в потребительской корзине",
                    className='header-description'
            ),
            html.P(
                children="График позволяет оценить динамику величины затрат по каждой составляющей продуктовой "
                         "корзины и наглядно демонстрирует, на какие из них приходятся наименьшие и наибольшие расходы.",
    ),
    dcc.Graph(id='my-graph'),
        dcc.Slider(
            id='Year-slider',
            min=df1['Year'].min(),
            max=df1['Year'].max(),
            value=df1['Year'].min(),
            marks={str(Year): str(Year) for Year in df1['Year'].unique()},
            step=None
        )])

@app.callback(
 	   Output('dd-output-container', 'children'),
    	Input('demo-dropdown', 'value')
)
def updete_output(value):
    fig_print = []
    if 'Индексы' in value:
        fig_print.append(infa3), fig_print.append(dcc.Graph(figure=fig)),fig_print.append(infa1)
    if 'Темп инфляции' in value:
        fig_print.append(infa4), fig_print.append(dcc.Graph(figure=fig1)),fig_print.append(infa2)
    return fig_print


@app.callback(
    Output('my-graph', 'figure'),
    [Input('Year-slider', 'value')])

def update_figure(selected_Year):
    filtered_df = df1[df1.Year == selected_Year]

    fig3 = px.scatter(filtered_df, x="Quantity", y="Price",
                     size="size", color="item", hover_name="item",
                     log_x=False, size_max=100)
    return fig3


if __name__ == "__main__":
    numb = pd.read_csv('infl_date.csv')
    df1 = pd.read_csv('DateForBubleMyne.csv')
    app.run_server(debug=True,
                   host='127.0.0.1')
    # dp = DashPage(numb, df1)
    # dp.infa1 = "################################################################"
    # dp.run()
