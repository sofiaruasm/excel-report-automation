import pandas as pd

MAPA_COLUNAS = {
    "DATA": "data",
    "produto": "produto",
    "Categoria ": "categoria",   
    "regiao": "regiao",
    "Qtd": "quantidade",
    "Preço Unitário (R$)": "preco_unitario",
}

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy() 
    df = _renomear_colunas(df)
    df = _remover_linhas_totalmente_vazias(df)
    df = _remover_linha_de_total(df)
    df = _limpar_texto(df)
    df = _tratar_datas(df)
    df = _tratar_preco(df)
    df = _tratar_quantidade(df)
    df = _remover_linhas_invalidas(df)
 
    df = df.reset_index(drop=True)
    return df

def _renomear_colunas(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=MAPA_COLUNAS)

def _remover_linhas_totalmente_vazias(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how="all")

def _remover_linha_de_total(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["data"] != "TOTAL"]

def _limpar_texto(df: pd.DataFrame) -> pd.DataFrame:
    colunas_texto = ["produto", "categoria", "regiao"]
    for col in colunas_texto:
        df[col] = df[col].astype(str).str.strip()  
        df[col] = df[col].str.title()

    df = _corrigir_acentos_conhecidos(df)
    return df
def _corrigir_acentos_conhecidos(df: pd.DataFrame) -> pd.DataFrame:
    correcoes_categoria = {
        "Moveis": "Móveis",
        "Eletronicos": "Eletrônicos",
    }
    df["categoria"] = df["categoria"].replace(correcoes_categoria)
    return df

def _tratar_datas(df: pd.DataFrame) -> pd.DataFrame:
    df["data"] = df["data"].apply(_parse_data_flexivel)
    return df

def _parse_data_flexivel(valor):
    if pd.isna(valor):
        return pd.NaT
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return pd.to_datetime(valor, format=formato)
        except (ValueError, TypeError):
            continue
    return pd.NaT

def _tratar_preco(df: pd.DataFrame) -> pd.DataFrame:
    df["preco_unitario"] = (
        df["preco_unitario"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.strip()
        .str.replace(",", ".", regex=False)
    )
    df["preco_unitario"] = pd.to_numeric(df["preco_unitario"], errors="coerce")
    return df

def _tratar_quantidade(df: pd.DataFrame) -> pd.DataFrame:
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    return df

def _remover_linhas_invalidas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["data", "preco_unitario", "quantidade"])
    df = df[df["quantidade"] > 0]
 
    return df

if __name__ == "__main__":
    from data_reader import ler_dados
    df_bruto = ler_dados("vendas_bagunçado.xlsx")
    df_limpo = limpar_dados(df_bruto)
    print(df_limpo)
    print("\nLinhas antes da limpeza:", len(df_bruto))
    print("Linhas depois da limpeza:", len(df_limpo))
    print("\nTipos de dado:")
    print(df_limpo.dtypes)