import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from gensim.utils import simple_preprocess
from gensim.models.doc2vec import Doc2Vec
import pandas as pd
import model_functions

from sklearn.metrics.pairwise import cosine_similarity


clean_data_df = pd.read_csv('clean_data_df_15000.csv')
combined_df = pd.read_csv('combined_df_15000.csv' )
model = Doc2Vec.load('model_15000.model')


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


header = html.Div(style={'backgroundColor': 'cornsilk'}, children = [
    html.Br(),
    html.H1("Recommending Legal Cases with NLP", style={
        'textAlign': 'center',
        'color': 'black'
    }),
    html.H2('An Unsupervised Learning Engine Using Doc2Vec',
    style={
        'textAlign': 'center',
        'color': 'black'
    }),
    html.H3('By: Minna Fingerhood, 2019',
    style={
        'textAlign': 'center',
        'color': 'black'
    }),
    html.Br(),
    ]
)

input_1 = html.Div(style={'backgroundColor': 'cornsilk'}, children = [
    html.Div(dcc.Input(id="input1", type="number", placeholder="please insert year of case i.e. 2017", min= 1900, max=3000,
    style = {'display': 'block', 'textAlign': 'center', 'width': '50%', 'margin-left': 'auto',
         'margin-right': 'auto'})),
         html.Button('Submit', id='button1', type='submit',
         style = {'display': 'block', 'textAlign': 'center', 'width': '50%', 'margin-left': 'auto',
         'margin-right': 'auto'}),
         html.Div(id="output1", children = '', style={
             'textAlign': 'center',
             'color': 'black'}),
             html.Br(),
             html.Br(),
])

input_2 = html.Div(style={'backgroundColor': 'cornsilk'}, children = [
    html.Div(dcc.Textarea(id="input2",
    placeholder="please insert case text... the more the better",
    style = {'display': 'block', 'textAlign': 'center', 'width': '50%', 'margin-left': 'auto',
     'margin-right': 'auto'}
    )),
    html.Button('Submit', id='button', type='submit',
        style = {'display': 'block', 'textAlign': 'center', 'width': '50%', 'margin-left': 'auto',
         'margin-right': 'auto'}),
    html.Br(),
    html.Div(id="output2",  children='',
         style={
    'textAlign': 'center',
    'color': 'black',
    'margin-left': 70,
     'margin-right': 70}),

])

results = html.Div(style={'backgroundColor': 'cornsilk'}, children = [
    html.Br(),
    html.Br(),
    html.Button('Get Similar Cases', id='cases_button',
        style = {'display': 'block', 'textAlign': 'center', 'width': '50%', 'margin-left': 'auto',
     'margin-right': 'auto'}),
    html.Br(),
    html.Br(),
    html.Div(id='similarCases', children = '',
        style={
            'textAlign': 'left',
            'color': 'black',
            'margin-left': 70,
             'margin-right': 70
            }),
    html.Br(),
    html.Br(),
    html.Br(),
])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': 'cornsilk'}, id = 'body', children = [
    header, input_1, input_2, results
])

@app.callback(
    dash.dependencies.Output('output1', 'children'),
    [dash.dependencies.Input('button1', 'n_clicks')],
    [dash.dependencies.State('input1', 'value')])
def update_output_text(n_clicks, value):
    return u'Case Year: {}'.format(value)


@app.callback(
    dash.dependencies.Output('output2', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input2', 'value')])
def update_output_text(n_clicks, value):
    return u'Case Text: {}'.format(value)


@app.callback(
    dash.dependencies.Output('similarCases', 'children'),
    [dash.dependencies.Input('cases_button', 'n_clicks')],
    [dash.dependencies.State('output1', 'children'),
    dash.dependencies.State('output2', 'children')])
def update_results(n_clicks, output1, output2):
    input1_update = int(output1[-4:])
    input2_vector = model_functions.clean_test_input(output2, model)
    case_text = model_functions.cosine_text_similarity(input2_vector, input1_update, combined_df, clean_data_df)
    cases = []
    for i in range(0, len(case_text)):
        cases.append(f"{case_text[i]}")
        cases.append(html.Br())
        cases.append(html.Br())
    return (cases)
    #u'Similar Cases: {}'.format(cases)


if __name__ == "__main__":
    app.run_server(debug=True)
