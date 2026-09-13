# Mini-Projeto Avaliativo — Análise Exploratória da Base Varejo

**Autora:** Daniele de Souza
**Turma:** Analise_de_Dados_T6  
**Módulo:** 1 — Semana 07  
**Disciplina/Trilha:** Análise de Dados com Python  
**Arquivo principal:** `Miniprojeto_Daniele_de_Souza_Analise_de_Dados_T6.py`

## 1. Objetivo

Este projeto realiza uma Análise Exploratória de Dados (AED) sobre a base `Base Varejo.csv`, utilizando **pandas**, com foco em qualidade dos dados, limpeza, validação da regra de negócio do identificador de compra, estatística descritiva e agrupamentos.

O projeto foi estruturado para ser executado no **VS Code** ou no **Google Colab**.

## 2. Estrutura do repositório

```text
Miniprojeto_Daniele_de_Souza_Analise_de_Dados_T6/
├── Base Varejo.csv
├── Miniprojeto_Daniele_de_Souza_Analise_de_Dados_T6.py
├── df_limpo.csv
├── resultado_execucao.txt
├── README.md
├── README_Daniele_de_Souza_Analise_de_Dados_T6.md
├── requirements.txt
└── resultados/
    ├── por_genero.csv
    ├── por_categoria.csv
    ├── por_segmento.csv
    └── por_mes.csv
```


## 3. Como executar

### VS Code

1. Instale o Python.
2. Abra esta pasta no VS Code.
3. Instale a dependência:

```bash
pip install -r requirements.txt
```

4. Execute:

```bash
python Miniprojeto_Daniele_de_Souza_Analise_de_Dados_T6.py
```

### Google Colab

Envie `Base Varejo.csv` e o arquivo `Miniprojeto_Daniele_de_Souza_Analise_de_Dados_T6.py` para o ambiente do Colab ou copie o conteúdo do script para uma célula. Execute todas as etapas em sequência.

## 4. ETL e qualidade dos dados

**Extração:** a base `Base Varejo.csv` foi lida com `pandas.read_csv`, usando `;` como separador e aproveitando apenas as 10 colunas significativas. A inspeção inicial apontou 830.000 registros.

**Transformação:**
- conversão de `DATA` para `datetime`;
- identificação de `#N/D` em `PR_CAT`;
- substituição de `#N/D`/vazios por `Sem Categoria`;
- remoção de registros com campos essenciais ausentes;
- remoção de duplicatas exatas;
- padronização dos tipos numéricos.

**Carga:** a base tratada foi salva em `df_limpo.csv`, e os principais agrupamentos foram exportados para a pasta `resultados/`.

### Reflexão sobre qualidade de dados

Qualidade de dados é essencial porque inconsistências podem distorcer estatísticas e decisões. Neste projeto, os principais controles foram completude, consistência de tipos, validade das datas, padronização de categorias e duplicidade. A estratégia adotada foi conservadora: foram removidas apenas duplicatas exatas, enquanto ocorrências repetidas de `CO_ID` foram preservadas, pois representam itens distintos da mesma compra.

## 5. Regra de negócio do CO_ID

Cada linha representa **um item comprado**, e não uma compra inteira. Por isso, `CO_ID` pode aparecer várias vezes. O agrupamento por `CO_ID` foi utilizado para identificar uma mesma compra quando necessário.

Após a limpeza:

- **Compras distintas:** 18.471
- **Média de itens por compra:** 39,71

## 6. Estatística descritiva — número de filhos (`CL_FHL`)

| Métrica | Resultado |
|---|---:|
| Contagem | 733.447 |
| Média | 1,1460 |
| Mediana | 0 |
| Desvio padrão | 1,4169 |
| Moda | 0 |
| Mínimo | 0 |
| 1º quartil (Q1) | 0 |
| 2º quartil (Q2) | 0 |
| 3º quartil (Q3) | 2 |
| Máximo | 4 |

**Observação:** essas estatísticas são calculadas sobre as linhas de itens após a limpeza; portanto, a frequência de um cliente na base influencia a quantidade de observações.

## 7. Principais agrupamentos

### Gênero

| Gênero | Registros | Compras distintas | Clientes distintos |
|---|---:|---:|---:|
| F | 382.427 | 9.615 | 519 |
| M | 351.020 | 8.856 | 481 |

### Categoria

| Categoria | Registros | Compras distintas | Produtos distintos |
|---|---:|---:|---:|
| ALIMENTOS | 384.197 | 18.267 | 120 |
| HIGIENE | 137.702 | 17.610 | 43 |
| LIMPEZA | 128.632 | 17.475 | 40 |
| BEBIDAS | 38.264 | 14.735 | 12 |
| PET | 28.553 | 13.495 | 9 |
| ACESSORIOS | 12.871 | 9.224 | 4 |
| Sem Categoria | 3.228 | 3.228 | 1 |

### Segmento

| Segmento | Registros | Compras distintas | Clientes distintos |
|---|---:|---:|---:|
| B | 468.505 | 11.843 | 645 |
| C | 205.265 | 5.136 | 271 |
| A | 59.677 | 1.492 | 84 |

### Evolução mensal

A maior quantidade de registros ocorreu em **2021-10**, com **28.575 itens**. A série mensal completa está em `resultados/por_mes.csv`.

## 8. Conclusões

1. Após a limpeza, a base ficou com **733.447 registros** e **18.471 compras distintas**.
2. O gênero **F** concentra **52,14%** dos registros, sendo o maior volume entre os gêneros.
3. **ALIMENTOS** é a categoria mais frequente, com **384.197 registros (52,38%)**.
4. O segmento **B** representa **63,88%** dos registros, sendo o maior entre os segmentos.
5. O maior volume mensal foi observado em **2021-10**, com **28.575 itens**.
6. Foram identificadas **3.650 ocorrências de `#N/D`** em categoria antes da limpeza; após remoção de duplicatas, **3.228 registros** ficaram classificados como `Sem Categoria`.

## 9. Observação importante sobre a base

A base não possui uma coluna explícita de valor monetário. Portanto, este projeto analisa **volume de itens/registros, compras, clientes e categorias**, e não faturamento em dinheiro.
