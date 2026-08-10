import pandas as pd 

def ler_dados(caminho_arquivo: str) -> pd.DataFrame:
    df = pd.read_excel(
        caminho_arquivo,
        sheet_name="Vendas",  
        header=2,            
                              
    )
 
    return df
if __name__ == "__main__":
    df = ler_dados("vendas_bagunçado.xlsx")
    print(df.head(10))
    print("\nColunas encontradas:", list(df.columns))
    print("Formato (linhas, colunas):", df.shape)