# Importa as bibliotecas pandas e matplotlib.pyplot
import pandas as pd
import matplotlib.pyplot as plt

# Lê o arquivo Excel contendo os dados de emissões de gases, especificando a planilha 'GEE Estados'
emissoes_gases = pd.read_excel('1-SEEG10_GERAL-BR_UF_2022.10.27-FINAL-SITE.xlsx', sheet_name='GEE Estados')

# Imprime o dataframe inteiro
print(emissoes_gases)

# Imprime informações sobre o dataframe, como colunas, tipos de dados e memória utilizada
print(emissoes_gases.info())

# Imprime os valores únicos da coluna 'Emissão / Remoção / Bunker'
print(emissoes_gases['Emissão / Remoção / Bunker'].unique())

# Verifica quais linhas possuem 'Remoção NCI' ou 'Remoção' na coluna 'Emissão / Remoção / Bunker'
print((emissoes_gases['Emissão / Remoção / Bunker'] == 'Remoção NCI') | (emissoes_gases['Emissão / Remoção / Bunker'] == 'Remoção'))

# Filtra o dataframe para incluir apenas as linhas com 'Remoção NCI' ou 'Remoção'
print(emissoes_gases[emissoes_gases['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção'])])

# Filtra o dataframe para incluir apenas as linhas com 'Remoção NCI' ou 'Remoção' e seleciona as colunas de 1970 a 2021
print(emissoes_gases.loc[emissoes_gases['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção']), 1970:2021])

# Encontra os valores máximos de emissão para as linhas filtradas entre 1970 e 2021
print(emissoes_gases.loc[emissoes_gases['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção']), 1970:2021].max())

# Imprime os estados únicos que têm 'Bunker' na coluna 'Emissão / Remoção / Bunker'
print(emissoes_gases.loc[emissoes_gases['Emissão / Remoção / Bunker'] == 'Bunker', 'Estado'].unique())

# Filtra o dataframe para incluir apenas as linhas com 'Emissão' na coluna 'Emissão / Remoção / Bunker'
emissoes_gases = emissoes_gases[emissoes_gases['Emissão / Remoção / Bunker'] == 'Emissão']
print(emissoes_gases)

# Remove a coluna 'Emissão / Remoção / Bunker'
emissoes_gases = emissoes_gases.drop(columns='Emissão / Remoção / Bunker')
print(emissoes_gases)

# Imprime os nomes das colunas do nível 1 ao produto
print(emissoes_gases.loc[:, 'Nível 1 - Setor':'Produto'].columns)

# Cria uma lista com os nomes das colunas do nível 1 ao produto
colunas_info = list(emissoes_gases.loc[:, 'Nível 1 - Setor':'Produto'].columns)
print(colunas_info)

# Imprime os nomes das colunas de 1970 a 2021
print(emissoes_gases.loc[:, 1970:2021].columns)

# Cria uma lista com os nomes das colunas de 1970 a 2021
colunas_emissao = list(emissoes_gases.loc[:, 1970:2021].columns)
print(colunas_emissao)

# Transforma o dataframe de wide para long, mantendo as colunas de informação e convertendo os anos em uma coluna 'Ano' e os valores em 'Emissão'
print(emissoes_gases.melt(id_vars=colunas_info, value_vars=colunas_emissao, var_name='Ano', value_name='Emissão'))

# Armazena o dataframe transformado em uma nova variável
emissoes_por_ano = emissoes_gases.melt(id_vars=colunas_info, value_vars=colunas_emissao, var_name='Ano', value_name='Emissão')

# Agrupa o dataframe por tipo de gás
print(emissoes_por_ano.groupby('Gás'))

# Imprime os grupos do agrupamento por tipo de gás
print(emissoes_por_ano.groupby('Gás').groups)

# Imprime as linhas do grupo que contém 'CO2 (t)'
print(emissoes_por_ano.groupby('Gás').get_group('CO2 (t)'))

# Soma as emissões por tipo de gás
print(emissoes_por_ano.groupby('Gás').sum())

# Armazena o resultado da soma das emissões por tipo de gás, ordenado de forma decrescente
emissao_por_gas = emissoes_por_ano.groupby('Gás').sum().sort_values('Emissão', ascending=False)
print(emissao_por_gas)

# Plota um gráfico de barras horizontais das emissões por gás
emissao_por_gas.plot(kind='barh', figsize=(10, 6))
plt.show()

# Imprime as nove primeiras linhas do dataframe
print(emissao_por_gas.iloc[0:9])

# Calcula e imprime a porcentagem de emissão de CO2 em relação ao total de emissões
print(f'A emissão de CO2 corresponde a {float(emissao_por_gas.iloc[0:9].sum()/emissao_por_gas.sum())*100:.2f} % de emissão total de gases estufa no Brasil de 1970 a 2021.')

# Agrupa o dataframe por tipo de gás e setor
gas_por_setor = emissoes_por_ano.groupby(['Gás', 'Nível 1 - Setor']).sum()
print(gas_por_setor)

# Imprime as linhas do grupo que contém 'CO2 (t)'
print(gas_por_setor.xs('CO2 (t)', level=0))

# Imprime as linhas do grupo que contém 'CO2 (t)' e 'Mudança de Uso da Terra e Floresta'
print(gas_por_setor.xs(('CO2 (t)', 'Mudança de Uso da Terra e Floresta'), level=[0, 1]))

