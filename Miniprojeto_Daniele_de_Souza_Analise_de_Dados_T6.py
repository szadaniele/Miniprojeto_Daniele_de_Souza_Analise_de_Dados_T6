"""
Mini-Projeto Avaliativo - Análise de Dados com Python [T6]
Módulo 1 - Semana 07
Autora: Daniele de Souza
Análise Exploratória da base Varejo.csv utilizando pandas.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_BASE = BASE_DIR / "Base Varejo.csv"
ARQUIVO_LIMPO = BASE_DIR / "df_limpo.csv"

COLUNAS = [
    "DATA", "CO_ID", "CL_ID", "CL_GENERO", "CL_EC", "CL_FHL",
    "CL_SEG", "PR_ID", "PR_CAT", "PR_NOME"
]


def formatar_inteiro(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


def carregar_base(caminho: Path) -> pd.DataFrame:
    """Carrega somente as 10 colunas úteis da base, descartando colunas vazias extras."""
    return pd.read_csv(
        caminho,
        sep=";",
        encoding="utf-8-sig",
        usecols=range(10),
        dtype={
            "CO_ID": "Int64",
            "CL_ID": "Int64",
            "CL_EC": "Int64",
            "CL_FHL": "Int64",
            "PR_ID": "Int64",
        },
    )


def resumir_qualidade(df: pd.DataFrame) -> None:
    print("\n=== QUALIDADE DA BASE - ANTES DA LIMPEZA ===")
    print(f"Registros: {formatar_inteiro(len(df))}")
    print(f"Colunas: {list(df.columns)}")
    print("Tipos de dados:")
    print(df.dtypes)
    print("\nNulos por coluna:")
    print(df.isna().sum())
    print(f"\nDuplicatas exatas: {formatar_inteiro(df.duplicated().sum())}")
    print(f"Categorias '#N/D': {formatar_inteiro((df['PR_CAT'].astype(str).str.strip() == '#N/D').sum())}")


def limpar_base(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Aplica a limpeza mínima exigida e retorna também os contadores de tratamento."""
    relatorio = {
        "nulos_antes": int(df.isna().sum().sum()),
        "duplicatas_antes": int(df.duplicated().sum()),
        "categoria_nd_antes": int((df["PR_CAT"].astype(str).str.strip() == "#N/D").sum()),
    }

    # Conversão de data para datetime. Valores inválidos seriam transformados em NaT.
    df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

    # Categorias ausentes ou marcadas como #N/D ficam explicitamente identificadas.
    df["PR_CAT"] = (
        df["PR_CAT"]
        .astype("string")
        .str.strip()
        .replace({"#N/D": pd.NA, "": pd.NA})
        .fillna("Sem Categoria")
    )

    # Remove linhas com dados essenciais ausentes.
    df = df.dropna(subset=["DATA", "CO_ID", "CL_ID", "PR_ID", "CL_FHL"]).copy()

    # Remove somente duplicatas exatas. Linhas com o mesmo CO_ID não são removidas,
    # pois uma compra pode conter vários itens/produtos.
    df = df.drop_duplicates().copy()

    # Padroniza tipos após a limpeza.
    for col in ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]:
        df[col] = df[col].astype("int64")
    df["DATA"] = pd.to_datetime(df["DATA"])

    relatorio.update({
        "nulos_depois": int(df.isna().sum().sum()),
        "duplicatas_depois": int(df.duplicated().sum()),
        "registros_depois": len(df),
        "categoria_sem_categoria": int((df["PR_CAT"] == "Sem Categoria").sum()),
    })
    return df, relatorio


def estatisticas_filhos(df: pd.DataFrame) -> pd.DataFrame:
    s = df["CL_FHL"]
    moda = s.mode()
    moda_texto = ", ".join(str(int(v)) for v in moda.tolist()) if not moda.empty else "N/A"
    estatisticas = pd.DataFrame(
        {
            "Métrica": [
                "Contagem", "Média", "Mediana", "Desvio padrão", "Moda",
                "Mínimo", "1º quartil (Q1)", "2º quartil (Q2)", "3º quartil (Q3)", "Máximo"
            ],
            "Valor": [
                int(s.count()), float(s.mean()), float(s.median()), float(s.std()), moda_texto,
                int(s.min()), float(s.quantile(0.25)), float(s.quantile(0.50)),
                float(s.quantile(0.75)), int(s.max())
            ],
        }
    )
    return estatisticas


