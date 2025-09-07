import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 importando os dados
df =  pd.read_csv('medical_examination.csv')

# 2 calculando o IMC para indicar se a pessoa está acima do peso e adicinando a coluna de overweight
df_sobrepeso = df["weight"] / ((df["height"] / 100) ** 2)
df["overweight"] = (df_sobrepeso > 25).astype(int) # se estiver acima do peso, 1, se não, 0

# 3 Normalizando os dados de colesterol e glicose para 0 e 1
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)

# 4 Função para criação do gráfico categórico
def draw_cat_plot():
    # 5 Transformando dados com melt
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"],
        var_name="variable",
        value_name="value",
    )
    # 6 Agrupando os dados e mostrando a contagem de cada grupo
    df_cat = (
        df_cat.groupby(["cardio", "variable", "value"])
        .size()
        .reset_index(name="total")
    )
    # 7 Criando o gráfico pedido
    grafico_df = sns.catplot(
        x="variable", y="total", hue="value", col="cardio",
        data=df_cat, kind="bar"
    )
    grafico_df.set_axis_labels("variable", "total")
    grafico_df.set_titles("cardio = {col_name}")



    # 8 atribuindo o gráfico a uma variável
    fig = grafico_df.figure


    # 9 Salvando e exportando o gráfico
    fig.savefig('catplot.png')
    return fig


# 10 Criando função para o mapa de calor
def draw_heat_map():
    
    # 11 Limpando os dados
    df_heat = df.copy()

    # Condição para veiricar pressão, altura e peso
    df_heat = df[
    (df['ap_lo'] <= df['ap_hi']) &
    (df['height'] >= df['height'].quantile(0.025)) &
    (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) &
    (df['weight'] <= df['weight'].quantile(0.975))
]


    # 12 Criando a matriz de correlação
    corr = df_heat.corr()

    # Garantir que -0.0 vire 0.0
    corr = corr.round(1)

    # 13 criando máscara para o triângulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14 Configurando tamanho da figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15 plotando o mapa de calor

    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        square=True,
        linewidths=0.5,
        ax=ax,
        cbar_kws={"shrink": 0.5},
        vmax=0.3,
        center=0
    )
    # 16 Salvando e exportando o mapa de calor
    fig.savefig('heatmap.png')
    return fig



