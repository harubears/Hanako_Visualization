import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime

index = ['測定局コード', 'アメダス測定局コード', '年月日', '時', '測定局名', '測定局種別', '都道府県コード', '都道府県名', '市区町村コード', '市区町村名', '花粉飛散量[個/m3]', '風向', '風速[m/s]', '気温[℃]', '降水量[mm]', 'レーダー降水量[mm]']
df = pd.read_csv('assets/Data_shinjuku.csv',names=index, encoding='shift_jisx0213', dtype='object')

# 花粉飛散量、気温をFloat型に
df['花粉飛散量[個/m3]'] = df['花粉飛散量[個/m3]'].astype('float')
df['気温[℃]'] = df['気温[℃]'].astype('float')
df['風速[m/s]'] = df['風速[m/s]'].astype('int')
df['風向'] = df['風向'].astype('int')



# 整数にして、マイナス１の値で上書き
df['時-1'] = df['時'].astype('int32')-1
# マイナス１にした値を文字列にし、２桁の固定長に
df['時-1'] = df['時-1'].astype(str).str.zfill(2)


# 年月日時でDatetime型に変換
df['ymdh'] = df['年月日'] + df['時-1']
df['date'] = pd.to_datetime(df['ymdh'], format='%Y%m%d%H')



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Dash 領域
app.layout = html.Div(children=[
    html.H2(children='新宿の花粉飛散量 2020'),
    ### Plotly Graph領域
    html.Div(children=[
        ### 受講生数グラフ
        dcc.Graph(
            id='pollen_graph',
            figure={
                'data':[
                    go.Scatter(
                        x=df['date'],
                        y=df['花粉飛散量[個/m3]'],
                        name='花粉飛散量',
                        mode='lines+markers',
                        opacity=0.7,
                        yaxis='y1'
                    )
                ],
                'layout': go.Layout(
                    title='花粉',
                    xaxis=dict(title='日時'),
                    yaxis=dict(
                        title='花粉',
                        side='left',
                        showgrid=True,
                        range=[min(df['花粉飛散量[個/m3]']), max(df['花粉飛散量[個/m3]']) + 10]
                    ),
                    margin=dict(l=200, r=200, b=100, t=100)
                )
            }
        ),
        dcc.Graph(
            id='temparture_graph',
            figure={
                'data': [
                    go.Scatter(
                        x=df['date'],
                        y=df['気温[℃]'],
                        mode='lines+markers',
                        name='気温',
                        opacity=0.7,
                        yaxis='y1'
                    )
                ],
                'layout': go.Layout(
                    title='気温',
                    xaxis=dict(title='日時'),
                    yaxis=dict(
                        title='気温',
                        side='left',
                        showgrid=True,
                        range=[min(df['気温[℃]']), max(df['気温[℃]'])]
                    ),
                    margin=dict(l=200, r=200, b=100, t=100)
                )
            }
        ),
        dcc.Graph(
            id='wind_graph',
            figure={
                'data': [
                    go.Scatter(
                        x=df['date'],
                        y=df['風速[m/s]'],
                        mode='lines+markers',
                        name='風速',
                        opacity=0.7,
                        yaxis='y1'
                    ),
                    go.Bar(
                        x=df['date'],
                        y=df['風向'],
                    )
                ],
                'layout': go.Layout(
                    title='風速',
                    xaxis=dict(title='日時'),
                    yaxis=dict(
                        title='風速',
                        side='left',
                        showgrid=True,
                        range=[min(df['風速[m/s]']), max(df['風速[m/s]'])]
                    ),
                    margin=dict(l=200, r=200, b=100, t=100)
                )
            }
        ),

    ]),
    html.Div(children=[

    ])
])



if __name__ == '__main__':
    app.run_server(debug=True)