import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

df = pd.read_csv('ecommerce_estatistica.csv')

print(df.head(n = 5).to_string())

df.drop(['Unnamed: 0', 'Review1', 'Review2', 'Review3'], axis = 1, inplace = True)
df.dropna(inplace = True)

# filtro para materiais que aparecem 6 ou mais vezes e Marcas que aparecem 8 ou mais vezes
contagens = df['Material'].value_counts().reset_index()
contagens.columns = ['Material', 'frequencia']
filtro_material = contagens[contagens['frequencia'] >= 6]['Material']
df = df[df['Material'].isin(filtro_material)]

contagens = df['Marca'].value_counts().reset_index()
contagens.columns = ['Marca', 'frequencia']
filtro_marca = contagens[contagens['frequencia'] >= 8]['Marca']
df = df[df['Marca'].isin(filtro_marca)]

print('\n',df.head(n = 5).to_string())
def graf_pizza(df):
    # Grafico de pizza
    pizza = px.pie(df, names='Gênero', color='Gênero', hole=0.2,
    color_discrete_sequence=px.colors.sequential.RdBu)
    return pizza

def graf_histograma(df):
    histograma1 = px.histogram(df, x='Nota', nbins=30, title='Distribuição de Notas')
    return histograma1

def graf_bolha(df):
    bolha = px.scatter(df, x='Preço', y='Nota', size='N_Avaliações', color='Marca', hover_name='Gênero',
                      size_max=60)
    bolha.update_layout(title='Marcas mais relevantes')
    return bolha

def graf_barra(df):
    barra = px.bar(df, x='Material', y='Preço', color='Temporada', barmode='group',
                  color_discrete_sequence=px.colors.qualitative.Bold, opacity=1)
    barra.update_layout(
        title='Total de vendas por material e temporada',
        xaxis_title='Material',
        yaxis_title='Preço',
        legend_title='Temporada',
        plot_bgcolor='rgba(222, 255, 253, 1)',
        paper_bgcolor='rgba(185, 245, 241, 1)',
    )
    return barra

def graf_3d(df):
    g3d = px.scatter_3d(df, x= 'Preço', y= 'Desconto', z= 'Qtd_Vendidos_Cod', color= 'Marca')
    return g3d

def graf_linha(df):
    linha = px.line(df, x='Nota', y='N_Avaliações', color='Marca', facet_col='Temporada')
    linha.update_layout(
        title='Número de Notas das marcas por Temporada',
        xaxis_title='Nota',
        yaxis_title='N_Avaliações'
    )
    return linha

def cria_app(df):
    # Cria app
    app = Dash(__name__)

    pizza = graf_pizza(df)
    barra = graf_barra(df)
    histograma1 = graf_histograma(df)
    bolha = graf_bolha(df)
    linha = graf_linha(df)
    g3d = graf_3d(df)

    app.layout = html.Div([
        dcc.Graph(figure= pizza),
        dcc.Graph(figure=barra),
        dcc.Graph(figure=histograma1),
        dcc.Graph(figure=bolha),
        dcc.Graph(figure=linha),
        dcc.Graph(figure=g3d)
    ])
    return app

if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug= True, port= 8050) # Default 8050