# Encontra o valor máximo de emissão de CO2 por setor
print(gas_por_setor.xs('CO2 (t)', level=0).max())

# Encontra o índice do valor máximo de emissão de CO2 por setor
print(gas_por_setor.xs('CO2 (t)', level=0).idxmax())

# Encontra os índices dos valores máximos de emissão por tipo de gás
print(gas_por_setor.groupby(level=0).idxmax())

# Encontra os valores máximos de emissão por tipo de gás
print(gas_por_setor.groupby(level=0).max())

# Armazena os valores máximos em uma variável
valores_max = gas_por_setor.groupby(level=0).max().values

# Cria uma tabela sumarizada com os índices e valores máximos de emissão por tipo de gás
tabela_sumarizada = gas_por_setor.groupby(level=0).idxmax()
tabela_sumarizada.insert(1, 'Quantidade de emissão', valores_max)
print(tabela_sumarizada)

# Troca o nível dos índices de lugar
print(gas_por_setor.swaplevel(0, 1))

# Encontra os índices dos valores máximos de emissão por setor
print(gas_por_setor.swaplevel(0, 1).groupby(level=0).idxmax())

# Imprime o dataframe transformado para long
print(emissoes_por_ano)

# Plota um gráfico da média das emissões por ano
emissoes_por_ano.groupby('Ano').mean().plot(figsize=(10, 6))
plt.show()

# Encontra o índice do ano com maior média de emissão
print(emissoes_por_ano.groupby('Ano').mean().idxmax())

# Agrupa as médias de emissão por ano e tipo de gás
print(emissoes_por_ano.groupby(['Ano', 'Gás']).mean())

# Armazena o resultado do agrupamento em uma nova variável e redefine os índices
media_emissao_anual = emissoes_por_ano.groupby(['Ano', 'Gás']).mean().reset_index()
print(media_emissao_anual)

# Transforma o dataframe em uma tabela pivot, com anos como índice, gases como colunas e emissões como valores
media_emissao_anual = media_emissao_anual.pivot_table(index='Ano', columns='Gás', values='Emissão')
print(media_emissao_anual)

# Plota gráficos de linha para cada tipo de gás
media_emissao_anual.plot(subplots=True, figsize=(10, 40))
plt.show()

# Lê o arquivo Excel contendo os dados de população dos estados, com cabeçalho na linha 1 e ignorando as últimas 34 linhas
populacao_estados = pd.read_excel('POP2022_Municipios.xls', header=1, skipfooter=34)
print(populacao_estados)

# Agrupa os dados de população por UF e soma
print(populacao_estados.groupby('UF').sum())

# Verifica se há parênteses nos valores da coluna 'POPULAÇÃO'
print(populacao_estados[populacao_estados['POPULAÇÃO'].str.contains('\(', na=False)])

# Cria novas colunas removendo parênteses e pontos dos valores da coluna 'POPULAÇÃO'
populacao_estados = populacao_estados.assign(
    populacao_sem_parenteses=populacao_estados['POPULAÇÃO'].replace('\(\d{1,2}\)', '', regex=True),
    populacao=lambda x: x.loc[:, 'populacao_sem_parenteses'].replace('\.', '', regex=True)
)

# Verifica novamente se há parênteses nos valores da coluna 'POPULAÇÃO'
print(populacao_estados[populacao_estados['POPULAÇÃO'].str.contains('\(', na=False)])

# Converte a coluna 'populacao' para o tipo inteiro
populacao_estados.loc[:, 'populacao'] = populacao_estados['populacao'].astype(int)

# Agrupa os dados de população por UF e soma, depois redefine o índice
populacao_estados = populacao_estados.groupby('UF').sum()['populacao'].reset_index()
print(populacao_estados)

# Agrupa as emissões do ano 2021 por estado e soma, depois redefine o índice
emissao_estados = emissoes_por_ano[emissoes_por_ano['Ano'] == 2021].groupby('Estado').sum().reset_index()
print(emissao_estados)

# Junta os dados de emissão e população por estado
dados_agrupados = pd.merge(emissao_estados, populacao_estados, left_on='Estado', right_on='UF')
print(dados_agrupados)

# Plota um gráfico de dispersão das emissões versus população
dados_agrupados.plot(x='populacao', y='Emissão', kind='scatter', figsize=(8, 6))
plt.show()

# Importa a biblioteca plotly.express
import plotly.express as px

# Plota um gráfico de dispersão das emissões versus população usando plotly
px.scatter(data_frame=dados_agrupados, x='populacao', y='Emissão', text='Estado', opacity=0)
plt.show()

# Adiciona uma coluna de emissões per capita, ordena o dataframe e imprime
dados_agrupados = dados_agrupados.assign(emissao_per_capita=dados_agrupados['Emissão'] / dados_agrupados['populacao']).sort_values('emissao_per_capita', ascending=False)
print(dados_agrupados)

# Plota um gráfico de barras das emissões per capita por estado usando plotly
px.bar(data_frame=dados_agrupados, x='Estado', y='emissao_per_capita')
plt.show()

# Plota um gráfico de dispersão das emissões versus população, dimensionando os pontos pelas emissões per capita usando plotly
px.scatter(data_frame=dados_agrupados, x='populacao', y='Emissão', text='Estado', size='emissao_per_capita')
plt.show()