def gerar_agrupamentos(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # 1) Gênero: volume de itens e quantidade de compras distintas.
    por_genero = (
        df.groupby("CL_GENERO")
        .agg(
            Registros=("CO_ID", "size"),
            Compras_distintas=("CO_ID", "nunique"),
            Clientes_distintos=("CL_ID", "nunique"),
        )
        .reset_index()
        .sort_values("Registros", ascending=False)
    )

    # 2) Categoria de produto: volume de itens e compras distintas.
    por_categoria = (
        df.groupby("PR_CAT")
        .agg(
            Registros=("CO_ID", "size"),
            Compras_distintas=("CO_ID", "nunique"),
            Produtos_distintos=("PR_ID", "nunique"),
        )
        .reset_index()
        .sort_values("Registros", ascending=False)
    )

    # 3) Segmento de cliente como agrupamento complementar.
    por_segmento = (
        df.groupby("CL_SEG")
        .agg(
            Registros=("CO_ID", "size"),
            Compras_distintas=("CO_ID", "nunique"),
            Clientes_distintos=("CL_ID", "nunique"),
        )
        .reset_index()
        .sort_values("Registros", ascending=False)
    )

    # 4) Evolução temporal por mês.
    por_mes = (
        df.assign(MES=df["DATA"].dt.to_period("M").astype(str))
        .groupby("MES")
        .agg(Registros=("CO_ID", "size"), Compras_distintas=("CO_ID", "nunique"))
        .reset_index()
        .sort_values("MES")
    )

    return {
        "por_genero": por_genero,
        "por_categoria": por_categoria,
        "por_segmento": por_segmento,
        "por_mes": por_mes,
    }


def gerar_conclusoes(df: pd.DataFrame, agrupamentos: dict[str, pd.DataFrame], relatorio: dict) -> list[str]:
    genero = agrupamentos["por_genero"].iloc[0]
    categoria = agrupamentos["por_categoria"].iloc[0]
    segmento = agrupamentos["por_segmento"].iloc[0]
    mes = agrupamentos["por_mes"].sort_values("Registros", ascending=False).iloc[0]

    total = len(df)
    pct_genero = genero["Registros"] / total * 100
    pct_categoria = categoria["Registros"] / total * 100
    pct_segmento = segmento["Registros"] / total * 100

    return [
        f"Após a limpeza, a base ficou com {formatar_inteiro(total)} registros, mantendo {formatar_inteiro(df['CO_ID'].nunique())} compras distintas.",
        f"O gênero {genero['CL_GENERO']} concentra {formatar_inteiro(genero['Registros'])} registros ({pct_genero:.2f}% do total), sendo o maior volume entre os gêneros.",
        f"A categoria {categoria['PR_CAT']} é a mais frequente, com {formatar_inteiro(categoria['Registros'])} registros ({pct_categoria:.2f}%).",
        f"O segmento {segmento['CL_SEG']} apresenta o maior volume, com {formatar_inteiro(segmento['Registros'])} registros ({pct_segmento:.2f}%).",
        f"O mês com maior número de registros foi {mes['MES']}, com {formatar_inteiro(mes['Registros'])} itens.",
        f"Foram convertidas {formatar_inteiro(relatorio['categoria_nd_antes'])} categorias '#N/D' para 'Sem Categoria'; após a limpeza não restaram duplicatas exatas.",
    ]


def main() -> None:
    print("Mini-Projeto Avaliativo - Análise Exploratória da Base Varejo")
    print("=" * 66)

    if not ARQUIVO_BASE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_BASE.name}. "
            "Coloque o CSV na mesma pasta do script."
        )

    df = carregar_base(ARQUIVO_BASE)
    resumir_qualidade(df)

    df_limpo, relatorio = limpar_base(df)
    df_limpo.to_csv(ARQUIVO_LIMPO, sep=";", index=False, encoding="utf-8-sig", date_format="%d/%m/%Y")

    print("\n=== LIMPEZA REALIZADA ===")
    print(f"Registros após limpeza: {formatar_inteiro(relatorio['registros_depois'])}")
    print(f"Duplicatas restantes: {relatorio['duplicatas_depois']}")
    print(f"Categorias 'Sem Categoria': {formatar_inteiro(relatorio['categoria_sem_categoria'])}")

    print("\n=== REGRA DO CO_ID ===")
    print("Cada linha representa um item comprado; CO_ID pode aparecer várias vezes na mesma compra.")
    print(f"Compras distintas (CO_ID): {formatar_inteiro(df_limpo['CO_ID'].nunique())}")
    print(f"Média de itens por compra: {df_limpo.groupby('CO_ID').size().mean():.2f}")

    print("\n=== ESTATÍSTICAS - NÚMERO DE FILHOS (CL_FHL) ===")
    stats = estatisticas_filhos(df_limpo)
    print(stats.to_string(index=False))

    agrupamentos = gerar_agrupamentos(df_limpo)
    pasta_resultados = BASE_DIR / "resultados"
    pasta_resultados.mkdir(exist_ok=True)
    for nome, tabela in agrupamentos.items():
        tabela.to_csv(pasta_resultados / f"{nome}.csv", index=False, encoding="utf-8-sig")
        print(f"\n=== AGRUPAMENTO: {nome.upper()} ===")
        print(tabela.to_string(index=False))

    conclusoes = gerar_conclusoes(df_limpo, agrupamentos, relatorio)
    print("\n=== CONCLUSÕES ===")
    for i, item in enumerate(conclusoes, 1):
        print(f"{i}. {item}")


if __name__ == "__main__":
    main()
